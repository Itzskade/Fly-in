from src.graph import Graph
from src.parser import MapParser
from src.pathfinding import Pathfinding
from src.simulation import Simulation


def create_simulation(filename):
    data = MapParser(filename).parse()

    graph = Graph(
        data["nb_drones"],
        data["start_hub"],
        data["hubs"],
        data["end_hub"],
        data["connections"],
    )

    path = Pathfinding(graph).find_path()

    for drone in data["drones"]:
        drone.path = path[1:]

    return Simulation(
        graph,
        data["drones"],
    )


def test_simulation_finishes():
    simulation = create_simulation(
        "maps/easy/01_linear_path.txt"
    )

    simulation.run()

    assert simulation.all_arrived()


def test_drones_reach_destination():
    simulation = create_simulation(
        "maps/easy/01_linear_path.txt"
    )

    simulation.run()

    for drone in simulation.drones:
        assert drone.has_arrived()


def test_simulation_with_capacity():
    simulation = create_simulation(
        "maps/easy/03_basic_capacity.txt"
    )

    simulation.run()

    assert simulation.all_arrived()