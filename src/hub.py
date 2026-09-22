"""Represent hubs in the drone map."""

from .drone import Drone


class Hub:
    """Represent a hub in the drone map."""

    VALID_ZONES = {
        "normal",
        "blocked",
        "restricted",
        "priority",
    }

    def __init__(
        self,
        name: str,
        x: int,
        y: int,
        color: str,
        zone: str = "normal",
        max_drones: int | None = None,
    ) -> None:
        """Initialize a hub."""
        self.name = name
        self.x = x
        self.y = y
        self.color = color
        self.zone = zone
        self.max_drones = max_drones
        self.drones: list[Drone] = []

    def has_capacity(self) -> bool:
        """Return whether another drone can enter this hub."""
        if self.max_drones is None:
            return True

        return len(self.drones) < self.max_drones
