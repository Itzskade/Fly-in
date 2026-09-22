"""Parser for Fly-in map files."""

from .connection import Connection
from .drone import Drone
from .hub import Hub


class MapParser:
    """Parse Fly-in map files."""

    def __init__(self, filename: str) -> None:
        """Initialize the parser."""
        self.filename = filename

    def parse(self) -> dict:
        """Parse the map file."""
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                lines = file.readlines()

            nb_drones = None
            hubs = {}
            connections = []
            start_hub = None
            end_hub = None

            for line_number, line in enumerate(lines, 1):
                line = line.split("#")[0].strip()

                if not line:
                    continue

                if line.startswith("nb_drones:"):
                    value = line.split(":", 1)[1].strip()
                    nb_drones = int(value)

                    if nb_drones <= 0:
                        raise ValueError(
                            "nb_drones must be positive"
                        )

                elif line.startswith("start_hub:"):
                    hub = self._parse_hub(line, "start_hub")

                    if start_hub is not None:
                        raise ValueError(
                            "multiple start_hub definitions"
                        )

                    if hub.name in hubs:
                        raise ValueError(
                            f"duplicate hub: {hub.name}"
                        )

                    hubs[hub.name] = hub
                    start_hub = hub

                elif line.startswith("end_hub:"):
                    hub = self._parse_hub(line, "end_hub")

                    if end_hub is not None:
                        raise ValueError(
                            "multiple end_hub definitions"
                        )

                    if hub.name in hubs:
                        raise ValueError(
                            f"duplicate hub: {hub.name}"
                        )

                    hubs[hub.name] = hub
                    end_hub = hub

                elif line.startswith("hub:"):
                    hub = self._parse_hub(line, "hub")

                    if hub.name in hubs:
                        raise ValueError(
                            f"duplicate hub: {hub.name}"
                        )

                    hubs[hub.name] = hub

                elif line.startswith("connection:"):
                    connection = self._parse_connection(
                        line,
                        hubs,
                    )
                    connections.append(connection)

                else:
                    raise ValueError(
                        f"unknown line: {line}"
                    )

            if nb_drones is None:
                raise ValueError("missing nb_drones")

            if start_hub is None:
                raise ValueError("missing start_hub")

            if end_hub is None:
                raise ValueError("missing end_hub")

            drones = []

            for number in range(1, nb_drones + 1):
                drones.append(
                    Drone(
                        f"D{number}",
                        start_hub.name,
                        end_hub.name,
                    )
                )

            return {
                "nb_drones": nb_drones,
                "hubs": hubs,
                "connections": connections,
                "drones": drones,
                "start_hub": start_hub,
                "end_hub": end_hub,
            }

        except (OSError, ValueError) as error:
            raise ValueError(
                f"Error parsing map: {error}"
            ) from error

    def _parse_hub(
        self,
        line: str,
        hub_type: str,
    ) -> Hub:
        """Parse a hub definition."""
        data = line.split(":", 1)[1].strip()

        if "[" in data:
            values, metadata = data.split("[", 1)
            metadata = metadata.rstrip("]").strip()
        else:
            values = data
            metadata = ""

        parts = values.strip().split()

        if len(parts) != 3:
            raise ValueError(
                f"invalid {hub_type} syntax"
            )

        name = parts[0]
        x = int(parts[1])
        y = int(parts[2])

        if "-" in name or " " in name:
            raise ValueError(
                f"invalid hub name: {name}"
            )

        zone = "normal"
        color = "none"
        max_drones: int | None = 1

        for item in metadata.split():
            key, value = item.split("=", 1)

            if key == "zone":
                if value not in Hub.VALID_ZONES:
                    raise ValueError(
                        f"invalid zone: {value}"
                    )
                zone = value

            elif key == "color":
                color = value

            elif key == "max_drones":
                max_drones = int(value)

                if max_drones <= 0:
                    raise ValueError(
                        "max_drones must be positive"
                    )

        if hub_type in ("start_hub", "end_hub"):
            max_drones = None

        return Hub(
            name,
            x,
            y,
            color,
            zone,
            max_drones,
        )

    def _parse_connection(
        self,
        line: str,
        hubs: dict,
    ) -> Connection:
        """Parse a connection definition."""
        data = line.split(":", 1)[1].strip()

        if "[" in data:
            values, metadata = data.split("[", 1)
            metadata = metadata.rstrip("]").strip()
        else:
            values = data
            metadata = ""

        parts = values.strip().split("-")

        if len(parts) != 2:
            raise ValueError("invalid connection")

        first, second = parts

        if first not in hubs or second not in hubs:
            raise ValueError(
                "connection references unknown hub"
            )

        max_capacity = 1

        for item in metadata.split():
            key, value = item.split("=", 1)

            if key == "max_link_capacity":
                max_capacity = int(value)

                if max_capacity <= 0:
                    raise ValueError(
                        "max_link_capacity must be positive"
                    )

        return Connection(
            hubs[first],
            hubs[second],
            max_capacity,
        )
