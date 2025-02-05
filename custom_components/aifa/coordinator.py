"""Coordinator for AIFA."""

from datetime import datetime, timedelta
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .api import AIFAAPIClient
from .const import (
    CONF_ACCESS_TOKEN,
    CONF_REFRESH_TOKEN,
    DOMAIN,
    MANUFACTURER,
    REFRESH_INTERVAL,
    UPDATE_INTERVAL,
    AIFAAPIDevice,
)

_LOGGER = logging.getLogger(__name__)


class AIFACoordinator(DataUpdateCoordinator[AIFAAPIDevice]):
    """Class to manage fetching AIFA data."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=UPDATE_INTERVAL),
        )
        self.api = AIFAAPIClient(
            session=async_get_clientsession(hass),
        )
        self.device_id = entry.unique_id
        self.device_info = DeviceInfo(
            manufacturer=MANUFACTURER,
            identifiers={(DOMAIN, self.device_id)},
        )
        self.entry = entry
        self.last_refresh = datetime.timestamp(datetime.now())
        self.hass = hass

    async def _async_setup(self) -> None:
        """Set up the coordinator."""

    async def _async_update_data(self) -> dict:
        # """Update data via library."""
        now = datetime.timestamp(datetime.now())
        if now - self.last_refresh > REFRESH_INTERVAL:
            tokens = await self.api.refresh(
                refresh_token=self.entry.data[CONF_REFRESH_TOKEN]
            )
            self.hass.config_entries.async_update_entry(
                entry=self.entry,
                data={
                    CONF_ACCESS_TOKEN: tokens[CONF_ACCESS_TOKEN],
                    CONF_REFRESH_TOKEN: tokens[CONF_REFRESH_TOKEN],
                },
            )
            self.last_refresh = now
        device: AIFAAPIDevice = await self.api.get_device(
            access_token=self.entry.data[CONF_ACCESS_TOKEN]
        )
        self.device_info.update(
            DeviceInfo(
                name=device["name"],
            )
        )
        return {
            "temperature": device["sensors"]["temperature"],
            "humidity": device["sensors"]["humidity"],
        }
