import requests
import time
import sys


def get(url, headers, interval=2):
    """
    Custom get request. Recursively make request every designated interval.

    Args:
        url: Request needs a url.
        headers: HTTP Headers.
        interval: The delay before making requests. Default 2 seconds.

    Returns:
        Return the response.
    """
    time.sleep(interval)
    res = requests.get(url, headers=headers)

    if res.status_code != 200:
        res = get(url, headers, interval)

    return res
