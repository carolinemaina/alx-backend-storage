#!/usr/bin/env python3
import redis
import requests
from functools import wraps

# Set up the Redis client
r = redis.StrictRedis(host='localhost', port=6379, db=0)

def cache_page(func):
    """
    A decorator to cache the page content and track access count in Redis.

    Args:
        func (function): The function to wrap and decorate.

    Returns:
        function: The wrapped function with caching and access tracking.
    """
    @wraps(func)
    def wrapper(url: str) -> str:
        """
        A wrapper function to handle caching and access count in Redis.

        Args:
            url (str): The URL to fetch and cache.

        Returns:
            str: The content of the page, either from cache or fetched from the URL.
        """
        # Check if page content is already cached
        cached_content = r.get(url)
        if cached_content:
            # Increment the access count
            count_key = f"count:{url}"
            r.incr(count_key)
            return cached_content.decode('utf-8')

        # If not cached, fetch the content
        content = func(url)

        # Cache the content with an expiration time of 10 seconds
        r.setex(url, 10, content)

        # Initialize access count if not set
        count_key = f"count:{url}"
        if not r.exists(count_key):
            r.set(count_key, 0)  # Initialize the count to 0

        # Increment the access count
        r.incr(count_key)

        return content

    return wrapper

@cache_page
def get_page(url: str) -> str:
    """
    Fetches the HTML content of a URL.

    Args:
        url (str): The URL to fetch content from.

    Returns:
        str: The HTML content of the page.
    """
    response = requests.get(url)
    return response.text
