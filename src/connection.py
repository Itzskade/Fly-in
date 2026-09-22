"""Represent connections between hubs."""

from .drone import Drone


class Connection:
    """Represent a connection between two hubs."""

    def __init__(
        self,
        hub_a,
        hub_b,
        max_link_capacity: int = 1,
    ) -> None:
        """Initialize a connection."""
        self.hub_a = hub_a
        self.hub_b = hub_b
        self.max_link_capacity = max_link_capacity
        self.drones: list[Drone] = []

    def get_other_hub(self, hub):
        """Return the hub at the other end of the connection."""
        if hub == self.hub_a:
            return self.hub_b

        if hub == self.hub_b:
            return self.hub_a

        return None

    def has_capacity(self) -> bool:
        """Return whether another drone can use the connection."""
        return len(self.drones) < self.max_link_capacity
