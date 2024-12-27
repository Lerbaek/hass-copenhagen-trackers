"""Copenhagen Trackers integration for Home Assistant."""
from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone
from abc import abstractmethod
import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_EMAIL,
    CONF_PASSWORD,
    Platform,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.entity import generate_entity_id
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import (
    DOMAIN,
    CONF_ACCESS_TOKEN,
    DEFAULT_SCAN_INTERVAL,
    API_ENDPOINT,
)
from .api import CopenhagenTrackersAPI

DEVICE_TYPE_MAP = {
    1: "Cobblestone",
    2: "Gemstone"
}

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
    Platform.SWITCH,
    Platform.DEVICE_TRACKER
]

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_EMAIL): cv.string,
                vol.Required(CONF_PASSWORD): cv.string,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)

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
        name="Copenhagen Trackers",
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

class CopenhagenTrackersDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Copenhagen Trackers data."""

    def __init__(
        self,
        hass: HomeAssistant,
        logger: logging.Logger,
        api: CopenhagenTrackersAPI,
        name: str,
        update_interval: timedelta,
    ) -> None:
        """Initialize."""
        super().__init__(
            hass,
            logger,
            name=name,
            update_interval=update_interval,
        )
        self.api = api
        self._last_sync_time = None

    async def _async_update_data(self):
        """Update data via library."""
        try:
            data = await self.api.async_get_devices()
            self._last_sync_time = datetime.now(timezone.utc)
            return data
        except Exception as exception:
            raise UpdateFailed(exception) from exception

    @property
    def last_sync_time(self) -> datetime.datetime:
        """Return the timestamp of the last successful sync."""
        return self._last_sync_time
    
class CopenhagenTrackersEntity(CoordinatorEntity):
    """Defines a base Copenhagen Trackers entity."""

    def __init__(
        self,
        coordinator: CopenhagenTrackersDataUpdateCoordinator,
        device_id: str,
    ) -> None:
        """Initialize the entity."""
        super().__init__(coordinator)
        self._device_id = device_id
        self.entity_id = generate_entity_id(
            f"{self.PLATFORM}.cphtrackers_" + "{}_" + self.SUFFIX,
            self.device_data["name"],
            hass=coordinator.hass)
        device_type = self.device_data['device_type']
        model = DEVICE_TYPE_MAP.get(device_type, f"Unknown model ({device_type})")
        self._attr_device_info = {
            "identifiers": {(DOMAIN, device_id)},
            "name": self.device_data["name"],
            "manufacturer": "Copenhagen Trackers",
            "model": model,
            "sw_version": self.device_data["firmware_version"],
        }
        
    @property
    @abstractmethod
    def SUFFIX(self):
        """Return the suffix of the entity."""

    @property
    @abstractmethod
    def PLATFORM(self):
        """Return the platform of the entity."""
    
    @property
    def unique_id(self):
        """Return a unique ID."""
        return f"cphtrackers_{self._device_id}_{self.SUFFIX}"

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self.device_data['name']} tracker {self.SUFFIX.replace('_', ' ')}"

    @property
    def device_data(self):
        """Return device data."""
        return next(
            device for device in self.coordinator.data["data"]
            if device["id"] == self._device_id
        )