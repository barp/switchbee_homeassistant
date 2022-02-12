from homeassistant import config_entries, core
from typing import Any, Dict, Optional
from homeassistant.const import CONF_CLIENT_SECRET, CONF_IP_ADDRESS
import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from .const import DOMAIN

CONFIG_SCHEMA = vol.Schema({
    vol.Required(CONF_CLIENT_SECRET): cv.string,
    vol.Required(CONF_IP_ADDRESS): cv.string,
})


class SwitchBeeConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):

  data: Optional[Dict[str, Any]]

  async def async_step_user(self, user_input: Optional[Dict[str, Any]] = None):
    errors: Dict[str, str] = {}
    if user_input is not None:
      # TODO add validations, create client that tries to send the CU GETA request
      self.data = user_input

      return self.async_create_entry(title="SwitchBee", data=self.data)

    return self.async_show_form(step_id="user",
                                data_schema=CONFIG_SCHEMA,
                                errors=errors)
