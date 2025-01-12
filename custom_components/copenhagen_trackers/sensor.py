"""Sensor platform for Copenhagen Trackers integration."""

from __future__ import annotations
import datetime

from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.const import PERCENTAGE
from homeassistant.helpers.entity import EntityCategory

from .const import (
    DOMAIN,
    ATTR_DATA,
    ATTR_ID
)
from .entity import CopenhagenTrackersEntity
 
# API response keys
ATTR_BATTERY_PERCENTAGE = "battery_percentage"
ATTR_DESCRIPTION = "description"
ATTR_DEVICE_INFO = "device_info"
ATTR_NAME = "name"
ATTR_PROFILE = "profile"
ATTR_SIGNAL_STRENGTH = "sig_strength"
ATTR_UPDATED_AT = "updated_at"

# Entity IDs
SUFFIX_BATTERY_PERCENTAGE = ATTR_BATTERY_PERCENTAGE
SUFFIX_LAST_SEEN_AT = "last_seen_at"
SUFFIX_PROFILE = ATTR_PROFILE
SUFFIX_SERVER_SYNC_AT = "server_sync_at"
SUFFIX_SIGNAL_STRENGTH = "signal_strength"

TRANSLATION_KEY_BATTERY_PERCENTAGE = ATTR_BATTERY_PERCENTAGE
TRANSLATION_KEY_LAST_SEEN_AT = SUFFIX_LAST_SEEN_AT
TRANSLATION_KEY_PROFILE = ATTR_PROFILE
TRANSLATION_KEY_SERVER_SYNC_AT = SUFFIX_SERVER_SYNC_AT
TRANSLATION_KEY_SIGNAL_STRENGTH = SUFFIX_SIGNAL_STRENGTH

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up Copenhagen Trackers sensors based on a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    
    entities = []
    for device in coordinator.data[ATTR_DATA]:
        entities.extend((
            ServerSyncAtSensor(coordinator, device[ATTR_ID]),
            LastSeenAtSensor(coordinator, device[ATTR_ID]),
            BatteryPercentageSensor(coordinator, device[ATTR_ID]),
            SignalStrengthSensor(coordinator, device[ATTR_ID]),
            ProfileNameSensor(coordinator, device[ATTR_ID]),
        ))
    
    async_add_entities(entities)

class LastSeenAtSensor(CopenhagenTrackersEntity, SensorEntity):
    """Sensor for when the device was last seen."""

    _attr_device_class = SensorDeviceClass.TIMESTAMP
    _attr_icon = "mdi:broadcast"
    _attr_translation_key = TRANSLATION_KEY_LAST_SEEN_AT
    SUFFIX = SUFFIX_LAST_SEEN_AT

    @property
    def native_value(self):
        """Return the state of the sensor."""
        last_seen_at = self.device_data.get(ATTR_UPDATED_AT)
        if last_seen_at:
            return datetime.datetime.fromisoformat(last_seen_at.replace("Z", "+00:00"))
        return None

class BatteryPercentageSensor(CopenhagenTrackersEntity, SensorEntity):
    """Sensor for device battery percentage."""

    _attr_device_class = SensorDeviceClass.BATTERY
    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_native_precision = 0
    _attr_translation_key = TRANSLATION_KEY_BATTERY_PERCENTAGE
    SUFFIX = SUFFIX_BATTERY_PERCENTAGE

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.device_data.get(ATTR_BATTERY_PERCENTAGE)

class SignalStrengthSensor(CopenhagenTrackersEntity, SensorEntity):
    """Sensor for device signal strength."""

    _attr_device_class = SensorDeviceClass.SIGNAL_STRENGTH
    _attr_native_unit_of_measurement = None
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_icon = "mdi:signal"
    _attr_native_precision = 0
    _attr_translation_key = TRANSLATION_KEY_SIGNAL_STRENGTH
    SUFFIX = SUFFIX_SIGNAL_STRENGTH

    @property
    def native_value(self) -> int | None:
        """Return the state of the sensor."""
        if location := self.get_location():
            if device_info := location.get(ATTR_DEVICE_INFO):
                if signal_strength := device_info.get(ATTR_SIGNAL_STRENGTH):
                    return int(signal_strength)
        return None

class ProfileNameSensor(CopenhagenTrackersEntity, SensorEntity):
    """Sensor for device profile name."""

    _attr_icon = "mdi:card-account-details-outline"
    _attr_translation_key = TRANSLATION_KEY_PROFILE
    SUFFIX = SUFFIX_PROFILE

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if profile := self.device_data.get(ATTR_PROFILE):
            return profile.get(ATTR_NAME)
        return None

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        if profile := self.device_data.get(ATTR_PROFILE):
            return {
                ATTR_DESCRIPTION: profile.get(ATTR_DESCRIPTION),
                ATTR_UPDATED_AT: profile.get(ATTR_UPDATED_AT),
            }
        return None

class ServerSyncAtSensor(CopenhagenTrackersEntity, SensorEntity):
    """Sensor for when the data was last synchronized with the server."""

    _attr_device_class = SensorDeviceClass.TIMESTAMP
    _attr_icon = "mdi:cloud-sync"
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    SUFFIX = SUFFIX_SERVER_SYNC_AT
    _attr_translation_key = TRANSLATION_KEY_SERVER_SYNC_AT
    
    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.coordinator.last_sync_time