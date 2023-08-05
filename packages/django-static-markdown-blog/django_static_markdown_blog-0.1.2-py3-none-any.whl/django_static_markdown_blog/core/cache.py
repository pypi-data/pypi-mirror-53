from .exceptions import BlogCacheException
from redis import StrictRedis
from redis.exceptions import ConnectionError
from typing import Any, Type

import logging

logger = logging.getLogger(__name__)


class AbstractCache:
    """
    An abstract cache with not implemented error.
    Developers can easily add cache system by implemented those classes.
    """

    default_options = {}

    @classmethod
    def check_options(cls, options):
        """
        Check options for the init of the cache
        :param options:
        :return:
        """
        raise NotImplementedError('AbstractCache')

    def exists(self, key: str) -> bool:
        """
        Return true if the given key exists in the cache
        :param key:
        :return:
        """
        raise NotImplementedError(self.__class__.__name__)

    def get(self, key: str) -> Any:
        """
        Return data with the given key in the cache.
        It should return None or raise an Exception if the key doesn't exist
        :param key:
        :return:
        """
        raise NotImplementedError(self.__class__.__name__)

    def set(self, key: str, data: Any):
        """
        Set the given data at the given key in the cache
        :param key:
        :param article:
        :return:
        """
        raise NotImplementedError(self.__class__.__name__)

    def remove(self, key: str):
        """
        Remove data at the given key in the cache
        :param key:
        :return:
        """
        raise NotImplementedError(self.__class__.__name__)


class RedisCache(AbstractCache):

    default_options = {
        'host': 'localhost',
        'port': 6379,
        'db': 0,
        'prefix': ''
    }

    def __init__(self, options):

        self.host = options.get('host', self.default_options['host'])
        self.port = options.get('port', self.default_options['port'])
        self.db = options.get('db', self.default_options['db'])
        self.prefix = options.get('prefix', self.default_options['prefix'])

        logger.debug("RedisCache.init: host='{}', port={}, db={}, prefix='{}'".format(
            self.host, self.port, self.db, self.prefix
        ))
        self.redis = StrictRedis(host=self.host, port=self.port, db=self.db)

        try:
            self.redis.exists('null')
        except ConnectionError:
            raise BlogCacheException('Connection to redis server failed: {}:{}'.format(self.host, self.port))

    @classmethod
    def check_options(cls, options):
        if 'host' in options and not isinstance(options['host'], str):
            logger.warning("RedisCache.host must be a string.")
            return False

        if 'port' in options and not isinstance(options['port'], int):
            logger.warning("RedisCache.port must be a int.")
            return False

        if 'db' in options and not isinstance(options['db'], int):
            logger.warning("RedisCache.db must be a int.")
            return False

        if 'prefix' in options and not isinstance(options['prefix'], str):
            logger.warning("RedisCache.prefix must be a string.")
            return False

        return True

    def get_key(self, key: str) -> str:
        """
        Return correct key with prefix
        :param key:
        :return:
        """
        if key.startswith(self.prefix):
            return key
        return self.prefix + key

    def exists(self, key: str) -> bool:
        key = self.get_key(key)
        if key in self.redis:
            return True

        logger.debug("Key not found: {}".format(key))
        return False

    def get(self, key: str) -> Any:
        key = self.get_key(key)
        if self.exists(key):
            result = self.redis.get(key).decode()
            # logger.debug("Get {}".format(key))
            return result

    def set(self, key: str, data: Any):
        key = self.get_key(key)
        result = self.redis.set(key, data)
        # logger.debug("Set {}".format(key))
        return result

    def remove(self, key: str):
        key = self.get_key(key)
        if self.exists(key):
            result = self.redis.delete(key)
            # logger.debug("Delete '{}".format(key))
            return result


class CacheFactory:
    """
    Create AbstractCache object
    """
    def __contains__(self, item: str) -> bool:
        class_name = item.capitalize() + 'Cache'
        for cls in AbstractCache.__subclasses__():
            if cls.__name__ == class_name:
                return True

    def __getattr__(self, item: str) -> Type:
        class_name = item.capitalize() + 'Cache'
        for cls in AbstractCache.__subclasses__():
            if cls.__name__ == class_name:
                return cls
