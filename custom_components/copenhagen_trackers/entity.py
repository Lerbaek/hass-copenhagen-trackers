"""Entity base for Copenhagen Trackers integration."""

from __future__ import annotations
from abc import abstractmethod

from homeassistant.helpers.entity import generate_entity_id
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    BRAND,
    DOMAIN,
    ATTR_DATA,
    ATTR_ID
)
from .coordinator import CopenhagenTrackersDataUpdateCoordinator
    
class CopenhagenTrackersEntity(CoordinatorEntity):
    """Defines a base Copenhagen Trackers entity."""

    DEVICE_TYPE_MAP = {
        1: "Cobblestone",
        2: "Gemstone"
    }

    # API response keys
    DEVICE_TYPE = "device_type"
    FIRMWARE_VERSION = "firmware_version"
    LOCATION = "location"
    NAME = "name"

    # Entity IDs
    PREFIX = "cphtrackers"

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: CopenhagenTrackersDataUpdateCoordinator,
        device_id: str,
    ) -> None:
        """Initialize the entity."""
        super().__init__(coordinator)
        self._device_id = device_id

        self.entity_id = generate_entity_id(
            f"{DOMAIN}.{self.PREFIX}_" + "{}_" + self.SUFFIX,
            self.device_data[self.NAME],
            hass=coordinator.hass)
        
        device_type = self.device_data[self.DEVICE_TYPE]
        model = self.DEVICE_TYPE_MAP.get(device_type, f"Unknown model ({device_type})")
        self._attr_device_info = {
            "identifiers": {(DOMAIN, device_id)},
            "name": f"{self.device_data[self.NAME]} Tracker",
            "manufacturer": BRAND,
            "model": model,
            "sw_version": self.device_data[self.FIRMWARE_VERSION],
        }

    def get_location(self) -> dict | None:
        """Get a location detail"""
        if device_data := self.device_data:
            if location := device_data.get(self.LOCATION):
                return location
        return None
        
    @property
    @abstractmethod
    def SUFFIX(self):
        """Return the suffix of the entity."""
    
    @property
    def unique_id(self):
        """Return a unique ID."""
        return f"{self.PREFIX}_{self._device_id}_{self.SUFFIX}"

    @property
    def device_data(self):
        """Return device data."""
        return next(
            device for device in self.coordinator.data[ATTR_DATA]
            if device[ATTR_ID] == self._device_id
        )