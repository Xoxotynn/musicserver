from __future__ import annotations

import hashlib
import secrets

import requests

from syncworker.navidrome.data.models.navidrome_models import NavidromeApiResponse


class NavidromeClient:
    def __init__(
        self,
        base_url: str,
        user: str,
        password: str,
        session: requests.Session | None = None,
    ):
        self.base_url = base_url.rstrip("/")
        self.user = user
        self.password = password
        self.session = session or requests.Session()

    def get(self, endpoint: str, params: dict[str, str] | list[tuple[str, str]] | None = None) -> NavidromeApiResponse:
        response = self.session.get(
            f"{self.base_url}/{endpoint}.view",
            params=self._params(params),
            timeout=30,
        )
        response.raise_for_status()
        return NavidromeApiResponse(payload=response.json())

    def _params(
        self,
        params: dict[str, str] | list[tuple[str, str]] | None = None,
    ) -> list[tuple[str, str]]:
        salt = self._salt()
        api_params = [
            ("u", self.user),
            ("t", self._token(salt)),
            ("s", salt),
            ("v", "1.16.1"),
            ("c", "syncworker"),
            ("f", "json"),
        ]

        if params is None:
            return api_params

        if isinstance(params, dict):
            api_params.extend(params.items())
        else:
            api_params.extend(params)

        return api_params

    @staticmethod
    def _salt() -> str:
        return secrets.token_hex(8)

    def _token(self, salt: str) -> str:
        return hashlib.md5(f"{self.password}{salt}".encode("utf-8")).hexdigest()
