
"""Constants for the Copenhagen Trackers integration."""
from datetime import timedelta

DOMAIN = "copenhagen_trackers"
API_ENDPOINT = "https://api.cphtrackers.com/v2"

CONF_ACCESS_TOKEN = "access_token"

DEFAULT_SCAN_INTERVAL = timedelta(hours=1)

ATTR_DESCRIPTION = "description"
ATTR_LOCATION = "location"
ATTR_UPDATED_AT = "updated_at"