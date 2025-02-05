"""Config flow for AIFA."""

import logging
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession
import homeassistant.helpers.config_validation as cv

from .api import AIFAAPIClient
from .const import CONF_ACCESS_TOKEN, CONF_REFRESH_TOKEN, DOMAIN

_LOGGER = logging.getLogger(__name__)

INPUT_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_ACCESS_TOKEN): cv.string,
        vol.Required(CONF_REFRESH_TOKEN): cv.string,
    }
)


class AIFAConfigFlow(ConfigFlow, domain=DOMAIN):
    """AIFA Custom config flow."""

    data: dict[str, Any] | None

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Invoke when a user initiates a flow via the user interface."""
        errors: dict[str, str] = {}
        if user_input is None:
            return self.async_show_form(
                step_id="user", data_schema=INPUT_SCHEMA, errors=errors
            )
        api = AIFAAPIClient(
            session=async_get_clientsession(self.hass),
        )
        self.data = user_input
        device = await api.get_device(access_token=user_input[CONF_ACCESS_TOKEN])
        _LOGGER.info(device)
        return self.async_create_entry(title=device["name"], data=self.data)
