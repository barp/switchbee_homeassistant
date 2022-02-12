from datetime import timedelta
import logging
import pybswitch
from .const import DOMAIN
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

_LOGGER = logging.getLogger(__name__)


def calculate_unique_id(item):
  return "switchbee_" + str(item.unit_type) + "_" + str(item.unit_id)


class SwitchBeeCoordinator(DataUpdateCoordinator):

  def __init__(self, hass, entry, config: dict, client: pybswitch.CuClient):
    self.entry = entry
    self.client = client
    self.config = config
    super().__init__(
        hass,
        _LOGGER,
        name=DOMAIN,
        update_method=self._make_update_method(),
        update_interval=timedelta(seconds=config.get("update_seconds", 30)))

  async def _update(self):
    try:
      items = await self.client.get_all_items()
      return {calculate_unique_id(item): item for item in items}
    except Exception as err:
      raise UpdateFailed(f"error getting items state: {err}") from err

  def _make_update_method(self):

    async def _update_data():
      return await self._update()

    return _update_data
