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
    # Check if the URL is in the cache
    if url in cache:
        # If it's in the cache, return the cached content
        return cache[url]

    # If not in the cache, make an HTTP request
    response = requests.get(url)

    if response.status_code == 200:
        # If the request was successful, store the content in the cache
        cache[url] = response.text
    else:
        # Handle the case where the request was not successful
        response.raise_for_status()

    return response.text


# Function to track the number of times a URL was accessed
def track_access_count(url):
    count_key = f"count:{url}"
    access_count = cache.get(count_key, 0)
    access_count += 1
    cache[count_key] = access_count


# Decorator for tracking access count
def track_access(func):
    @wraps(func)
    def wrapper(url):
        track_access_count(url)
        return func(url)
    return wrapper


# Apply the decorator to the get_page function
get_page = track_access(get_page)

# Example usage
if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk/delay/1000/url/http://www.example.com"

    for _ in range(5):
        content = get_page(url)
        print(f"Accessed URL: {url}")

    print(f"Total access count for {url}: {cache[f'count:{url}']}")
