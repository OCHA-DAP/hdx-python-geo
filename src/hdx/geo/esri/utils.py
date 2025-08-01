from urllib.parse import urlparse

from httpx import Client, Response
from tenacity import retry, stop_after_attempt, wait_fixed

from ..config import ATTEMPT, TIMEOUT, WAIT


@retry(stop=stop_after_attempt(ATTEMPT), wait=wait_fixed(WAIT))
def client_get(url: str, params: dict | None = None) -> Response:
    """HTTP GET with retries, waiting, and longer timeouts."""
    with Client(http2=True, timeout=TIMEOUT) as client:
        return client.get(url, params=params)


def generate_token(url: str, username: str, password: str) -> str:
    """Generate a token for ArcGIS Server."""
    o = urlparse(url)
    auth_url = f"{o.scheme}://{o.netloc}/portal/sharing/rest/generateToken"
    referer = f"{o.scheme}://{o.netloc}/portal"
    data = {"f": "json", "password": password, "referer": referer, "username": username}
    with Client(http2=True) as client:
        return client.post(auth_url, data=data).json()["token"]
