from datetime import UTC, datetime, timedelta
from enum import StrEnum
from typing import Annotated, Self

from pydantic import BaseModel, Field, field_validator, model_validator


class MetricType(StrEnum):
    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"
    PRESSURE = "pressure"


METRIC_BOUNDS: dict[MetricType, tuple[float, float]] = {
    MetricType.TEMPERATURE: (-50.0, 100.0),
    MetricType.HUMIDITY: (0.0, 100.0),
    MetricType.PRESSURE: (800.0, 1200.0),
}

MAX_CLOCK_SKEW = timedelta(minutes=5)


class ReadingCreate(BaseModel):
    """Input for POST /readings: one sensor reading."""

    device_id: Annotated[
        str, Field(min_length=1, max_length=100, pattern=r"^[A-Za-z0-9_-]+$")
    ]
    metric: MetricType
    value: float
    timestamp: datetime

    @field_validator("timestamp")
    @classmethod
    def timestamp_must_be_plausible(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            msg = "timestamp must include a timezone offset"
            raise ValueError(msg)
        if value > datetime.now(UTC) + MAX_CLOCK_SKEW:
            msg = "timestamp must not be in the future"
            raise ValueError(msg)
        return value

    @model_validator(mode="after")
    def value_must_fit_metric(self) -> Self:
        low, high = METRIC_BOUNDS[self.metric]
        if not low <= self.value <= high:
            msg = (
                f"{self.metric} reading {self.value} "
                f"outside plausible range [{low}, {high}]"
            )
            raise ValueError(msg)
        return self