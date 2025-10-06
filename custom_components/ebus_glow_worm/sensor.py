"""Sensor platform for eBus Glow-worm boiler integration."""

from __future__ import annotations
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    UnitOfTemperature,
    PERCENTAGE,
    UnitOfEnergy,
    UnitOfPower,
    UnitOfPressure,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.typing import StateType
from .const import DOMAIN
from .coordinator import EbusGlowWormCoordinator


from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
    SensorDeviceClass,
    SensorStateClass,
)


SENSOR_DESCRIPTIONS: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key="outside_temp",
        name="Outside Temperature",
        translation_key="outside_temp",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="inside_temp",
        name="Inside Temperature",
        translation_key="inside_temp",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="flow_temp",
        name="Flow Temperature",
        translation_key="flow_temp",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="return_temp",
        name="Return Temperature",
        translation_key="return_temp",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="desired_flow_temp",
        name="Desired Flow Temperature",
        translation_key="desired_flow_temp",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="power",
        name="Power",
        translation_key="power",
        device_class=SensorDeviceClass.POWER_FACTOR,
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="usage_heating",
        name="Heating Usage",
        translation_key="usage_heating",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SensorEntityDescription(
        key="usage_hot_water",
        name="Hot Water Usage",
        translation_key="usage_hot_water",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SensorEntityDescription(
        key="current_heat_loss",
        name="House Estimated Heat Loss",
        translation_key="current_heat_loss",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="water_pressure",
        name="Water Pressure",
        translation_key="water_pressure",
        device_class=SensorDeviceClass.PRESSURE,
        native_unit_of_measurement=UnitOfPressure.BAR,
        state_class=SensorStateClass.MEASUREMENT,
    ),
)

STAT_KEYS = ["usage_heating", "usage_hot_water", "current_heat_loss", "water_pressure"]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up eBus Glow-worm boiler sensors from a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    entities: list[EbusGlowWormSensor] = []

    for description in SENSOR_DESCRIPTIONS:
        if description.key in STAT_KEYS:
            entities.append(
                EbusGlowWormStatSensor(
                    coordinator=coordinator,
                    config_entry=entry,
                    description=description,
                )
            )
        else:
            entities.append(
                EbusGlowWormSensor(
                    coordinator=coordinator,
                    config_entry=entry,
                    description=description,
                )
            )

    async_add_entities(entities)


class EbusGlowWormSensor(CoordinatorEntity[EbusGlowWormCoordinator], SensorEntity):
    """Sensor for eBus Glow-worm boiler."""

    entity_description: SensorEntityDescription

    def __init__(
        self,
        coordinator: EbusGlowWormCoordinator,
        config_entry: ConfigEntry,
        description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, config_entry)
        self.entity_description = description
        self._attr_unique_id = f"{config_entry.entry_id}-{description.key}"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, config_entry.entry_id)},
            "name": f"{coordinator.get_name()} {description.name}",
        }

    @property
    def native_value(self) -> StateType:
        """Return the sensor value."""
        if self.entity_description.key in self.coordinator.data:
            return self.coordinator.data[self.entity_description.key]
        return None

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        if self.entity_description.key in self.coordinator.data:
            return self.coordinator.data[self.entity_description.key] != -1
        return False

class EbusGlowWormStatSensor(CoordinatorEntity[EbusGlowWormCoordinator], SensorEntity):
    """Sensor for eBus Glow-worm boiler."""

    entity_description: SensorEntityDescription

    def __init__(
        self,
        coordinator: EbusGlowWormCoordinator,
        config_entry: ConfigEntry,
        description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, config_entry)
        self.entity_description = description
        self._attr_unique_id = f"{config_entry.entry_id}-{description.key}"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, config_entry.entry_id)},
            "name": description.name,
        }

    @property
    def native_value(self) -> StateType:
        """Return the sensor value."""
        if self.entity_description.key in self.coordinator.data["stat"]:
            return self.coordinator.data["stat"][self.entity_description.key]
        return None

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        if self.entity_description.key in self.coordinator.data["stat"]:
            return self.coordinator.data["stat"][self.entity_description.key] != -1
        return False
