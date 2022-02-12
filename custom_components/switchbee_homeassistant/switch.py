import logging
from typing import Callable
from homeassistant import config_entries, core

import pybswitch
from .const import DOMAIN

from homeassistant.helpers.aiohttp_client import async_get_clientsession

from homeassistant.components.switch import SwitchEntity

from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: core.HomeAssistant,
    entry: config_entries.ConfigEntry,
    async_add_entities: Callable,
):
  async_get_clientsession(hass)
  coordinator = hass.data[DOMAIN][entry.entry_id]

  switches = [
      SwitchBeeSwitch(coordinator, id, coordinator.client)
      for id in coordinator.data.keys()
  ]
  async_add_entities(switches)


class SwitchBeeSwitch(CoordinatorEntity, SwitchEntity):

  def __init__(self, coordinator: DataUpdateCoordinator, id: str,
               client: pybswitch.CuClient):
    super().__init__(coordinator)
    self.client = client
    self._unique_id = id

  @property
  def _item(self):
    return self.coordinator.data[self._unique_id]

  @property
  def is_on(self):
    return self._item.value == 100

  @property
  def unique_id(self) -> str:
    return self._unique_id

  @property
  def name(self):
    """The name property."""
    return self._item.name

  async def async_turn_on(self):
    await self.client.turn_on(self._item)
    await self.coordinator.async_request_refresh()

  async def async_turn_off(self):
    await self.client.turn_off(self._item)
    await self.coordinator.async_request_refresh()

  @property
  def device_info(self):
    return {
        "identifiers": {("id", self.unique_id)},
        "name": self.name,
        "manufacturer": "SwitchBee",
        "model": "Switch",
    }
