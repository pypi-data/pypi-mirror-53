import json
from functools import partial
from typing import Any, Mapping, Optional, Tuple, Dict, List

from flask_requests import get_data
from nezha.encryption.aes import AESCrypt
from nezha.func import check_argument
from nezha.obj import has_callable_method
from nezha.ustring import is_valid_password

check_cls_argument = partial(check_argument, is_func_decorated=False)

try:
    # used when stored_db is mysql and sqlalchemy orm is used.
    from sqlalchemy import Column, Integer, String, DateTime, FetchedValue


    class UserModel:
        id = Column(Integer, primary_key=True)
        uuid = Column(String(32), nullable=False)
        account = Column(String(32), nullable=False, comment='账户名，登录时使用', unique=True)
        role = Column(String(32), nullable=True, comment='角色 uuid')
        phone = Column(String(32), nullable=True, index=True)
        email = Column(String(128), nullable=True, index=True)
        password = Column(String(128), nullable=True)
        status = Column(Integer, nullable=True, comment='状态:0:正常;1:废弃')
        last_login_time = Column(DateTime, nullable=True, comment="最近一次登录时间。判断第一次登录时使用。")
        create_at = Column(DateTime, nullable=True, server_default=FetchedValue())
        update_at = Column(DateTime, nullable=True)

        @classmethod
        def bind(cls, obj) -> None:
            """
            usage:

            class User(db.Model):
                pass
            UserModel.bound(User)

            """
            set_user_attr = lambda item: setattr(obj, item[0], item[1])
            list(map(set_user_attr, attrs(cls)))

except Exception as e:
    pass


def _verify_stored_db(stored_db) -> bool:
    return has_callable_method(stored_db, ('filter_one', 'get_attr'))


def _verify_encrypt_obj(encrypt_class) -> bool:
    return has_callable_method(encrypt_class, ('encrypt', 'decrypt'))


def _verify_cache_obj(cache_obj) -> bool:
    if not cache_obj:
        return True
    return has_callable_method(cache_obj, ('get', 'set')) and hasattr(cache_obj, 'expire')


def _check_account_ins(account_ins) -> bool:
    """
    account ins should have the UserModel attributes and update method
    :param account_ins:
    :return:
    """
    expected_attrs = attrs(UserModel)
    if not any(map(lambda key: getattr(account_ins, key, None), expected_attrs)):
        return False
    return has_callable_method(account_ins, ('update',))


def filter_one(cls, condition: Mapping):
    """
    query stored_db by condition.
    :param cls:
    :param condition:
    :return:
    """
    return cls.query.filter_by(**condition).first()


def get_attr(instance, key: str) -> Optional[Any]:
    """
    Get instance attribute by key.
    It's default method.
    :param instance:
    :param key:
    :return:
    """
    return getattr(instance, key, None)


def attrs(obj) -> Tuple[Tuple[str, Any], ...]:
    condition = lambda item: not (item[0].startswith('__') or isinstance(item[1], (classmethod, staticmethod)))
    return tuple(filter(condition, obj.__dict__.items()))


class ParameterError(Exception):
    pass


class AccountNotExist(ParameterError):
    pass


class PasswordInvalid(ParameterError):
    pass


class PasswordExisted(PasswordInvalid):
    pass


class PasswordFormatError(PasswordInvalid):
    pass


class AccessDeny(Exception):
    pass


class User:

    @check_cls_argument(_verify_stored_db, 2)
    @check_cls_argument(_verify_encrypt_obj, 'encrypt_class')
    @check_cls_argument(_verify_cache_obj, 'cache_obj')
    def __init__(self, account_key: str, password_key: str,
                 stored_db: Any,
                 password_secret_key: Optional[str] = 'it is hard to guess',
                 encrypt_class: Any = AESCrypt,
                 cache_obj: Any = None):
        """
        :param account_key: stored_db account field
        :param password_key: stored_db password field
        :param stored_db:
            Forbid to change the parameter position.
            stored_db should implement filter method, the return value should be object and implement.
            if stored_db is sqlalchemy, filter function can be used.
        :param password_secret_key: encrypt password key.
        :param encrypt_class:
            It has encrypt and decrypt method.
            And the __init__ method accepts password_secret_key as parameter.
        :param cache_obj: cache_obj is used to record failed login retry times. Such as redis client.
            cache_obj should has set / get method and expire attribute.
        """
        self.account_key = account_key
        self.password_key = password_key
        self.stored_db = stored_db
        self.password_secret_key = password_secret_key
        self.encrypt_instance = encrypt_class(self.password_secret_key)
        self.cache_obj = cache_obj

    def get_account_info(self, condition: Mapping):
        """
        get account info from stored_db.
        :param condition:
        :return: subclass of UserModel
        """
        return self.stored_db.filter_one(condition)

    def verify_password(self, stored_password: str, receiver_password: str) -> bool:
        return stored_password == self.encrypt_instance.encrypt(receiver_password)

    def generate_password(self, password: str) -> str:
        return self.encrypt_instance.encrypt(password)

    def record_retry_times(self, account: str, expire: int = 3600) -> int:
        """
        record retry times when login failed.
        :param account: login account, it should be unique key.
        :param expire: unit second. cache expire time.
        :return:
        """
        if not self.cache_obj:
            raise SystemError(f'self.cache_obj {self.cache_obj} is invalid.')
        retry_times_key = f'retry_times_{account}'
        retried_times = int(self.cache_obj.get(retry_times_key) or 0)
        current_retry_times = retried_times + 1
        self.cache_obj.set(retry_times_key, current_retry_times + 1, expire)
        return current_retry_times

    def generate_token(self, info: str) -> str:
        return self.encrypt_instance.encrypt(info)

    def is_first_login(self, account_ins) -> bool:
        """

        :param account_ins: keep pace with method get_account_info, account_ins should implement UserModel attrs.
        :return:
        """
        if not account_ins:
            return False
        return bool(getattr(account_ins, 'last_login_time', None))

    def login(self, max_retry_times: int = 5, expire: int = 3600, token_key: str = 'token') -> Dict:
        """

        :param max_retry_times: tolerate max retry times when login failed.
        :param expire: how long to deny access when beyond max retry times.
        :return:
        """
        # parse data from request.
        received_data = get_data(self.account_key, self.password_key)
        if not received_data:
            raise ParameterError(
                f'parse data from request failed. received_data {received_data}, account_key {self.account_key} password_key {self.password_key}')
        account, password = received_data
        # retry_times
        if max_retry_times:
            retry_times = self.record_retry_times(account, expire)
            if retry_times > max_retry_times:
                raise AccessDeny(f'retry_times {retry_times} too much in {expire} seconds')
        # verify account.
        account_ins = self.get_account_info({self.account_key: account})
        if not (account_ins and _check_account_ins(account_ins)):
            raise AccountNotExist(f'account {account} not exist or invalid')
        # verify password.
        stored_password = self.stored_db.get_attr(account_ins, self.account_key)
        if not self.verify_password(stored_password, password):
            raise PasswordInvalid(f'password {password} is wrong')
        # generate token.
        raw_token_val = json.dumps({self.account_key: account})
        token = self.generate_token(raw_token_val)
        # cache redis
        if self.cache_obj:
            self.cache_obj.set(token, raw_token_val, self.cache_obj.expire)
        # first login
        first_login = self.is_first_login(account_ins)
        setattr(account_ins, 'first_login', first_login)
        if first_login:
            account_ins.update()
        setattr(account_ins, token_key, token)
        return dict(attrs(account_ins))

    @check_cls_argument(_check_account_ins, 2)
    def update_password(self, current_password: str,
                        new_password: str, account_ins: Any,
                        length_range: Optional[List[int]] = None):
        if self.verify_password(current_password, new_password):
            raise PasswordExisted(f'new_password {new_password} is same to current_password')
        if is_valid_password(new_password, length_range=length_range):
            raise PasswordFormatError(f'new_password {new_password} format is wrong.')
        account_ins.update()
