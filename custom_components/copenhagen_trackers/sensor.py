
"""Sensor platform for Copenhagen Trackers integration."""
from __future__ import annotations

from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.const import (
    PERCENTAGE,
    SIGNAL_STRENGTH_DECIBELS,
)
from homeassistant.helpers.entity import EntityCategory

from .const import DOMAIN, ATTR_DESCRIPTION, ATTR_UPDATED_AT
from . import CopenhagenTrackersEntity

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up Copenhagen Trackers sensors based on a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    
    entities = []
    for device in coordinator.data["data"]:
        entities.extend((
            LocationSensor(coordinator, device["id"]),
            GeoLocationSensor(coordinator, device["id"]),
            UpdatedAtSensor(coordinator, device["id"]),
            BatteryPercentageSensor(coordinator, device["id"]),
            SignalStrengthSensor(coordinator, device["id"]),
            ProfileNameSensor(coordinator, device["id"]),
        ))
    
    async_add_entities(entities)

class LocationSensor(CopenhagenTrackersEntity, SensorEntity):
    """Sensor for device location."""

    _attr_icon = "mdi:map-marker"
    
    @property
    def unique_id(self):
        """Return a unique ID."""
        return f"{self._device_id}_location"

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self.device_data['name']} location"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        location = self.device_data.get("location", {})
        if road := location.get("road"):
            return f"{road}, {location.get('city', '')}, {location.get('country', '')}"
        return None

class GeoLocationSensor(CopenhagenTrackersEntity, SensorEntity):
    """Sensor for device geolocation."""

    _attr_icon = "mdi:crosshairs-gps"
    
    @property
    def unique_id(self):
        """Return a unique ID."""
        return f"{self._device_id}_geolocation"

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self.device_data['name']} geolocation"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        location = self.device_data.get("location", {}).get("details", {})
        if lat := location.get("lat"):
            return f"{lat},{location.get('lon', '')}"
        return None

class UpdatedAtSensor(CopenhagenTrackersEntity, SensorEntity):
    """Sensor for device last update time."""

    _attr_device_class = SensorDeviceClass.TIMESTAMP
    _attr_icon = "mdi:clock-outline"
    
    @property
    def unique_id(self):
        """Return a unique ID."""
        return f"{self._device_id}_updated_at"

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self.device_data['name']} updated at"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.device_data.get("updated_at")

class BatteryPercentageSensor(CopenhagenTrackersEntity, SensorEntity):
    """Sensor for device battery percentage."""

    _attr_device_class = SensorDeviceClass.BATTERY
    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    
    @property
    def unique_id(self):
        """Return a unique ID."""
        return f"{self._device_id}_battery_percentage"

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self.device_data['name']} battery percentage"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.device_data.get("battery_percentage")

class SignalStrengthSensor(CopenhagenTrackersEntity, SensorEntity):
    """Sensor for device signal strength."""

    _attr_device_class = SensorDeviceClass.SIGNAL_STRENGTH
    _attr_native_unit_of_measurement = SIGNAL_STRENGTH_DECIBELS
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_icon = "mdi:signal"
    
    @property
    def unique_id(self):
        """Return a unique ID."""
        return f"{self._device_id}_signal_strength"

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self.device_data['name']} signal strength"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.device_data.get("signal")

class ProfileNameSensor(CopenhagenTrackersEntity, SensorEntity):
    """Sensor for device profile name."""

    _attr_icon = "mdi:card-account-details-outline"
    
    @property
    def unique_id(self):
        """Return a unique ID."""
        return f"{self._device_id}_profile_name"

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self.device_data['name']} profile name"

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