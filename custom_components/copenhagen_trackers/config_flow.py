
"""Config flow for Copenhagen Trackers integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN
from .api import CopenhagenTrackersAPI

_LOGGER = logging.getLogger(__name__)

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Copenhagen Trackers."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            try:
                session = async_get_clientsession(self.hass)
                api = CopenhagenTrackersAPI(
                    session,
                    user_input[CONF_EMAIL],
                    user_input[CONF_PASSWORD],
                )
                
                # Test the credentials by getting an access token
                await api.async_ensure_token()

                return self.async_create_entry(
                    title=user_input[CONF_EMAIL],
                    data=user_input,
                )
            except Exception:
                _LOGGER.exception("Failed to connect to Copenhagen Trackers")
                errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_EMAIL): str,
                    vol.Required(CONF_PASSWORD): str,
                }
            ),
            errors=errors,
        )