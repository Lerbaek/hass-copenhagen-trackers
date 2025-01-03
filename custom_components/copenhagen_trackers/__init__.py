"""Copenhagen Trackers integration for Home Assistant."""

from __future__ import annotations
from datetime import timedelta
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_EMAIL,
    CONF_PASSWORD,
    Platform,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import CopenhagenTrackersAPI
from .const import (
    BRAND,
    DOMAIN,
    CONF_ACCESS_TOKEN,
)
from .coordinator import CopenhagenTrackersDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
    Platform.SWITCH,
    Platform.DEVICE_TRACKER
]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Copenhagen Trackers from a config entry."""
    session = async_get_clientsession(hass)
    
    api = CopenhagenTrackersAPI(
        session,
        entry.data[CONF_EMAIL],
        entry.data[CONF_PASSWORD],
        entry.data.get(CONF_ACCESS_TOKEN),
    )

    coordinator = CopenhagenTrackersDataUpdateCoordinator(
        hass,
        _LOGGER,
        api,
        name=BRAND,
        update_interval=timedelta(hours=1),
    )

    await coordinator.async_config_entry_first_refresh()
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok