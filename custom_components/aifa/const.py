"""Define constants for the AIFA integration."""

from dataclasses import dataclass

DOMAIN = "aifa"

CONF_ACCESS_TOKEN = "access_token"
CONF_REFRESH_TOKEN = "refresh_token"

API_CLIENT_ID = "Ecp5TUQxtOjdQ24u"
API_URL_TOKEN = "https://api.aifaremote.com/oauth2/token"
API_URL_DEVICE = "https://api.aifaremote.com/devices"
API_GRANT_TYPE_PASSWORD = "password"
API_GRANT_TYPE_REFRESH_TOKEN = "refresh_token"
API_USER_AGENT = "Dart/3.0 (dart:io)"

UPDATE_INTERVAL = 300
REFRESH_INTERVAL = 60 * 60 * 12

MANUFACTURER = "AIFA Smart"


@dataclass
class AIFAAPISubDevice:
    """AIFA Sub Device."""

    name: str
    subType: int  # noqa: N815
    id: int
    deviceCode: int  # noqa: N815
    type: int
    deviceId: int  # noqa: N815


@dataclass
class AIFADeviceSensor:
    """AIFA Device Sensor."""

    temperature: float
    humidity: float


@dataclass
class AIFAAPIDevice:
    """AIFA Device."""

    owner: bool
    country: int
    type: int
    version: int
    mac: str
    room: str
    sensors: AIFADeviceSensor
    subversion: int
    subDevices: list[AIFAAPISubDevice]  # noqa: N815
    name: str
    online: bool
    location: dict
    id: int
    locked: bool
    firmware: int


@dataclass
class AIFAAPIDevices:
    """AIFA Devices."""

    devices: list[AIFAAPIDevice]


@dataclass
class AIFAAPIToken:
    """AIFA token response."""

    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int
