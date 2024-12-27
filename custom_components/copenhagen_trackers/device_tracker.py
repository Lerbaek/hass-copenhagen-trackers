"""Device tracker platform for Copenhagen Trackers integration."""
from homeassistant.components.device_tracker import SourceType, TrackerEntity
from .const import DOMAIN
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
    _attr_has_entity_name = True

    def __init__(self, coordinator, device_id):
        """Initialize the tracker."""
        super().__init__(coordinator, device_id)
        self._attr_unique_id = f"{device_id}_location"
        self._attr_name = "Location"

    @property
    def source_type(self):
        """Return the source type of the device."""
        return SourceType.GPS

    @property
    def latitude(self):
        """Return latitude value of the device."""
        return float(self.device_data.get("location", {}).get("details", {}).get("lat", 0))

    @property
    def longitude(self):
        """Return longitude value of the device."""
        return float(self.device_data.get("location", {}).get("details", {}).get("lon", 0))

    @property
    def location_accuracy(self):
        """Return the location accuracy of the device."""
        return float(self.device_data.get("location", {}).get("details", {}).get("acc", 0))

    @property
    def location_name(self):
        """Return the location name."""
        location = self.device_data.get("location", {})
        if road := location.get("road"):
            return f"{road}, {location.get('city', '')}, {location.get('country', '')}"
        return None