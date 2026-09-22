"""Find paths through the graph."""

from .graph import Graph


class Pathfinding:
    """Find paths through the graph."""

    def __init__(self, graph: Graph) -> None:
        """Initialize pathfinding."""
        self.graph = graph

    def find_path(self) -> list[str]:
        """Find the shortest path from start to end."""
        distances = {}

        for hub_name in self.graph.hubs:
            distances[hub_name] = float("inf")

        start = self.graph.start_hub.name
        end = self.graph.end_hub.name

        distances[start] = 0

        previous = {}
        unvisited = list(distances.keys())

        while unvisited:
            current = min(
                unvisited,
                key=lambda hub: distances[hub]
            )
            unvisited.remove(current)

            if distances[current] == float("inf"):
                break

            if current == end:
                break

            for neighbor in self.graph.get_neighbors(current):
                hub = self.graph.hubs[neighbor]

                if hub.zone == "blocked":
                    continue

                if hub.zone == "restricted":
                    cost = 2
                else:
                    cost = 1

                new_distance = distances[current] + cost

                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    previous[neighbor] = current

        if end not in previous:
            return []

        path = []
        current = end

        while current != start:
            path.append(current)
            current = previous[current]

        path.append(start)
        path.reverse()

        return path
