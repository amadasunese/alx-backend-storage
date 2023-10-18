#!/usr/bin/env python3
"""
Caching request module
"""
import requests
from cachetools import TTLCache
from functools import wraps

# Create a cache with a TTL of 10 seconds
cache = TTLCache(maxsize=100, ttl=10)


def get_page(url: str) -> str:
    """
    Return the cached content
    """
    if url in cache:
        return cache[url]

    response = requests.get(url)

    if response.status_code == 200:
        cache[url] = response.text
    else:
        response.raise_for_status()

    return response.text


def track_access_count(url):
    count_key = f"count:{url}"
    access_count = cache.get(count_key, 0)
    access_count += 1
    cache[count_key] = access_count


def track_access(func):
    @wraps(func)
    def wrapper(url):
        track_access_count(url)
        return func(url)
    return wrapper


get_page = track_access(get_page)

