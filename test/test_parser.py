from src.parser import MapParser


def test_parse_easy_map():
    data = MapParser(
        "maps/easy/01_linear_path.txt"
    ).parse()

    assert data["nb_drones"] > 0
    assert data["start_hub"] is not None
    assert data["end_hub"] is not None
    assert len(data["hubs"]) > 0
    assert len(data["connections"]) > 0


def test_parse_all_easy_maps():
    maps = [
        "maps/easy/01_linear_path.txt",
        "maps/easy/02_simple_fork.txt",
        "maps/easy/03_basic_capacity.txt",
    ]

    for filename in maps:
        data = MapParser(filename).parse()

        assert data["nb_drones"] > 0
        assert data["start_hub"] is not None
        assert data["end_hub"] is not None


def test_parse_medium_and_hard_maps():
    maps = [
        "maps/medium/01_dead_end_trap.txt",
        "maps/medium/02_circular_loop.txt",
        "maps/medium/03_priority_puzzle.txt",
        "maps/hard/01_maze_nightmare.txt",
        "maps/hard/02_capacity_hell.txt",
        "maps/hard/03_ultimate_challenge.txt",
    ]

    for filename in maps:
        data = MapParser(filename).parse()

        assert data["nb_drones"] > 0
        assert len(data["hubs"]) > 0
        assert len(data["connections"]) > 0