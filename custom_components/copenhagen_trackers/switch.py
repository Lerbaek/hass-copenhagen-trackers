"""Switch platform for Copenhagen Trackers integration."""

from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.entity import EntityCategory

from .const import (
    DOMAIN,
    ATTR_DATA,
    ATTR_ID
)
from .entity import CopenhagenTrackersEntity

# Entity IDs
SUFFIX_FORCE_REFRESH = "force_refresh"
TRANSLATION_KEY_FORCE_REFRESH = SUFFIX_FORCE_REFRESH

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up Copenhagen Trackers switches based on a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    
    entities = []
    for device in coordinator.data[ATTR_DATA]:
        entities.append(ForceRefreshSwitch(coordinator, device[ATTR_ID]))
    
    async_add_entities(entities)

class ForceRefreshSwitch(CopenhagenTrackersEntity, SwitchEntity):
    """Switch to force a refresh from the servers."""

    _attr_entity_category = EntityCategory.CONFIG
    _attr_icon = "mdi:refresh"
    _attr_translation_key = TRANSLATION_KEY_FORCE_REFRESH
    SUFFIX = SUFFIX_FORCE_REFRESH

    @property
    def is_on(self):
        """Return true if the switch is on."""
        # This is a momentary switch, so it's always off
        return False

    async def async_turn_on(self, **kwargs):
        """Turn the switch on."""
        # Trigger a immediate refresh
        await self.coordinator.async_request_refresh()
        # The switch will automatically return to off state

    async def async_turn_off(self, **kwargs):
        """Turn the switch off."""
        # This is a momentary switch, so turn_off does nothing
        pass