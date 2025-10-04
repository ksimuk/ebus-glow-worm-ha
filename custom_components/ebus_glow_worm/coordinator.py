"""Coordinator for the eBus Glow Worm boiler integration."""

import logging
from typing import Any

import requests

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_PORT
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    HomeAssistant,
    UpdateFailed,
    timedelta,
)

from .const import DOMAIN, PARAMETERS_MAP

_LOGGER = logging.getLogger("EbusGW_" + __name__)


class EbusGlowWormCoordinator(DataUpdateCoordinator):
    """Ebus Glow Worm coordinator class."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize."""

        self.entry = entry
        self.host = entry.data[CONF_HOST]
        self.port = entry.data[CONF_PORT]
        self.password = entry.data[CONF_PASSWORD]
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=60),
        )
        self.entry = entry

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from the boiler."""
        try:
            return await self.hass.async_add_executor_job(self._fetch_data)
        except Exception as err:
            raise UpdateFailed(f"Error communicating with boiler: {err}") from err

    def _fetch_data(self) -> dict[str, Any]:
        """Fetch data from the boiler."""
        # load json from host:port

        data = {}
        try:
            response = requests.get(f"http://{self.host}:{self.port}/get", timeout=5)
            response.raise_for_status()
            data.update(response.json())
        except requests.Timeout:
            _LOGGER.error("Request timed out")
        except requests.RequestException as err:
            _LOGGER.error(f"Error fetching data: {err}")
        finally:
            response.close()
        return data

    async def async_set_target_temperature(self, temperature: float) -> None:
        """Set target temperature."""
        try:
            await self.hass.async_add_executor_job(
                self._set_target_temperature, temperature
            )
        except Exception as err:
            raise UpdateFailed(f"Error setting target temperature: {err}") from err

    async def async_set_heating(self, heating: bool) -> None:
        """Set heating."""
        try:
            await self.hass.async_add_executor_job(self._set_heating, heating)
        except Exception as err:
            raise UpdateFailed(f"Error setting heating: {err}") from err

    def _set_target_temperature(self, temperature: float) -> None:
        """Set target temperature."""
        try:
            response = requests.post(
                f"http://{self.host}:{self.port}/set",
                json={"target_temperature": temperature},
                timeout=5,
            )
            response.raise_for_status()
        except requests.Timeout:
            _LOGGER.error("Request timed out")
        except requests.RequestException as err:
            _LOGGER.error(f"Error setting target temperature: {err}")
        finally:
            response.close()

    def _set_heating(self, heating: bool) -> None:
        """Set heating."""
        try:
            response = requests.post(
                f"http://{self.host}:{self.port}/set",
                json={"mode": "heating" if heating else "off"},
                timeout=5,
            )
            response.raise_for_status()
        except requests.Timeout:
            _LOGGER.error("Request timed out")
        except requests.RequestException as err:
            _LOGGER.error(f"Error setting heating: {err}")
        finally:
            response.close()

    async def async_set_switch(self, key: str, state: bool) -> None:
        """Set switch state."""
        try:
            await self.hass.async_add_executor_job(self._set_switch, key, state)
        except Exception as err:
            raise UpdateFailed(f"Error setting switch {key}: {err}") from err

    def _set_switch(self, key: str, state: bool) -> None:
        """Set switch state."""
        try:
            response = requests.post(
                f"http://{self.host}:{self.port}/override?force_heating={'1' if state else '0'}",
                json={key: state},
                timeout=5,
            )
            response.raise_for_status()
        except requests.Timeout:
            _LOGGER.error("Request timed out")
        except requests.RequestException as err:
            _LOGGER.error(f"Error setting switch {key}: {err}")
        finally:
            response.close()

    def get_name(self) -> str:
        """Return the name of the boiler."""
        return (
            self.data["boiler"]["name"]
            if "boiler" in self.data and "name" in self.data["boiler"]
            else "Ebus Glow-worm Boiler"
        )

    async def async_set_hw_target_temp(self, temperature: float) -> None:
        """Set hot water target temperature."""
        try:
            await self.hass.async_add_executor_job(
                self._set_hw_target_temp, temperature
            )
        except Exception as err:
            raise UpdateFailed(
                f"Error setting hot water target temperature: {err}"
            ) from err

    def _set_hw_target_temp(self, temperature: float) -> None:
        """Set hot water target temperature."""
        try:
            response = requests.post(
                f"http://{self.host}:{self.port}/set",
                json={"hw_target_temp": int(temperature)},
                timeout=5,
            )
            response.raise_for_status()
        except requests.Timeout:
            _LOGGER.error("Request timed out")
        except requests.RequestException as err:
            _LOGGER.error(f"Error setting hot water target temperature: {err}")
        finally:
            response.close()
