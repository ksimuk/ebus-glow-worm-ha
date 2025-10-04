"""Climate platform for eBus Glow-worm boiler integration."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.climate import (
    ClimateEntity,
    ClimateEntityFeature,
    HVACMode,
)
from homeassistant.components.climate.const import HVACAction
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_TEMPERATURE, UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import EbusGlowWormCoordinator

_LOGGER = logging.getLogger(__name__)

PARALLEL_UPDATES = 0


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up climate entity for eBus Glow-worm boiler."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities([EbusBoilerClimate(coordinator, entry)])


class EbusBoilerClimate(CoordinatorEntity[EbusGlowWormCoordinator], ClimateEntity):
    """Representation of the Glow-worm boiler as a climate entity."""

    _attr_has_entity_name = True
    _attr_translation_key = "boiler"
    _attr_temperature_unit = UnitOfTemperature.CELSIUS
    _attr_supported_features = ClimateEntityFeature.TARGET_TEMPERATURE
    _attr_hvac_modes = [HVACMode.HEAT, HVACMode.OFF]
    _attr_min_temp = 10.0
    _attr_max_temp = 30.0

    def __init__(
        self, coordinator: EbusGlowWormCoordinator, entry: ConfigEntry
    ) -> None:
        """Initialize the climate entity."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_climate"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": coordinator.get_name(),
            "manufacturer": "Glow-worm",
        }
        self._attr_supported_features = (
            ClimateEntityFeature.TARGET_TEMPERATURE
            | ClimateEntityFeature.TURN_ON
            | ClimateEntityFeature.TURN_OFF
        )

    @property
    def current_temperature(self) -> StateType:
        """Return the current temperature."""
        return self.coordinator.data.get("current_temperature")

    @property
    def target_temperature(self) -> StateType:
        """Return the temperature we try to reach."""
        return self.coordinator.data.get("target_temperature")

    @property
    def hvac_mode(self) -> HVACMode:
        """Return current operation mode."""
        return (
            HVACMode.HEAT
            if self.coordinator.data.get("heating_active")
            else HVACMode.OFF
        )

    async def async_set_temperature(self, **kwargs: Any) -> None:
        """Set new target temperature."""
        temperature = kwargs.get(ATTR_TEMPERATURE)
        if temperature is None:
            return
        await self.coordinator.async_set_target_temperature(temperature)
        await self.coordinator.async_request_refresh()

    async def async_set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        """Set HVAC mode."""
        if hvac_mode == HVACMode.HEAT:
            await self.coordinator.async_set_heating(True)
        elif hvac_mode == HVACMode.OFF:
            await self.coordinator.async_set_heating(False)
        await self.coordinator.async_request_refresh()

    @property
    def current_temperature(self) -> float | None:
        """Return the current temperature."""
        if "inside_temp" in self.coordinator.data:
            return self.coordinator.data["inside_temp"]
        return None

    @property
    def target_temperature(self) -> float | None:
        """Return the target temperature."""
        if "target_temperature" in self.coordinator.data:
            return self.coordinator.data["target_temperature"]
        return None

    @property
    def hvac_mode(self) -> HVACMode:
        """Return current HVAC mode."""
        if "mode" in self.coordinator.data:
            mode = self.coordinator.data["mode"]
            if mode == "off":
                return HVACMode.OFF
            elif mode == "heating":
                return HVACMode.HEAT
        return HVACMode.OFF

    @property
    def hvac_action(self) -> HVACAction | None:
        """Return the current HVAC action."""
        if "gas_active" in self.coordinator.data:
            active = self.coordinator.data["gas_active"]
            return HVACAction.HEATING if active else HVACAction.IDLE
        return None
