"""Constants for the Ebus Glow Worm integration."""

from homeassistant.const import UnitOfTemperature
from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass

DOMAIN = "ebus_boiler_glow_worm"

PARAMETERS_MAP = {
    0: {
        "param_id": "mode",
        "name": "Selected Operating Mode",
        "unit": None,
        "device_class": None,
        "state_class": None,
        "scale": 1,
        "offset": 0,
        "description": "Selected operating mode (off=OFF, heating=HEATING)",
    },
    1: {
        "param_id": "inside_temp",
        "name": "Room Temperature",
        "unit": UnitOfTemperature.CELSIUS,
        "device_class": SensorDeviceClass.TEMPERATURE,
        "state_class": SensorStateClass.MEASUREMENT,
        "scale": 0.1,
        "offset": 0,
        "description": "Room temperature",
    },
    2: {
        "param_id": "target_temperature",
        "name": "Target Room Temperature",
        "unit": UnitOfTemperature.CELSIUS,
        "device_class": SensorDeviceClass.TEMPERATURE,
        "state_class": SensorStateClass.MEASUREMENT,
        "scale": 0.1,
        "offset": 0,
        "description": "Target room temperature",
    },
    3: {
        "param_id": "outside_temp",
        "name": "Outside Temperature",
        "unit": UnitOfTemperature.CELSIUS,
        "device_class": SensorDeviceClass.TEMPERATURE,
        "state_class": SensorStateClass.MEASUREMENT,
        "scale": 0.1,
        "offset": 0,
        "description": "Outside temperature",
    },
    4: {
        "param_id": "flow_temp",
        "name": "Flow Temperature",
        "unit": UnitOfTemperature.CELSIUS,
        "device_class": SensorDeviceClass.TEMPERATURE,
        "state_class": SensorStateClass.MEASUREMENT,
        "scale": 0.1,
        "offset": 0,
        "description": "Flow temperature",
    },
    5: {
        "param_id": "return_temp",
        "name": "Return Temperature",
        "unit": UnitOfTemperature.CELSIUS,
        "device_class": SensorDeviceClass.TEMPERATURE,
        "state_class": SensorStateClass.MEASUREMENT,
        "scale": 0.1,
        "offset": 0,
        "description": "Return temperature",
    },
    6: {
        "param_id": "gas_active",
        "name": "Gas Active",
        "device_class": None,
        "description": "Is gas currently active (1=Yes, 0=No)",
    },
    7: {
        "param_id": "name",
        "name": "Boiler Name",
        "device_class": None,
        "description": "Name of the boiler",
    },
    8: {
        "param_id": "hw_target_temp",
        "name": "Hot Water Target Temperature",
        "unit": UnitOfTemperature.CELSIUS,
        "device_class": SensorDeviceClass.TEMPERATURE,
        "state_class": SensorStateClass.MEASUREMENT,
        "description": "Hot water target temperature",
    },
}
