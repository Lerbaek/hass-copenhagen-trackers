"""Sensor platform for Copenhagen Trackers integration."""
from __future__ import annotations

from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.const import (
    PERCENTAGE,
    Platform
)
from homeassistant.helpers.entity import EntityCategory
import datetime

from .const import DOMAIN, ATTR_DESCRIPTION, ATTR_UPDATED_AT
from . import CopenhagenTrackersEntity

PLATFORM = Platform.SENSOR

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up Copenhagen Trackers sensors based on a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    
    entities = []
    for device in coordinator.data["data"]:
        entities.extend((
            ServerSyncAtSensor(coordinator, device["id"]),
            LastSeenAtSensor(coordinator, device["id"]),
            BatteryPercentageSensor(coordinator, device["id"]),
            SignalStrengthSensor(coordinator, device["id"]),
            ProfileNameSensor(coordinator, device["id"]),
        ))
    
    async_add_entities(entities)

class LastSeenAtSensor(CopenhagenTrackersEntity, SensorEntity):
    """Sensor for when the device was last seen."""

    _attr_device_class = SensorDeviceClass.TIMESTAMP
    _attr_icon = "mdi:clock-outline"
    PLATFORM = PLATFORM
    SUFFIX = "last_seen_at"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        last_seen_at = self.device_data.get("updated_at")
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
    PLATFORM = PLATFORM
    SUFFIX = "battery_percentage"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.device_data.get("battery_percentage")

class SignalStrengthSensor(CopenhagenTrackersEntity, SensorEntity):
    """Sensor for device signal strength."""

    _attr_device_class = SensorDeviceClass.SIGNAL_STRENGTH
    _attr_native_unit_of_measurement = None
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_icon = "mdi:signal"
    _attr_native_precision = 0
    PLATFORM = PLATFORM
    SUFFIX = "signal_strength"

    @property
    def native_value(self) -> int | None:
        """Return the state of the sensor."""
        return int(self.device_data.get("location", {}).get("device_info", {}).get("sig_strength", 0))

class ProfileNameSensor(CopenhagenTrackersEntity, SensorEntity):
    """Sensor for device profile name."""

    _attr_icon = "mdi:card-account-details-outline"
    PLATFORM = PLATFORM
    SUFFIX = "profile_name"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if profile := self.device_data.get("profile"):
            return profile.get("name")
        return None

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        if profile := self.device_data.get("profile"):
            return {
                ATTR_DESCRIPTION: profile.get("description"),
                ATTR_UPDATED_AT: profile.get("updated_at"),
            }
        return None

class ServerSyncAtSensor(CopenhagenTrackersEntity, SensorEntity):
    """Sensor for when the data was last synchronized with the server."""

    _attr_device_class = SensorDeviceClass.TIMESTAMP
    _attr_icon = "mdi:cloud-sync"
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    PLATFORM = PLATFORM
    SUFFIX = "server_sync_at"
    
    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.coordinator.last_sync_time