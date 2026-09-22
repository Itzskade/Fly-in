"""Run the drone simulation."""

from .connection import Connection
from .drone import Drone
from .graph import Graph


class Simulation:
    """Simulate the drone movements."""

    def __init__(
        self,
        graph: Graph,
        drones: list[Drone],
    ) -> None:
        """Initialize the simulation."""
        self.graph = graph
        self.drones = drones
        self.turn = 0
        self.in_flight: dict[
            Drone, tuple[Connection, str, int]
        ] = {}

        for drone in drones:
            graph.start_hub.drones.append(drone)

    def run(self) -> None:
        """Run the simulation until all drones arrive."""
        while not self.all_arrived():
            self.turn += 1

            self.finish_flights()

            moves = self.plan_moves()

            self.apply_moves(moves)

            if moves:
                output = []

                for drone, _, next_hub in moves:
                    output.append(f"{drone.name}-{next_hub}")

                print(f"Turn {self.turn}: {' '.join(output)}")

    def all_arrived(self) -> bool:
        """Return whether all drones reached the destination."""
        for drone in self.drones:
            if not drone.has_arrived():
                return False

        return True

    def finish_flights(self) -> None:
        """Finish drones currently travelling."""
        finished = []

        for drone, data in self.in_flight.items():
            connection, destination, remaining = data

            remaining -= 1

            if remaining <= 0:
                drone.current = destination
                drone.path_index += 1

                if drone not in self.graph.hubs[
                    destination
                ].drones:
                    self.graph.hubs[destination].drones.append(
                        drone
                    )

                if drone in connection.drones:
                    connection.drones.remove(drone)

                finished.append(drone)
            else:
                self.in_flight[drone] = (
                    connection,
                    destination,
                    remaining,
                )

        for drone in finished:
            del self.in_flight[drone]

    def plan_moves(
        self,
    ) -> list[tuple[Drone, Connection, str]]:
        """Plan all possible moves for the current turn."""
        moves: list[tuple[Drone, Connection, str]] = []

        hub_arrivals: dict[str, int] = {}
        connection_usage: dict[Connection, int] = {}

        for drone in self.drones:
            if drone.has_arrived():
                continue

            if drone in self.in_flight:
                continue

            next_hub_name = drone.next_hub()

            if next_hub_name is None:
                continue

            next_hub = self.graph.hubs[next_hub_name]

            if next_hub.zone == "blocked":
                continue

            connection = self.find_connection(
                drone.current,
                next_hub_name,
            )

            if connection is None:
                continue

            current_usage = connection_usage.get(
                connection,
                0,
            )

            if (
                len(connection.drones) + current_usage
                >= connection.max_link_capacity
            ):
                continue

            if next_hub.max_drones is not None:
                current_drones = len(next_hub.drones)

                departures = self.count_departures(
                    next_hub_name,
                    moves,
                )

                arrivals = hub_arrivals.get(
                    next_hub_name,
                    0,
                )

                available = (
                    current_drones
                    - departures
                    + arrivals
                )

                if available >= next_hub.max_drones:
                    continue

            moves.append(
                (
                    drone,
                    connection,
                    next_hub_name,
                )
            )

            connection_usage[connection] = (
                current_usage + 1
            )

            hub_arrivals[next_hub_name] = (
                hub_arrivals.get(next_hub_name, 0) + 1
            )

        return moves

    def count_departures(
        self,
        hub_name: str,
        moves: list[tuple[Drone, Connection, str]],
    ) -> int:
        """Count drones leaving a hub this turn."""
        count = 0

        for drone, _, _ in moves:
            if drone.current == hub_name:
                count += 1

        return count

    def apply_moves(
        self,
        moves: list[tuple[Drone, Connection, str]],
    ) -> None:
        """Apply all planned moves simultaneously."""
        for drone, connection, next_hub_name in moves:
            current_hub = self.graph.hubs[drone.current]
            next_hub = self.graph.hubs[next_hub_name]

            if drone in current_hub.drones:
                current_hub.drones.remove(drone)

            if next_hub.zone == "restricted":
                connection.drones.append(drone)

                self.in_flight[drone] = (
                    connection,
                    next_hub_name,
                    2,
                )
            else:
                next_hub.drones.append(drone)
                drone.move()

    def find_connection(
        self,
        first: str,
        second: str,
    ) -> Connection | None:
        """Find the connection between two hubs."""
        for connection in self.graph.connections:
            if (
                connection.hub_a.name == first
                and connection.hub_b.name == second
            ) or (
                connection.hub_a.name == second
                and connection.hub_b.name == first
            ):
                return connection

        return None
