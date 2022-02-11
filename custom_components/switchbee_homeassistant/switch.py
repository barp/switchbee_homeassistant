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
    CONF_UNIQUE_ID,
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

SCAN_INTERVAL = timedelta(seconds=10)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
      vol.Required(CONF_CLIENT_SECRET): cv.string,
      vol.Required(CONF_IP_ADDRESS): cv.string,
      }
    )


async def async_setup_platform(
    hass: HomeAssistantType,
    config: ConfigType,
    async_add_entities: Callable,
    discovery_info: Optional[DiscoveryInfoType] = None,
    ):
  session = async_get_clientsession(hass)

  client = await pybswitch.CuClient.new(config[CONF_IP_ADDRESS], 23789, base64.urlsafe_b64decode(config[CONF_CLIENT_SECRET]))
  items = await client.get_all_items()
  switches = [SwitchBeeSwitch(client, item) for item in items]
  async_add_entities(switches, update_before_add=True)


class SwitchBeeSwitch(SwitchEntity):
  def __init__(self, client, item):
    self.client = client
    self.tp = tp
    self.id = id
    self._item = item

  def is_on(self):
    return self._item.value == 100

  async def async_turn_on(self):
    await self.client.turn_on(self._item)
  
  async def async_turn_off(self):
    await self.client.turn_off(self._item)

  async def async_update(self):
    items = await self.client.get_all_items()
    for item in items:
      if item.unit_id == self._item.unit_id and item.unit_type == self._item.unit_type:
        self._item = item
        break
