import logging
from typing import Any, Callable, Dict, Optional

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

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
      vol.Required(CONF_CLIENT_SECRET): cv.string,
      vol.Required(CONF_IP_ADDRESS): cv.string,
      vol.Required(CONF_UNIQUE_ID): cv.string,
      }
    )


def parse_id(id: str):
  tp, id = id.split(",")
  return tp, id

async def async_setup_platform(
    hass: HomeAssistantType,
    config: ConfigType,
    async_add_entities: Callable,
    discovery_info: Optional[DiscoveryInfoType] = None,
    ):
  session = async_get_clientsession(hass)
  switches = [SwitchBeeSwitch(conf[CONF_CLIENT_SECRET], conf[CONF_IP_ADDRESS], tp, id)]
  async_add_entities(switches, update_before_add=True)


class SwitchBeeSwitch(SwitchEntity):
  def __init__(self, cert, ip, tp, id):
    self.cert = cert
    self.ip = ip
    self.tp = tp
    self.id = id
    self._state = False # not on

  def is_on(self):
    return self._state

  async def async_turn_on(self):
    pass
  
  async def async_turn_off(self):
    pass

  async def async_update(self):
    pass
