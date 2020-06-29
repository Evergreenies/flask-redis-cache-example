from flask import Response

from redis_ex import app, cache


@app.route('/', methods=['GET', 'POST'])
def set_temp_caches():
    """
    Set caches in bulk for testing purpose.

    :return:
    :rtype:
    """
    [cache.set(
        'cache_prefix' + str(key),
        value,
        ex=app.config.get('CACHE_EXPIRE_TIME', 60)  # Cache Expire time (Optional)
    ) for key, value in list(map(lambda x: (x, x), range(10, 100)))]
    return Response('set_temp_caches')


@app.route('/remove-cache', methods=['GET', 'POST'])
def remove_caches():
    """
    Remove caches.

    :return:
    :rtype:
    """

    # Count number of keys exist in cache
    print('Keys exist in cache: ', cache.dbsize())

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

    # Count number of keys exist in cache
    print('Keys exist in cache: ', cache.dbsize())

    return Response('remove_caches')


@app.route('/exist-caches', methods=['GET', 'POST'])
def check_caches():
    # Count number of keys exist in cache
    print('Keys exist in cache: ', cache.dbsize())

    for key in cache.scan_iter():
        print(key)

    return Response(str(cache.dbsize()))
