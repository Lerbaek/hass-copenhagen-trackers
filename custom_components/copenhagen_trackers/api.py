"""API Client for Copenhagen Trackers."""

import aiohttp

from typing import Any, Dict, Optional

from .const import (
    API_ENDPOINT,
    CONF_ACCESS_TOKEN
)

class CopenhagenTrackersAPI:
    """Copenhagen Trackers API client."""

    def __init__(
        self,
        session: aiohttp.ClientSession,
        email: str,
        password: str,
        access_token: Optional[str] = None,
    ) -> None:
        """Initialize."""
        self._session = session
        self._email = email
        self._password = password
        self._access_token = access_token

    async def _async_fetch_access_token(self):
        """Get access token."""
        response = await self._session.post(
            f"{API_ENDPOINT}/login",
            json={"email": self._email, "password": self._password},
        )
        response.raise_for_status()
        data = await response.json()
        self._access_token = data[CONF_ACCESS_TOKEN]

    async def async_ensure_token(self) -> None:
        """Ensure a valid access token exists."""
        if not self._access_token:
            await self._async_fetch_access_token()

    async def async_get_devices_with_auth(self) -> Dict[str, Any]:
        """Get devices data."""
        await self.async_ensure_token()
        
        try:
            return await self._async_get_devices()
        except aiohttp.ClientResponseError as error:
            if error.status in (401, 403):
                # Token invalid/expired, get a new one and retry
                await self._async_fetch_access_token()
                return await self._async_get_devices()
            raise
    
    async def _async_get_devices(self) -> Dict[str, Any]:
        """Get devices data."""
        response = await self._session.get(
            f"{API_ENDPOINT}/devices",
            headers={"Authorization": f"Bearer {self._access_token}"},
        )
        response.raise_for_status()
        return await response.json()