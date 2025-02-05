"""API for AIFA."""

import logging

from aiohttp import ClientSession

from .const import (
    API_CLIENT_ID,
    API_GRANT_TYPE_REFRESH_TOKEN,
    API_URL_DEVICE,
    API_URL_TOKEN,
    API_USER_AGENT,
    CONF_ACCESS_TOKEN,
    CONF_REFRESH_TOKEN,
    AIFAAPIDevice,
    AIFAAPIDevices,
    AIFAAPIToken,
)

_LOGGER = logging.getLogger(__name__)


class AIFAAPIClient:
    """API client for AIFA."""

    def __init__(self, session: ClientSession) -> None:
        """Initialize."""
        self.session = session

    async def get_device(self, access_token: str) -> AIFAAPIDevice:
        """Get devices."""
        _LOGGER.info(access_token)
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "User-Agent": API_USER_AGENT,
        }
        response = await self.session.get(API_URL_DEVICE, headers=headers)
        result: AIFAAPIDevices = await response.json()
        _LOGGER.info(result)
        device: AIFAAPIDevice = result["devices"][0]
        return device

    async def refresh(self, refresh_token: str) -> dict:
        """Refresh tokens."""
        headers = {
            "Content-Type": "application/json",
            "User-Agent": API_USER_AGENT,
        }
        response = await self.session.post(
            API_URL_TOKEN,
            json={
                "grant_type": API_GRANT_TYPE_REFRESH_TOKEN,
                "client_id": API_CLIENT_ID,
                "refresh_token": refresh_token,
            },
            headers=headers,
        )
        result: AIFAAPIToken = await response.json()
        return {
            "access_token": result[CONF_ACCESS_TOKEN],
            "refresh_token": result[CONF_REFRESH_TOKEN],
        }
