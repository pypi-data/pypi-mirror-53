import requests
import time


def get(url, headers=None):
    """
    Custom get request.

    Args:
        url: Request needs a url.

    Returns:
        Return the response.
    """
    res = requests.get(url, headers=headers)
    request_count = 0

    while res.status_code != 200 and request_count <= 10:
        time.sleep(1.5)
        res = requests.get(url, headers=headers)
        request_count += 1

    return res
