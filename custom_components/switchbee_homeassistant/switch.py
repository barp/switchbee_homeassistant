import logging
from typing import Any, Callable, Dict, Optional
from datetime import timedelta

import pybswitch
import base64

import voluptuous as vol

from homeassistant.components.switch import PLATFORM_SCHEMA
from homeassistant.const import (
    CONF_CLIENT_SECRET,
    CONF_IP_ADDRESS,
)

from homeassistant.helpers.aiohttp_client import async_get_clientsession
import homeassistant.helpers.config_validation as cv

try:
  from homeassistant.components.switch import SwitchEntity
except ImportError:
  from homeassistant.components.switch import SwitchDevice as SwitchEntity

from homeassistant.helpers.typing import (
    ConfigType,
    DiscoveryInfoType,
    HomeAssistantType,
)

from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(minutes=1)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_CLIENT_SECRET): cv.string,
    vol.Required(CONF_IP_ADDRESS): cv.string,
})


def calculate_unique_id(item):
  return "switchbee_" + str(item.unit_type) + "_" + str(item.unit_id)


async def async_setup_platform(
    hass: HomeAssistantType,
    config: ConfigType,
    async_add_entities: Callable,
    _: Optional[DiscoveryInfoType] = None,
):
  async_get_clientsession(hass)

  client = await pybswitch.CuClient.new(
      config[CONF_IP_ADDRESS], 23789,
      base64.urlsafe_b64decode(config[CONF_CLIENT_SECRET]))

  async def async_update_data():
    try:
      items = await client.get_all_items()
      return {calculate_unique_id(item): item for item in items}
    except Exception as err:
      raise UpdateFailed(f"error getting items state: {err}")

  coordinator = DataUpdateCoordinator(
      hass,
      _LOGGER,
      name="switchbee",
      update_method=async_update_data,
      update_interval=timedelta(minutes=1),
  )
  await coordinator.async_config_entry_first_refresh()
  switches = [
      SwitchBeeSwitch(coordinator, id, client)
      for id in coordinator.data.keys()
  ]
  async_add_entities(switches, update_before_add=True)


class SwitchBeeSwitch(CoordinatorEntity, SwitchEntity):

  def __init__(self, coordinator: DataUpdateCoordinator, id: str,
               client: pybswitch.CuClient):
    super().__init__(coordinator)
    self.client = client
    self._unique_id = id

  @property
  def is_on(self):
    return self.coordinator.data[self._unique_id].value == 100

  @property
  def unique_id(self) -> str:
    return self._unique_id

  @property
  def name(self):
    """The name property."""
    return self.coordinator.data[self._unique_id].name

  async def async_turn_on(self):
    await self.client.turn_on(self.coordinator.data[self._unique_id])
    await self.coordinator.async_request_refresh()

  async def async_turn_off(self):
    await self.client.turn_off(self.coordinator.data[self._unique_id])
    await self.coordinator.async_request_refresh()
