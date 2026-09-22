*This project has been created as part of the 42 curriculum by <<rmarin-n></rmarin-n>.*

# Fly-in

## Description

Fly-in is a Python project that simulates a fleet of drones travelling through a network of connected hubs.

The goal of the project is to find routes between a starting hub and a destination hub while taking into account movement costs, blocked areas, hub capacities, connection capacities, and multiple drones moving simultaneously.

The project is designed around an object-oriented architecture and is divided into several components:

* **Parser**: reads and validates map files.
* **Graph**: represents hubs and connections.
* **Pathfinding**: calculates a route from the start hub to the destination.
* **Drone**: represents the state and movement of each drone.
* **Hub**: represents locations and their capacity restrictions.
* **Connection**: represents links between hubs and their capacity.
* **Simulation**: manages simultaneous drone movements and turn progression.
* **Main**: handles program execution.

The project does not use external graph libraries. The graph and pathfinding logic are implemented directly in Python.

## Features

* Map parsing from text files.
* Multiple drones.
* Start and destination hubs.
* Normal, priority, restricted, and blocked zones.
* Hub capacity restrictions.
* Connection capacity restrictions.
* Simultaneous drone movements.
* Restricted zones with increased movement cost.
* Blocked hubs are excluded from pathfinding.
* Automatic route calculation.
* Turn-by-turn simulation output.
* Input validation and error handling.
* Unit tests.
* Static type checking with Mypy.
* Code quality checking with Flake8.

## Project Structure

```text
Fly-In/
├── README.md
├── Makefile
├── pyproject.toml
├── maps/
│   ├── easy/
│   ├── medium/
│   ├── hard/
│   └── challenger/
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── parser.py
│   ├── graph.py
│   ├── hub.py
│   ├── connection.py
│   ├── drone.py
│   ├── pathfinding.py
│   └── simulation.py
└── test/
    ├── test_parser.py
    ├── test_pathfinding.py
    └── test_simulation.py
```

## Instructions

### Requirements

The project requires:

* Python 3.10 or newer
* `uv`
* Make

The project uses `uv` to manage the Python environment and development dependencies.

### Installation

Clone the repository and enter the project directory:

```bash
git clone <repository-url>
cd Fly-In
```

The project dependencies are managed automatically by `uv`.

### Running the program

A map file must be provided through the `MAP` variable:

```bash
make run MAP=maps/easy/01_linear_path.txt
```

The program can also be executed directly:

```bash
uv run python -m src.main maps/easy/01_linear_path.txt
```

### Running the tests

Run the complete test suite with:

```bash
make test
```

### Code checks

Run Flake8:

```bash
make flake8
```

Run Mypy:

```bash
make mypy
```

Run all checks and tests:

```bash
make check
```

The `check` target runs:

1. Flake8
2. Mypy
3. Pytest

### Available maps

Example maps are provided in the `maps/` directory:

```text
maps/
├── easy/
├── medium/
├── hard/
└── challenger/
```

For example:

```bash
make run MAP=maps/easy/01_linear_path.txt
```

## Input Format

A map is described using a text file.

Example:

```text
nb_drones: 2

start_hub: hub 0 0 [color=green]
end_hub: goal 10 10 [color=yellow]

hub: waypoint1 3 3 [zone=normal]
hub: waypoint2 6 6 [zone=normal]

connection: hub-waypoint1
connection: waypoint1-waypoint2
connection: waypoint2-goal
```

The supported hub properties include:

* `zone`
* `color`
* `max_drones`

Supported zones are:

```text
normal
blocked
restricted
priority
```

Connections can optionally define a maximum capacity:

```text
connection: waypoint1-waypoint2 [max_link_capacity=2]
```

Comments beginning with `#` are ignored.

## Algorithm

### Graph Representation

The map is represented as an undirected graph.

Each `Hub` stores:

* its name;
* its coordinates;
* its zone;
* its color;
* its maximum drone capacity;
* the drones currently occupying it.

Each `Connection` stores:

* its two connected hubs;
* its maximum capacity;
* the drones currently travelling through it.

The `Graph` class contains all hubs and connections and provides methods for retrieving connections and neighbouring hubs.

### Pathfinding

The pathfinding algorithm is implemented manually without using a graph library.

A Dijkstra-style shortest-path algorithm is used because different hub zones can have different movement costs.

Movement costs are:

| Zone       |         Cost |
| ---------- | -----------: |
| Normal     |            1 |
| Priority   |            1 |
| Restricted |            2 |
| Blocked    | Inaccessible |

Blocked hubs are ignored during pathfinding.

The algorithm maintains:

* a distance table containing the current best known cost for each hub;
* a previous-hub table used to reconstruct the final route;
* a list of unvisited hubs.

Once the destination is reached, the previous-hub information is used to reconstruct the path from the start hub to the destination.

### Simulation Strategy

After a route has been calculated, every drone receives the sequence of hubs that it needs to visit.

The simulation progresses turn by turn.

For each turn:

1. Drones currently travelling through restricted areas are updated.
2. Possible movements are calculated.
3. Hub capacity is checked.
4. Connection capacity is checked.
5. Blocked hubs are rejected.
6. Valid movements are applied simultaneously.
7. The movements are printed.

This approach separates route calculation from movement simulation, making the different responsibilities easier to maintain.

## Visual Representation

The project uses a textual turn-by-turn representation rather than a graphical interface.

Each turn displays the movements performed by the drones:

```text
Turn 1: D1-waypoint1
Turn 2: D1-waypoint2 D2-waypoint1
Turn 3: D1-goal D2-waypoint2
Turn 4: D2-goal
Simulation completed in 4 turns.
```

This representation provides a simple way to follow the simulation without requiring additional graphical dependencies.

The output makes it possible to see:

* which drones move during each turn;
* which hub each drone reaches;
* when drones have to wait;
* when multiple drones move simultaneously;
* when the simulation finishes.

## Example

### Input

```text
nb_drones: 2

start_hub: hub 0 0 [color=green]
end_hub: goal 10 10 [color=yellow]

hub: waypoint1 3 3 [zone=normal]
hub: waypoint2 6 6 [zone=normal]

connection: hub-waypoint1
connection: waypoint1-waypoint2
connection: waypoint2-goal
```

### Expected Output

```text
Turn 1: D1-waypoint1
Turn 2: D1-waypoint2 D2-waypoint1
Turn 3: D1-goal D2-waypoint2
Turn 4: D2-goal
Simulation completed in 4 turns.
```

The exact number of turns depends on the map topology, capacities, and movement restrictions.

## Error Handling

The parser validates the input map before starting the simulation.

Examples of invalid input include:

* missing number of drones;
* zero or negative number of drones;
* missing start or destination hub;
* duplicate hub names;
* invalid zones;
* invalid coordinates;
* invalid capacities;
* connections referencing unknown hubs;
* invalid map syntax.

Parsing errors are converted into clear `ValueError` messages and stop the program instead of allowing invalid data to reach the simulation.

## Testing

The project includes tests for:

* map parsing;
* pathfinding;
* blocked hubs;
* successful simulations;
* drone arrival;
* capacity handling.

The complete test suite can be executed with:

```bash
make test
```

Current project checks:

```text
Flake8  ✓
Mypy    ✓
Pytest  ✓
```

## Resources

### Python Documentation

* Python documentation: https://docs.python.org/3/
* Python `typing` documentation: https://docs.python.org/3/library/typing.html
* Python file handling: https://docs.python.org/3/tutorial/inputoutput.html
* Python exceptions: https://docs.python.org/3/tutorial/errors.html

### Algorithms

* Dijkstra's algorithm: https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
* Graph theory: https://en.wikipedia.org/wiki/Graph_theory
* Shortest path problem: https://en.wikipedia.org/wiki/Shortest_path_problem

### Development Tools

* Pytest documentation: https://docs.pytest.org/
* Mypy documentation: https://mypy.readthedocs.io/
* Flake8 documentation: https://flake8.pycqa.org/
* `uv` documentation: https://docs.astral.sh/uv/

### AI Usage

AI tools were used as a development and learning aid during the project.

AI assistance was used for:

* understanding the project requirements and breaking them into smaller tasks;
* discussing the architecture of the Python modules;
* identifying and explaining Python and Mypy errors;
* improving type annotations;
* understanding how package imports work;
* debugging the Makefile and development environment;
* suggesting test cases and checking project requirements;
* reviewing implementation decisions and explaining algorithms.

The AI was also used to help identify issues during development, but the project was implemented, tested, and executed locally by the developer.

The final code was checked using Flake8, Mypy, and Pytest.

## Technical Choices

The project uses a modular object-oriented design so that parsing, graph representation, pathfinding, drones, and simulation are separated into different classes.

Python was chosen because it provides suitable standard-library data structures and type annotations while keeping the implementation relatively compact.

No external graph library is used. The graph and pathfinding algorithms are implemented directly to meet the project requirements and provide a clearer understanding of the underlying algorithms.
