from typing import Optional, List, Mapping

from nezha.ustring import is_valid_password, unique_id
from nezha.utime import strftime
from sqlalchemy import Column, Integer, String, DateTime, FetchedValue


class AccountNotExist(ValueError):
    pass


class PasswordInvalid(ValueError):
    pass


class PasswordExisted(PasswordInvalid):
    pass


class PasswordFormatError(PasswordInvalid):
    pass


class FlaskUser:
    """
    usage:

        class MyFlaskUser(FlaskUser):
            pass

        MyFlaskUser.init_db(db, encrypt_instance, password_length_range)
    """
    id = Column(Integer, primary_key=True)
    uuid = Column(String(32), nullable=False)
    name = Column(String(32), nullable=False, comment='账户名', unique=True)
    role = Column(String(32), nullable=True, comment='角色 uuid')
    phone = Column(String(32), nullable=True, index=True)
    email = Column(String(128), nullable=True, index=True)
    password = Column(String(128), nullable=True)
    status = Column(Integer, nullable=True, comment='状态:0:正常;1:废弃')
    last_login_time = Column(DateTime, nullable=True, comment="最近一次登录时间。判断第一次登录时使用。")
    create_at = Column(DateTime, nullable=True, server_default=FetchedValue())
    update_at = Column(DateTime, nullable=True)

    def filter_one(cls, condition: Mapping) -> Optional['Account']:
        return cls.query.filter_by(**condition).first()

    @classmethod
    def init_db(cls, db, encrypt_instance, password_length_range: Optional[List[int]]):
        """
        :param db: sqlalchemy mysql db instance.
        :param encrypt_instance: implement encrypt and decrypt method.
        :param password_length_range: It is a range list.
        :return:
        """
        cls.db = db
        cls.encrypt_instance = encrypt_instance
        cls.password_length_range = password_length_range

    @classmethod
    def is_valid_password(cls, raw_password: str) -> bool:
        return is_valid_password(raw_password, length_range=cls.password_length_range)

    @classmethod
    def encrypt_password(cls, raw_password: str) -> str:
        return cls.encrypt_instance.encrypt(raw_password)

    @classmethod
    def check_account_ins(cls, account_ins: Optional['FlaskUser']):
        if not account_ins:
            raise ValueError(f'account_ins {account_ins} is invalid.')

    @classmethod
    def update_password(cls, account_ins: Optional['FlaskUser'], new_password: str):
        """
        :param account_ins:
        :param new_password:
        :return:
        """
        cls.check_account_ins(account_ins)
        if not cls.is_valid_password(new_password):
            raise PasswordFormatError(f'new_password {new_password} format is wrong.')
        account_ins.password = cls.encrypt_password(new_password)
        cls.db.session.add(account_ins)
        cls.db.session.commit()

    @classmethod
    def is_first_login(cls, account_ins: Optional['FlaskUser']) -> bool:
        try:
            cls.check_account_ins(account_ins)
        except:
            return False
        return not account_ins.last_login_time

    @classmethod
    def login(cls, account_ins: Optional['FlaskUser'], password: str):
        cls.check_account_ins(account_ins)
        if account_ins.password != cls.encrypt_password(password):
            raise PasswordInvalid(f'password {password} is wrong.')
        account_ins.last_login_time = strftime()
        cls.db.session.add(account_ins)
        cls.db.session.commit()

    @classmethod
    def register(cls, name: str, role: str, phone: str, email: str, password: str):
        parameter = {k: v for k, v in locals().items() if k != 'cls'}
        if not cls.is_valid_password(password):
            raise PasswordFormatError(f'password {password} format error.')
        instance = cls(**parameter)
        instance.uuid = unique_id()
        instance.password = cls.encrypt_password(instance.password)
        instance.status = 0
        instance.create_at = strftime()
        cls.db.session.add(instance)
        cls.db.session.commit()
