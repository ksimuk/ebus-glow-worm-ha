"""Switch platform for eBus Glow-worm boiler integration."""

from __future__ import annotations
from datetime import timedelta
import logging
from typing import Any
from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN
from .coordinator import EbusGlowWormCoordinator


_LOGGER = logging.getLogger(__name__)

PARALLEL_UPDATES = 0

SWITCH_TYPES = {
    0: {
        "key": "gas_active",
        "name": "Gas Active",
        "translation_key": "heating_enabled",
        "device_class": None,
        "icon": "mdi:radiator",
    },
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up eBus Glow-worm boiler switches from a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    entities: list[EbusBoilerSwitch] = []

    for description in SWITCH_TYPES.values():
        if description["key"] in coordinator.data:
            entities.append(EbusBoilerSwitch(coordinator, description, entry))

    async_add_entities(entities)


class EbusBoilerSwitch(
    CoordinatorEntity[EbusGlowWormCoordinator], dict[str, Any], SwitchEntity
):
    """Representation of a eBus Glow-worm boiler switch."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: EbusGlowWormCoordinator,
        description: dict[str, Any],
        entry: ConfigEntry,
    ) -> None:
        """Initialize the switch entity."""
        super().__init__(coordinator)
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": coordinator.get_name(),
        }
        self.description = description
        self._attr_unique_id = f"{entry.entry_id}_switch_{description['key']}"
        self._attr_translation_key = description["translation_key"]
        self._attr_name = f"{coordinator.get_name()} {description['name']}"

    @property
    def is_on(self) -> bool | None:
        """Return true if the switch is on."""
        return self.coordinator.data[self.description["key"]]

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on."""
        await self._async_set_state(True)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off."""
        await self._async_set_state(False)

    async def _async_set_state(self, state: bool) -> None:
        """Set the state of the switch."""
        try:
            await self.coordinator.async_set_switch(self.description["key"], state)
        except Exception as err:
            _LOGGER.error("Failed to set %s: %s", self.description["key"], err)
            return
        await self.coordinator.async_request_refresh()

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.description["key"] in self.coordinator.data
