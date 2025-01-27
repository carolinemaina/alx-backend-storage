#!/usr/bin/env python3
'''A module with tools for request caching and tracking.
'''

import redis
import requests
from functools import wraps
from typing import Callable


redis_store = redis.Redis()
'''The module-level Redis instance.
'''


def data_cacher(method: Callable) -> Callable:
    '''Caches the output of fetched data and tracks the access count.
    '''
    @wraps(method)
    def invoker(url: str) -> str:
        '''The wrapper function for caching the output and incrementing access count.
        '''
        # Increment the access count for this URL
        redis_store.incr(f'count:{url}')
        
        # Try to fetch the cached result
        result = redis_store.get(f'result:{url}')
        
        # If result is cached, return it
        if result:
            return result.decode('utf-8')
        
        # If no cached result, fetch it using the method
        result = method(url)
        
        # Cache the result with an expiration time of 10 seconds
        redis_store.setex(f'result:{url}', 10, result)
        
        return result

    return invoker


@data_cacher
def get_page(url: str) -> str:
    '''Returns the content of a URL after caching the request's response,
    and tracking the request.
    '''
    response = requests.get(url)
    return response.text

