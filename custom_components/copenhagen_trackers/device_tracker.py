"""Device tracker platform for Copenhagen Trackers integration."""

from homeassistant.components.device_tracker import SourceType, TrackerEntity

from .const import (
    DOMAIN,
    ATTR_DATA,
    ATTR_ID
)
from .entity import CopenhagenTrackersEntity

# API response keys
ATTR_ACCURACY = "acc"
ATTR_CITY = "city"
ATTR_COUNTRY = "country"
ATTR_DETAILS = "details"
ATTR_LATITUDE = "lat"
ATTR_LONGITUDE = "lon"
ATTR_ROAD = "road"

# Entities
SUFFIX_LOCATION = "location"
TRANSLATION_KEY_LOCATION = SUFFIX_LOCATION

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up Copenhagen Trackers device tracker based on a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    entities = []
    for device in coordinator.data[ATTR_DATA]:
        entities.append(DeviceTracker(coordinator, device[ATTR_ID]))

    async_add_entities(entities)


class DeviceTracker(CopenhagenTrackersEntity, TrackerEntity):
    """Copenhagen Trackers Device Tracker."""

    _attr_icon = "mdi:map-marker"
    _attr_entity_category = None
    _attr_translation_key = TRANSLATION_KEY_LOCATION
    SUFFIX = SUFFIX_LOCATION

    @property
    def source_type(self):
        """Return the source type of the device."""
        return SourceType.GPS
    
    def get_location_details(self, key: str) -> float:
        """Get a location detail"""
        return float(self.get_location().get(ATTR_DETAILS, {}).get(key))

    @property
    def latitude(self) -> float:
        """Return latitude value of the device."""
        return self.get_location_details(ATTR_LATITUDE)

    @property
    def longitude(self) -> float:
        """Return longitude value of the device."""
        return self.get_location_details(ATTR_LONGITUDE)

    @property
    def location_accuracy(self) -> float:
        """Return the location accuracy of the device."""
        return self.get_location_details(ATTR_ACCURACY) * 10

    @property
    def location_name(self) -> str:
        """Return the location name."""
        location = self.get_location()
        location_parts = [
            part
            for part in [location.get(ATTR_ROAD), location.get(ATTR_CITY), location.get(ATTR_COUNTRY)]
            if part
        ]
        return ", ".join(location_parts) if location_parts else None
