"""The Ebus Glow Worm integration."""

from __future__ import annotations
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .coordinator import EbusGlowWormCoordinator as Coordinator

_PLATFORMS: list[Platform] = [
    Platform.CLIMATE,
    Platform.SWITCH,
    Platform.NUMBER,
    Platform.SENSOR,
]

type EbusGlowWormConfigEntry = ConfigEntry[Coordinator]

_LOGGER = logging.getLogger("EbusGW_" + __name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: EbusGlowWormConfigEntry
) -> bool:
    """Set up Ebus Glow Worm from a config entry."""
    _LOGGER.debug("async_setup_entry")
    hass.data.setdefault(DOMAIN, {})

    coordinator = Coordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, _PLATFORMS)

    return True


async def async_unload_entry(
    hass: HomeAssistant, entry: EbusGlowWormConfigEntry
) -> bool:
    """Unload a config entry."""
    _LOGGER.debug("async_unload_entry")
    return await hass.config_entries.async_unload_platforms(entry, _PLATFORMS)
