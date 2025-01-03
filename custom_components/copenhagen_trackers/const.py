"""Constants for the Copenhagen Trackers integration."""

from datetime import timedelta

API_ENDPOINT = "https://api.cphtrackers.com/v2"
ATTR_DATA = "data"
ATTR_DESCRIPTION = "description"
ATTR_ID = "id"
BRAND = "Copenhagen Trackers"
CONF_ACCESS_TOKEN = "access_token"
DEFAULT_SCAN_INTERVAL = timedelta(hours=1)
DOMAIN = "copenhagen_trackers"