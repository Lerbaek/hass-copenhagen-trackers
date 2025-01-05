"""Coordinator for the Copenhagen Trackers integration."""

from __future__ import annotations
from datetime import datetime, timedelta, timezone
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .api import CopenhagenTrackersAPI

class CopenhagenTrackersDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Copenhagen Trackers data."""

    def __init__(
        self,
        hass: HomeAssistant,
        logger: logging.Logger,
        api: CopenhagenTrackersAPI,
        name: str,
        update_interval: timedelta,
    ) -> None:
        """Initialize."""
        super().__init__(
            hass,
            logger,
            name=name,
            update_interval=update_interval,
        )
        self.api = api
        self._last_sync_time = None

    async def _async_update_data(self):
        """Update data via library."""
        try:
            data = await self.api.async_get_devices_with_auth()
            self._last_sync_time = datetime.now(timezone.utc)
            return data
        except Exception as exception:
            raise UpdateFailed(exception) from exception

    @property
    def last_sync_time(self) -> datetime.datetime:
        """Return the timestamp of the last successful sync."""
        return self._last_sync_time