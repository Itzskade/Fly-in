"""Entry point for the Fly-in simulation."""

import sys

from .graph import Graph
from .parser import MapParser
from .pathfinding import Pathfinding
from .simulation import Simulation


def main() -> None:
    """Run the Fly-in program."""
    if len(sys.argv) != 2:
        print("Usage: python -m src.main <map_file>")
        return

    filename = sys.argv[1]

    try:
        data = MapParser(filename).parse()

        graph = Graph(
            data["nb_drones"],
            data["start_hub"],
            data["hubs"],
            data["end_hub"],
            data["connections"],
        )

        pathfinding = Pathfinding(graph)
        path = pathfinding.find_path()

        if not path:
            print("No path from start to end.")
            return

        for drone in data["drones"]:
            drone.path = path[1:]

        simulation = Simulation(
            graph,
            data["drones"],
        )

        simulation.run()

        print(f"Simulation completed in {simulation.turn} turns.")

    except (OSError, ValueError, KeyError) as error:
        print(error)


if __name__ == "__main__":
    main()
