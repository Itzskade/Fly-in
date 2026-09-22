"""Represent the map graph."""

from .connection import Connection
from .hub import Hub


class Graph:
    """Represent the map graph."""

    def __init__(
        self,
        nb_drones: int,
        start_hub: Hub,
        hubs: dict[str, Hub],
        end_hub: Hub,
        connections: list[Connection],
    ) -> None:
        """Initialize the graph."""
        self.nb_drones = nb_drones
        self.start_hub = start_hub
        self.hubs = hubs
        self.end_hub = end_hub
        self.connections = connections

    def get_connections(
        self,
        hub_name: str,
    ) -> list[Connection]:
        """Return connections connected to a hub."""
        connections = []

        for connection in self.connections:
            if (
                connection.hub_a.name == hub_name
                or connection.hub_b.name == hub_name
            ):
                connections.append(connection)

        return connections

    def get_neighbors(
        self,
        hub_name: str,
    ) -> list[str]:
        """Return neighboring hub names."""
        neighbors = []

        for connection in self.get_connections(hub_name):
            if connection.hub_a.name == hub_name:
                neighbors.append(connection.hub_b.name)
            else:
                neighbors.append(connection.hub_a.name)

        return neighbors
