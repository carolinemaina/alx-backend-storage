#!/usr/bin/env python3
'''A module with tools for request caching and tracking.
'''
import redis
import requests
from functools import wraps


r = redis.StrictRedis(host='localhost', port=6379, db=0)
'''The module-level Redis instance.
'''


def cache_page(func):
    '''
    A decorator to cache the page content and track access count in Redis.

    Args:
        func (function): The function to wrap and decorate.

    Returns:
        function: The wrapped function with caching and access tracking.
    '''
    @wraps(func)
    def wrapper(url: str) -> str:
        '''
        A wrapper function to handle caching and access count in Redis.

        Args:
            url (str): The URL to fetch and cache.

        Returns:
            str: The content of the page.
        '''
        cached_content = r.get(url)
        if cached_content:
            count_key = f"count:{url}"
            r.incr(count_key)
            return cached_content.decode('utf-8')

        content = func(url)

        r.setex(url, 10, content)

        count_key = f"count:{url}"
        if not r.exists(count_key):
            r.set(count_key, 0)

        r.incr(count_key)

        return content

    return wrapper


@cache_page
def get_page(url: str) -> str:
    '''
    Fetches the HTML content of a URL.

    Args:
        url (str): The URL to fetch content from.

    Returns:
        str: The HTML content of the page.
    '''
    response = requests.get(url)
    return response.text
