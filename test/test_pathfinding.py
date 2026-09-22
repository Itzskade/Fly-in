from src.graph import Graph
from src.parser import MapParser
from src.pathfinding import Pathfinding


def create_graph(filename):
    data = MapParser(filename).parse()

    return Graph(
        data["nb_drones"],
        data["start_hub"],
        data["hubs"],
        data["end_hub"],
        data["connections"],
    )


def test_find_path():
    graph = create_graph(
        "maps/easy/01_linear_path.txt"
    )

    path = Pathfinding(graph).find_path()

    assert path
    assert path[0] == graph.start_hub.name
    assert path[-1] == graph.end_hub.name


def test_path_avoids_blocked_hubs():
    graph = create_graph(
        "maps/easy/01_linear_path.txt"
    )

    path = Pathfinding(graph).find_path()

    for hub_name in path:
        assert graph.hubs[hub_name].zone != "blocked"


def test_path_exists_in_hard_map():
    graph = create_graph(
        "maps/hard/01_maze_nightmare.txt"
    )

    path = Pathfinding(graph).find_path()

    assert path
    assert path[0] == graph.start_hub.name
    assert path[-1] == graph.end_hub.name