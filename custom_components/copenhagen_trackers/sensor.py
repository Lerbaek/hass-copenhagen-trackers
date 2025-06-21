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
ATTR_UPDATED_AT = "updated_at"

# Entity IDs
SUFFIX_BATTERY_PERCENTAGE = ATTR_BATTERY_PERCENTAGE
SUFFIX_LAST_SEEN_AT = "last_seen_at"
SUFFIX_PROFILE = ATTR_PROFILE
SUFFIX_SERVER_SYNC_AT = "server_sync_at"
SUFFIX_CELLULAR_SIGNAL = "cellular_signal"
SUFFIX_GPS_SIGNAL = "gps_signal"

TRANSLATION_KEY_BATTERY_PERCENTAGE = ATTR_BATTERY_PERCENTAGE
TRANSLATION_KEY_LAST_SEEN_AT = SUFFIX_LAST_SEEN_AT
TRANSLATION_KEY_PROFILE = ATTR_PROFILE
TRANSLATION_KEY_SERVER_SYNC_AT = SUFFIX_SERVER_SYNC_AT
TRANSLATION_KEY_CELLULAR_SIGNAL = SUFFIX_CELLULAR_SIGNAL
TRANSLATION_KEY_GPS_SIGNAL = SUFFIX_GPS_SIGNAL

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up Copenhagen Trackers sensors based on a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    
    entities = []
    for device in coordinator.data[ATTR_DATA]:
        entities.extend((
            ServerSyncAtSensor(coordinator, device[ATTR_ID]),
            LastSeenAtSensor(coordinator, device[ATTR_ID]),
            BatteryPercentageSensor(coordinator, device[ATTR_ID]),
            CellularSignalSensor(coordinator, device[ATTR_ID]),
            GPSSignalSensor(coordinator, device[ATTR_ID]),
            ProfileNameSensor(coordinator, device[ATTR_ID])
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

class CellularSignalSensor(CopenhagenTrackersEntity, SensorEntity):
    """Sensor for device cellular signal strength."""

    _attr_device_class = SensorDeviceClass.SIGNAL_STRENGTH
    _attr_native_unit_of_measurement = "dBm"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_native_precision = 0
    _attr_translation_key = TRANSLATION_KEY_CELLULAR_SIGNAL
    SUFFIX = SUFFIX_CELLULAR_SIGNAL

    @staticmethod
    def _convert_to_dbm(value: int | str) -> int:
        """Convert signal value to dBm."""
        return -113 + (2 * int(value))

    @property
    def native_value(self) -> int | None:
        """Return the cellular signal strength."""
        location = self.get_location()
        if not location or not location.get(ATTR_DEVICE_INFO):
            return None
            
        device_info = location[ATTR_DEVICE_INFO]
        # For Cobblestone devices
        if sig_strength := device_info.get("sig_strength"):
            return self._convert_to_dbm(sig_strength)
        # For Gemstone devices
        if trans := device_info.get("trans"):
            return self._convert_to_dbm(trans)
        return None

    @property
    def icon(self) -> str:
        """Return an icon representing the cellular signal strength."""
        value = self.native_value
        if value >= -70:
            return "mdi:signal-cellular-3"
        if value >= -80:
            return "mdi:signal-cellular-2"
        if value >= -90:
            return "mdi:signal-cellular-1"
        if value >= -100:
            return "mdi:signal-cellular-outline"
        return "mdi:sim-off"

class GPSSignalSensor(CopenhagenTrackersEntity, SensorEntity):
    """Sensor for GPS signal quality."""

    _attr_device_class = None
    _attr_native_unit_of_measurement = "bars"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_translation_key = TRANSLATION_KEY_GPS_SIGNAL
    SUFFIX = SUFFIX_GPS_SIGNAL
    _attr_native_max_value = 4
    _attr_native_min_value = 0
    _attr_native_step = 1

    @property
    def native_value(self) -> int | None:
        """Return the GPS signal quality (0-4)."""
        location = self.get_location()
        if not location:
            return None
        return location.get("signal")

    @property
    def extra_state_attributes(self) -> dict | None:
        """Return the GPS signal quality attributes."""
        location = self.get_location()
        if not location or not location.get(ATTR_DEVICE_INFO):
            return None
            
        device_info = location[ATTR_DEVICE_INFO]
        attributes = {}
        
        # For Gemstone
        if ttf := device_info.get("ttf"):
            attributes["time_to_fix"] = int(ttf)
        # For Cobblestone
        if fixt := device_info.get("fixt"):
            attributes["fix_time"] = int(fixt)
        if num_sats := device_info.get("num_sats"):
            attributes["satellites"] = int(num_sats)
            
        return attributes if attributes else None

    @property
    def icon(self) -> str:
        """Return an icon representing the GPS signal quality (bars)."""
        value = self.native_value
        if value >= 4:
            return "mdi:signal-cellular-3"
        if value == 3:
            return "mdi:signal-cellular-2"
        if value == 2:
            return "mdi:signal-cellular-1"
        if value == 1:
            return "mdi:signal-cellular-outline"
        return "mdi:crosshairs-off"

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