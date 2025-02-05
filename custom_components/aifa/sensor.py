"""Definition of AIFA sensor platform."""

from collections.abc import Callable
from dataclasses import dataclass

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import PERCENTAGE, UnitOfTemperature
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import AIFAConfigEntry, AIFACoordinator


@dataclass(frozen=True, kw_only=True)
class AIFASensorDescription(SensorEntityDescription):
    """Class describing AccuWeather sensor entities."""

    value: Callable[[dict], float | int | None]


SENSOR_TYPES: list[AIFASensorDescription] = [
    AIFASensorDescription(
        key="temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        value=lambda data: data.get("temperature"),
    ),
    AIFASensorDescription(
        key="humidity",
        device_class=SensorDeviceClass.HUMIDITY,
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value=lambda data: data.get("humidity"),
    ),
]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: AIFAConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up sensor entities based on a config entry."""
    coordinator = entry.runtime_data
    entities: list[AIFASensor] = [
        AIFASensor(coordinator, description) for description in SENSOR_TYPES
    ]
    async_add_entities(entities)


class AIFASensor(CoordinatorEntity, SensorEntity):
    """Representation of a Sensor."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: AIFACoordinator,
        description: AIFASensorDescription,
    ) -> None:
        """Initialize a single sensor."""
        super().__init__(coordinator)
        self.entity_description: AIFASensorDescription = description

        self._attr_device_info = coordinator.device_info
        self._attr_unique_id = f"{coordinator.device_id}_{description.key}"
        self._attr_native_value = description.value(coordinator.data)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_native_value = self.entity_description.value(self.coordinator.data)
        self.async_write_ha_state()
