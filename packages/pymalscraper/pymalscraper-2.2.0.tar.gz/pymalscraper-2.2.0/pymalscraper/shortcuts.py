import requests
import time
import sys


def get(url, headers=None, interval=2, max=999):
    """
    Custom get request. Recursively make request every designated interval.

    Args:
        url: Request needs a url.
        headers: HTTP Headers.
        interval: The delay before making requests. Default 2 seconds.
        max: Maximum number of request to be made.

    Returns:
        Return the response.
    """
    time.sleep(interval)
    res = requests.get(url, headers=headers)

    if res.status_code != 200 and max != 0:
        res = get(url, headers, interval, max - 1)

    return res
