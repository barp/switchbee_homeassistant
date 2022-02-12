import base64
import asyncio
import pybswitch
from .switchbee import SwitchBeeCoordinator
from homeassistant import config_entries, core
from homeassistant.const import (
    CONF_CLIENT_SECRET,
    CONF_IP_ADDRESS,
)

from .const import DOMAIN


async def async_setup_entry(hass: core.HomeAssistant,
                            entry: config_entries.ConfigEntry):
  hass.data.setdefault(DOMAIN, {})
  config = dict(entry.data)
  client = await pybswitch.CuClient.new(
      config[CONF_IP_ADDRESS], 23789,
      base64.urlsafe_b64decode(config[CONF_CLIENT_SECRET]))
  coordinator = SwitchBeeCoordinator(hass, entry, config, client)
  await coordinator.async_config_entry_first_refresh()
  hass.data[DOMAIN][entry.entry_id] = coordinator

  hass.async_create_task(
      hass.config_entries.async_forward_entry_setup(entry, "switch"))
  return True


async def async_unload_entry(hass: core.HomeAssistant,
                             entry: config_entries.ConfigEntry):
  unload_ok = all(await asyncio.gather(
      *[hass.config_entries.async_forward_entry_unload(entry, "switch")]))

  if unload_ok:
    hass.data[DOMAIN].pop(entry.entry_id)


async def async_setup(hass: core.HomeAssistant, _: dict) -> bool:
  """Set up the SwitchBee Integration component."""
  hass.data.setdefault(DOMAIN, {})

  return True
