
"""Switch platform for Copenhagen Trackers integration."""
from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.entity import EntityCategory

from .const import DOMAIN
from . import CopenhagenTrackersEntity

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up Copenhagen Trackers switches based on a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    
    entities = []
    for device in coordinator.data["data"]:
        entities.append(ForceUpdateSwitch(coordinator, device["id"]))
    
    async_add_entities(entities)

class ForceUpdateSwitch(CopenhagenTrackersEntity, SwitchEntity):
    """Switch to force update of device."""

    _attr_entity_category = EntityCategory.CONFIG
    _attr_icon = "mdi:refresh"
    
    @property
    def unique_id(self):
        """Return a unique ID."""
        return f"cphtrackers_{self._device_id}_force_update"

    @property
    def name(self):
        """Return the name of the switch."""
        return f"{self.device_data['name']} tracker force update"

    @property
    def is_on(self):
        """Return true if the switch is on."""
        # This is a momentary switch, so it's always off
        return False

    async def async_turn_on(self, **kwargs):
        """Turn the switch on."""
        # Trigger an immediate update
        await self.coordinator.async_request_refresh()
        # The switch will automatically return to off state

    async def async_turn_off(self, **kwargs):
        """Turn the switch off."""
        # This is a momentary switch, so turn_off does nothing
        pass