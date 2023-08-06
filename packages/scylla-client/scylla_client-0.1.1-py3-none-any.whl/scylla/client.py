from typing import Optional

import potion_client as potion
import requests

from .auth import HTTPJWTAuth
from .config import conf


class Client:
    def __init__(self, username: str, password: str, endpoint: Optional[str] = None, auth_path: str = "/auth") -> None:
        self._endpoint = conf.get_config("charybdis_endpoint", endpoint)
        self._username = username
        self._password = password
        self._auth_path = auth_path

        self._token = self._get_token()

        self._client = potion.Client(self._endpoint, auth=HTTPJWTAuth(self._token))

    def _get_token(self) -> str:
        payload = {"username": self._username, "password": self._password}
        response = requests.post(f"{self._endpoint}{self._auth_path}", json=payload)

        if response.status_code != 200:
            raise RuntimeError(f"Auth error with code {response.status_code} | {response.text}")

        return response.json().get("access_token")

    def __getattribute__(self, item):
        try:
            return super().__getattribute__(item)
        except AttributeError:
            return self._client.__getattribute__(item)
