"""Device tracker platform for Copenhagen Trackers integration."""
from homeassistant.components.device_tracker import SourceType, TrackerEntity
from homeassistant.const import Platform
from .const import (
    DOMAIN,
    ATTR_LOCATION as LOCATION,
)
from . import CopenhagenTrackersEntity

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up Copenhagen Trackers device tracker based on a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    
    entities = []
    for device in coordinator.data["data"]:
        entities.append(DeviceTracker(coordinator, device["id"]))
    
    async_add_entities(entities)

class DeviceTracker(CopenhagenTrackersEntity, TrackerEntity):
    """Copenhagen Trackers Device Tracker."""

    _attr_icon = "mdi:map-marker"
    _attr_entity_category = None
    PLATFORM = Platform.DEVICE_TRACKER
    SUFFIX = LOCATION

    @property
    def source_type(self):
        """Return the source type of the device."""
        return SourceType.GPS
    
    def get_location_details(self, key: str) -> float:
        """Get a location detail"""
        return float(self.get_location.get("details", {}).get(key, 0))
    
    @property
    def location(self) -> dict:
        """Get a location detail"""
        return self.device_data.get(LOCATION, {})

    @property
    def latitude(self):
        """Return latitude value of the device."""
        return self.get_location_details("lat", 0)

    @property
    def longitude(self):
        """Return longitude value of the device."""
        return self.get_location_details("lon", 0)

    @property
    def location_accuracy(self):
        """Return the location accuracy of the device."""
        return self.get_location_details("acc", 0)

    @property
    def location_name(self):
        """Return the location name."""
        location = self.device_data.get(LOCATION, {})
        if road := location.get("road"):
            return f"{road}, {location.get('city', '')}, {location.get('country', '')}"
        return None