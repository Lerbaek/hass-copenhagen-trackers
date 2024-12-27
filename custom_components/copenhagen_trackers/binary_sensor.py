"""Binary sensor platform for Copenhagen Trackers integration."""
from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorDeviceClass,
)
from homeassistant.helpers.entity import EntityCategory
from homeassistant.const import Platform
from .const import DOMAIN
from . import CopenhagenTrackersEntity

PLATFORM = Platform.BINARY_SENSOR

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up Copenhagen Trackers binary sensors based on a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    
    entities = []
    for device in coordinator.data["data"]:
        entities.extend((
            CanUpdateBinarySensor(coordinator, device["id"]),
            ShouldUpdateBinarySensor(coordinator, device["id"]),
        ))
    
    async_add_entities(entities)

class CanUpdateBinarySensor(CopenhagenTrackersEntity, BinarySensorEntity):
    """Binary sensor for device update capability."""

    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_icon = "mdi:cloud-download"
    _attr_device_class = BinarySensorDeviceClass.UPDATE
    PLATFORM = PLATFORM
    SUFFIX = "can_update"

    @property
    def is_on(self):
        """Return true if the binary sensor is on."""
        return bool(self.device_data.get("can_update", False))

class ShouldUpdateBinarySensor(CopenhagenTrackersEntity, BinarySensorEntity):
    """Binary sensor for device update recommendation."""

    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_icon = "mdi:update-alert"
    _attr_device_class = BinarySensorDeviceClass.UPDATE
    PLATFORM = PLATFORM
    SUFFIX = "should_update"

    @property
    def is_on(self):
        """Return true if the binary sensor is on."""
        return bool(self.device_data.get("should_update", False))