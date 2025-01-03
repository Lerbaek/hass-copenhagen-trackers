"""Binary sensor platform for Copenhagen Trackers integration."""

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorDeviceClass,
)
from homeassistant.helpers.entity import EntityCategory

from .const import (
    DOMAIN,
    ATTR_DATA as ATTR_DATA,
    ATTR_ID as ATTR_ID
)
from .entity import CopenhagenTrackersEntity

# API response keys
ATTR_CAN_UPDATE = "can_update"
ATTR_SHOULD_UPDATE = "should_update"

# Entities
SUFFIX_CAN_UPDATE = ATTR_CAN_UPDATE
SUFFIX_SHOULD_UPDATE = ATTR_SHOULD_UPDATE
TRANSLATION_KEY_CAN_UPDATE = ATTR_CAN_UPDATE
TRANSLATION_KEY_SHOULD_UPDATE = ATTR_SHOULD_UPDATE

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up Copenhagen Trackers binary sensors based on a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    
    entities = []
    for device in coordinator.data[ATTR_DATA]:
        entities.extend((
            CanUpdateBinarySensor(coordinator, device[ATTR_ID]),
            ShouldUpdateBinarySensor(coordinator, device[ATTR_ID]),
        ))
    
    async_add_entities(entities)

class CanUpdateBinarySensor(CopenhagenTrackersEntity, BinarySensorEntity):
    """Binary sensor for device update capability."""

    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_icon = "mdi:cloud-download"
    _attr_device_class = BinarySensorDeviceClass.UPDATE
    _attr_translation_key = TRANSLATION_KEY_CAN_UPDATE
    SUFFIX = SUFFIX_CAN_UPDATE

    @property
    def is_on(self):
        """Return true if the binary sensor is on."""
        return bool(self.device_data.get(ATTR_CAN_UPDATE, False))

class ShouldUpdateBinarySensor(CopenhagenTrackersEntity, BinarySensorEntity):
    """Binary sensor for device update recommendation."""

    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_icon = "mdi:cloud-alert"
    _attr_device_class = BinarySensorDeviceClass.UPDATE
    _attr_translation_key = TRANSLATION_KEY_SHOULD_UPDATE
    SUFFIX = SUFFIX_SHOULD_UPDATE

    @property
    def is_on(self):
        """Return true if the binary sensor is on."""
        return bool(self.device_data.get(ATTR_SHOULD_UPDATE, False))