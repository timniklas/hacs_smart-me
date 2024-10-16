from dataclasses import dataclass
from enum import StrEnum
import logging
from random import choice, randrange

from homeassistant.helpers.aiohttp_client import async_get_clientsession
from aiohttp import ClientError, ClientResponseError, ClientSession, BasicAuth
from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)


class DeviceType(StrEnum):
    """Device types."""

    TEMP_SENSOR = "temp_sensor"
    DOOR_SENSOR = "door_sensor"
    OTHER = "other"


@dataclass
class Device:
    """API device."""

    device_id: int
    device_unique_id: str
    device_type: DeviceType
    name: str
    state: int | bool


class API:
    """Class for example API."""

    def __init__(self, hass: HomeAssistant, deviceid: str, username: str, password: str) -> None:
        """Initialise."""
        self.deviceid = deviceid
        self.username = username
        self.password = password
        self._session = async_get_clientsession(hass)

    @property
    def controller_name(self) -> str:
        """Return the name of the controller."""
        return self.deviceid

    def pullDeviceData(self) -> bool:
        """get device data from api."""
        try:
            async with websession.get(url=f"https://api.smart-me.com/Devices/{self.deviceid}", auth=BasicAuth(self.username, self.password)) as response:
                response.raise_for_status()
                response_data = await response.json()
                return response_data
        except ClientResponseError as exc:
            raise APIAuthError("Error connecting to api. Invalid username or password.")
        except ClientError as exc:
            raise APIConnectionError("Error connecting to api.")


class APIAuthError(Exception):
    """Exception class for auth error."""


class APIConnectionError(Exception):
    """Exception class for connection error."""
