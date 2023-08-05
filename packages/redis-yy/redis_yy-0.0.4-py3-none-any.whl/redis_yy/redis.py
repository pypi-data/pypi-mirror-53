"""
Create by yy on 2019/9/27
I'm looking for a good job, can you provide for me?
Please contact me by email 1023767856@qq.com.
"""
import warnings

import redis

from .lib.tool import Tool

__all__ = ['RedisDB']


class RedisDB(object):
    """
    因为之后可能 根据业务需求，对一些方法进行代理，所以才写了这个包。
    为了拓展性，和组件化思想(对于我写的Helper这个包，
    借鉴了flask的组件化思想，进行组件化开发) 会有一个 init_db函数
    """

    def __init__(self, helper=None, is_debug=True, **kwargs):
        """
        构造函数
        :param max_conn: 最大连接数
        :param mode: 连接模式  1 为默认连接池模式, 2 为单连接模式
        :param helper:
        :param kwargs:
        """
        self.tool = Tool()
        self.redis = None
        self.host = kwargs.setdefault("host", "127.0.0.1")
        self.port = kwargs.setdefault("port", 6379)
        self.max_conn = kwargs.setdefault("max_conn", 1)
        self.password = kwargs.setdefault("password", None)
        self.mode = kwargs.setdefault("mode", 1)
        self.is_debug = is_debug
        if helper is not None:
            self.helper = helper
            self.init_helper(helper)
        else:
            self.helper = None

    def __del__(self):
        try:
            self.close()
        except:
            pass

    def init(self):
        """
        创建连接
        Create a redis connection
        :return:
        """
        if self.mode == 1:
            pool = redis.ConnectionPool(host=self.host, port=self.port, db=self.max_conn, password=self.password)
            self.redis = redis.Redis(connection_pool=pool)
        else:
            self.redis = redis.Redis(host=self.host, port=self.port, db=1, password=self.password)

    def get_redis(self):
        """
        return redis pool object
        :return:
        """
        return self.redis

    def get_config(self, config):
        """
        获取配置
        Get config from config dict.
        The config example:
            REDIS_CONFIG = {
                "USERNAME": "postgres",
                "PASSWORD": "root",
                "HOST": "127.0.0.1",
                "PORT": "5432",
                "DATABASE": "postgres",
                "TABLE_PREFIX": ""
            }
        :param config:
        :return:
        """
        self.host = self.helper.config[config].setdefault("HOST", "127.0.0.1")
        self.port = self.helper.config[config].setdefault("PORT", 6379)
        self.max_conn = self.helper.config[config].setdefault("MAX_CONN", 1)
        self.password = self.helper.config[config].setdefault("PASSWORD", None)
        self.mode = self.helper.config[config].setdefault("MODE", 1)
        self.is_debug = self.helper.config[config].setdefault("DEBUG", True)

    def __call__(self, *args, **kwargs):
        """
        :param args:
        :param kwargs:
        :return:
        """
        if len(args) < 1:
            warnings.warn('Please give a config name.')
            return self
        return self.init_db(config=args[0])

    def init_db(self, config):
        """
        If you want to use this method,
        you must call function init_helper,
        otherwise it will give a warning.
        :param config:
        :return:
        """
        if self.helper is None:
            warnings.warn('Please call function init_helper first.')
            return None
        if config not in self.helper.config:
            warnings.warn('Please set redis connect info.')
            return None
        self.get_config(config)
        self.init()
        return self

    def init_helper(self, helper, init_config=True):
        """This callback can be used to initialize an Helper application for the
        use with this database setup.  Never use a database in the context
        of an application not initialized that way or connections will
        leak.
        """
        self.helper = helper
        default_config = 'REDIS_CONF'
        if init_config:
            if default_config not in helper.config:
                warnings.warn('Please set redis connect info.')
                return self
            self.get_config(default_config)
        helper.redis = self

    def close(self):
        """
        关闭数据库
        Close the redis connection
        :return:
        """
        self.redis.close()

    def set(self, name, value, ex=None, px=None, nx=False, xx=False):
        """
        设置给定key的值
        Set key's value
        :param name:
        :param value:
        :param ex:
        :param px:
        :param nx:
        :param xx:
        :return:
        """
        return self.redis.set(name, value, ex, px, nx, xx)

    def get(self, key=None, encode="utf-8"):
        """
        获取对应键的值
        Get value
        :param encode:
        :param key:
        :return:
        """
        if key is None:
            self.tool.debug("Please give a key which you want to search.")
            return
        try:
            data = self.redis.get(key).decode(encode)
        except Exception as e:
            data = None
            if self.is_debug:
                self.tool.debug("Get key's value is error: ".format(error=e))
        return data
