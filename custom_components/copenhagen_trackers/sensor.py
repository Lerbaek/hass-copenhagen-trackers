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
        
    @property 
    def entity_id(self) -> str:
        """Return entity ID."""
        return f"{Platform.SENSOR}.cphtrackers_{self._device_id}_last_seen_at"
    
    @property
    def unique_id(self):
        """Return a unique ID."""
        return f"cphtrackers_{self._device_id}_last_seen_at"

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self.device_data['name']} tracker last seen at"

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
        
    @property 
    def entity_id(self) -> str:
        """Return entity ID."""
        return f"{Platform.SENSOR}.cphtrackers_{self._device_id}_battery_percentage"
    
    @property
    def unique_id(self):
        """Return a unique ID."""
        return f"cphtrackers_{self._device_id}_battery_percentage"

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self.device_data['name']} tracker battery percentage"

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
        
    @property 
    def entity_id(self) -> str:
        """Return entity ID."""
        return f"{Platform.SENSOR}.cphtrackers_{self._device_id}_signal_strength"
    
    @property
    def unique_id(self) -> str:
        """Return a unique ID."""
        return f"cphtrackers_{self._device_id}_signal_strength"

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return f"{self.device_data['name']} tracker signal strength"

    @property
    def native_value(self) -> int | None:
        """Return the state of the sensor."""
        return int(self.device_data.get("location", {}).get("device_info", {}).get("sig_strength", 0))

class ProfileNameSensor(CopenhagenTrackersEntity, SensorEntity):
    """Sensor for device profile name."""

    _attr_icon = "mdi:card-account-details-outline"
        
    @property 
    def entity_id(self) -> str:
        """Return entity ID."""
        return f"{Platform.SENSOR}.cphtrackers_{self._device_id}_profile_name"
    
    @property
    def unique_id(self):
        """Return a unique ID."""
        return f"cphtrackers_{self._device_id}_profile_name"

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self.device_data['name']} tracker profile name"

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
        
    @property 
    def entity_id(self) -> str:
        """Return entity ID."""
        return f"{Platform.SENSOR}.cphtrackers_{self._device_id}_server_sync_at"
    
    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.coordinator.last_update_success_time