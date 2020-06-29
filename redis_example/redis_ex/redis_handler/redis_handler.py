import redis


class RedisConfigurations(object):
    """
    Preparing object of Redis and initialize with flask app.
    """

    def __init__(self, app=None, strict=True, config_prefix="REDIS", **kwargs):
        self._redis_client = None
        self.provider_class = redis.StrictRedis if strict else redis.Redis
        self.provider_kwargs = kwargs
        self.config_prefix = config_prefix

        if app is not None:
            self.init_app(app)

    @classmethod
    def from_custom_provider(cls, provider, app=None, **kwargs):
        """
        We can use different Redis Providers using this class method

        :param provider:
        :type provider:
        :param app:
        :type app:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """

        assert provider is not None, "your custom provider is None, come on"

        instance = cls(**kwargs)
        instance.provider_class = provider

        if app is not None:
            instance.init_app(app)

        return instance

    def init_app(self, app, **kwargs):

        redis_url = app.config.get("{0}_URL".format(self.config_prefix), "redis://localhost:6379/0")

        self.provider_kwargs.update(kwargs)
        self._redis_client = self.provider_class.from_url(redis_url, **self.provider_kwargs)

        if not hasattr(app, "extensions"):
            app.extensions = {}

        app.extensions[self.config_prefix.lower()] = self

    def __getattr__(self, name):
        return getattr(self._redis_client, name)

    def __getitem__(self, name):
        return self._redis_client[name]

    def __setitem__(self, name, value):
        self._redis_client[name] = value

    def __delitem__(self, name):
        del self._redis_client[name]


class RedisCacheManager(RedisConfigurations):
    """
    Redis configuration for Cache Management.
    """

    def __init__(self, app=None, strict=True, config_prefix="REDIS", **kwargs):
        super().__init__(app, strict, config_prefix, **kwargs)

    @staticmethod
    def delete_all_caches(cache_obj=None, cache_prefix=None):
        """
        Delete all or specified cache prefix keys from cache.

        :param cache_obj: cache object
        :type cache_obj: RedisConfigurations object
        :param cache_prefix: cache prefix
        :type cache_prefix: str
        :return:
        :rtype:
        """
        for key in cache_obj.scan_iter(cache_prefix):
            cache_obj.delete(key)

    @staticmethod
    def delete_cache(cache_obj=None, cache_prefix=None, cache_key=None):
        """
        Delete cached data from cache.

        Ex: -

        # Remove all caches
        cache.delete_all_caches(cache_obj=cache)

        # Remove caches with specifies cache prefix start index
        cache.delete_cache(cache_obj=cache, cache_prefix='cache_prefix')
        cache.delete_all_caches(cache_obj=cache, cache_prefix='cache_prefix')

        # Remove specific cache
        cache.delete_cache(cache_obj=cache, cache_key='cache_prefix100')

        # We can pass list, tuple or dict as cache_key
        cache.delete_cache(cache_obj=cache, cache_key=['cache_prefix12', 'cache_prefix88', 'cache_prefix120'])

        # Delete specific index and some specified caches
        cache.delete_cache(cache_obj=cache, cache_prefix='cache_prefix', cache_key='cache_prefix100')

        :param cache_obj: cache object
        :type cache_obj: RedisConfigurations object
        :param cache_prefix: cache prefix
        :type cache_prefix: str
        :param cache_key: specific key(s) to delete
        :type cache_key: str, list, tuple or dict
        :return:
        :rtype:
        """

        if cache_key:

            if isinstance(cache_key, str):
                cache_obj.delete(cache_key)

            elif isinstance(cache_key, list) or isinstance(cache_key, tuple):
                cache_obj.delete(*cache_key)

            elif isinstance(cache_key, dict):
                for key in cache_key.keys():
                    cache_obj.delete(key)

        if cache_prefix:
            for key in cache_obj.scan_iter(cache_prefix):
                cache_obj.delete(key)


class RedisQueueManager(RedisConfigurations):
    """
    TODO: Future development for Task/Queue manager with the help of Redis
    """

    def __init__(self, app=None, strict=True, config_prefix="REDIS", **kwargs):
        super().__init__(app, strict, config_prefix, **kwargs)
