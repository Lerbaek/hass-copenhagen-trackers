"""Binary sensor platform for Copenhagen Trackers integration."""
from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorDeviceClass,
)
from homeassistant.const import Platform
from homeassistant.helpers.entity import EntityCategory

from .const import DOMAIN
from . import CopenhagenTrackersEntity

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
        
    @property 
    def entity_id(self) -> str:
        """Return entity ID."""
        return f"{Platform.BINARY_SENSOR}.cphtrackers_{self._device_id}_can_update"
    
    @property
    def unique_id(self):
        """Return a unique ID."""
        return f"cphtrackers_{self._device_id}_can_update"

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self.device_data['name']} tracker can update"

    @property
    def is_on(self):
        """Return true if the binary sensor is on."""
        return bool(self.device_data.get("can_update", False))

class ShouldUpdateBinarySensor(CopenhagenTrackersEntity, BinarySensorEntity):
    """Binary sensor for device update recommendation."""

    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_icon = "mdi:update-alert"
    _attr_device_class = BinarySensorDeviceClass.UPDATE
        
    @property 
    def entity_id(self) -> str:
        """Return entity ID."""
        return f"{Platform.BINARY_SENSOR}.cphtrackers_{self._device_id}_should_update"
    
    @property
    def unique_id(self):
        """Return a unique ID."""
        return f"cphtrackers_{self._device_id}_should_update"

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self.device_data['name']} tracker should update"

    @property
    def is_on(self):
        """Return true if the binary sensor is on."""
        return bool(self.device_data.get("should_update", False))