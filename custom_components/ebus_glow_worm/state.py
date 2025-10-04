import logging

from homeassistant.components.sensor.const import SensorDeviceClass, SensorStateClass
from homeassistant.const import UnitOfTemperature
from dataclasses import dataclass


# data strcuture recived from boiler with description and types for each field
@dataclass
class EbusBoilerDataBoiler:
    name: str
    #    model: str
    #    firmware: str
    connected: bool
    error: str


@dataclass
class EbusBoilerDataStat:
    usage_heating: float
    usage_hot_water: float


@dataclass
class EbusoilerData:
    mode: str
    target_temperature: float
    hw_target_temp: float
    outside_temp: float
    inside_temp: float
    heat_loss_balance: int
    flow_temp: float
    return_temp: float
    desired_flow_temp: int
    power: int
    gas_active: bool
    pump_active: bool
    consumption_heating: int
    stat: EbusBoilerDataStat
    boiler: EbusBoilerDataBoiler
