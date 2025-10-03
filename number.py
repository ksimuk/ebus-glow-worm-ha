"""Number platform for eBus Boiler Glow-worm integration."""

from __future__ import annotations
from datetime import timedelta
import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory, UnitOfTemperature
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN
from .coordinator import EbusGlowWormCoordinator


from homeassistant.components.number import (
    NumberEntity,
    NumberEntityDescription,
)


_LOGGER = logging.getLogger(__name__)

NUMBER_TYPES: tuple[NumberEntityDescription, ...] = (
    NumberEntityDescription(
        key="hw_target_temp",
        translation_key="hw_target_temp",
        name="Hot water target temperature",
        icon="mdi:thermometer",
        native_min_value=35.0,
        native_max_value=50.0,
        native_step=1.0,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        entity_category=EntityCategory.CONFIG,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up number entities from config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    entities: list[EbusBoilerGlowWormNumber] = []

    for description in NUMBER_TYPES:
        if description.key == "hw_target_temp":
            entities.append(
                EbusBoilerGlowWormNumber(
                    coordinator=coordinator,
                    config_entry=entry,
                    description=description,
                )
            )

    async_add_entities(entities)


class EbusBoilerGlowWormNumber(
    CoordinatorEntity[EbusGlowWormCoordinator], NumberEntity
):
    """Number entity for eBus Boiler Glow-worm."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: EbusGlowWormCoordinator,
        config_entry: ConfigEntry,
        description: NumberEntityDescription,
    ) -> None:
        """Initialize the number entity."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{config_entry.entry_id}_{description.key}"
        self._attr_native_value = self._get_value_from_coordinator()
        self._attr_device_info = {
            "identifiers": {(DOMAIN, config_entry.entry_id)},
            "name": coordinator.get_name(),
        }

    @callback
    def _get_value_from_coordinator(self) -> int | None:
        """Get the current value from coordinator data."""
        if "hw_target_temp" in self.coordinator.data:
            return self.coordinator.data["hw_target_temp"]
        return None

    @property
    def native_value(self) -> int | None:
        """Return the current value."""
        return self._get_value_from_coordinator()

    async def async_set_native_value(self, value: int) -> None:
        """Set the value."""
        await self.coordinator.async_set_hw_target_temp(value)
        await self.coordinator.async_request_refresh()
