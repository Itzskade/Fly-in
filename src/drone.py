"""Represent drones in the simulation."""


class Drone:
    """Represent a drone in the simulation."""

    def __init__(
        self,
        name: str,
        start: str,
        destination: str,
    ) -> None:
        """Initialize a drone."""
        self.name = name
        self.start = start
        self.destination = destination
        self.current = start
        self.path: list[str] = []
        self.path_index = 0
        self.remaining_turns = 0

    def has_arrived(self) -> bool:
        """Return whether the drone reached its destination."""
        return self.current == self.destination

    def next_hub(self) -> str | None:
        """Return the next hub in the path."""
        if self.path_index >= len(self.path):
            return None

        return self.path[self.path_index]

    def move(self) -> bool:
        """Move the drone to the next hub."""
        next_hub = self.next_hub()

        if next_hub is None:
            return False

        self.current = next_hub
        self.path_index += 1

        return True
