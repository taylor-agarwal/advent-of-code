from pathlib import Path
from tqdm import tqdm
from typing import Set


class Position:
    def __init__(self, x: int, y: int, value: str):
        # Represent a single position on the map
        self.x = x
        self.y = y
        self.value = value

    def __eq__(self, other):
        if not isinstance(other, Position):
            return False
        return not self.is_antenna() and self.value == other.value

    def __hash__(self):
        return int((self.x + self.y) * (self.x + self.y + 1) / 2 + self.x)

    def __repr__(self):
        return f"Position({self.x=}, {self.y=}, {self.value})"

    def __str__(self):
        # String repr
        return self.value

    def is_antenna(self):
        return self.value != "." and self.value != "#"

    def is_antinode(self):
        return self.value == "#"


class Map:
    def __init__(self, input: Path):
        # Load input into Position objects
        with open(input) as f:
            map_lines = f.readlines()

        self.map = [[Position(x=x, y=y, value=val) for x, val in enumerate(line.strip())] for y, line in enumerate(map_lines)]
        self.positions = [pos for line in self.map for pos in line]

    def __iter__(self):
        # Iteration method
        for position in self.positions:
            yield position

    def __str__(self):
        # String repr
        return "\n".join(["".join([str(pos) for pos in row]) for row in self.map])

    def get_position(self, x: int, y: int):
        # Get the Position object for given coordinates
        position = [position for position in self.positions if position.x == x and position.y == y]
        return position[0]


class AntinodeDetector:
    def __init__(self, map: Map):
        self.map = map

    def antenna2matches(self):
        # Create a mapping of antennas to their matching antennas a0 -> [a1, a2, ...]
        antenna2matches: dict[Position, Set[Position]] = {}
        for position in self.map:
            if position.is_antenna():
                antenna = position
                matching_antennae = [ant for ant in antenna2matches.keys() if ant.value == antenna.value]
                antenna2matches[antenna] = set()
                for matching_antenna in matching_antennae:
                    antenna2matches[matching_antenna].add(antenna)
                    antenna2matches[antenna].add(matching_antenna)
        return antenna2matches

    def antinode_position(self, pos1: Position, pos2: Position, scale: int = 1):
        # Determine antinode coordinates
        if pos1.x < pos2.x:
            antinode_x = pos1.x - (scale * (pos2.x - pos1.x))
        else:
            antinode_x = pos1.x + (scale * (pos1.x - pos2.x))
        if pos1.y < pos2.y:
            antinode_y = pos1.y - (scale * (pos2.y - pos1.y))
        else:
            antinode_y = pos1.y + (scale * (pos1.y - pos2.y))
        return self.map.get_position(x=antinode_x, y=antinode_y)

    def draw_antinodes(self):
        # Draw antinodes
        for antenna, matching_antennae in self.antenna2matches().items():
            for matching_antenna in matching_antennae:
                # Get the antinode position if it exists
                try:
                    antinode_position = self.antinode_position(pos1=antenna, pos2=matching_antenna)
                except IndexError:
                    continue

                # Set the position value to antinode
                antinode_position.value = "#"

    def draw_antinodes_resonance(self):
        for antenna, matching_antennae in self.antenna2matches().items():
            for matching_antenna in matching_antennae:
                # Set a starting scale of 1, increasing by 1 after each drawn antinode to generate the line
                scale = 1
                while True:
                    # Get the antinode position if it exists
                    try:
                        antinode_position = self.antinode_position(pos1=antenna, pos2=matching_antenna, scale=scale)
                    except IndexError:
                        break

                    # Set the position value to antinode
                    antinode_position.value = "#"

                    # Increase the scale
                    scale += 1


def main():
    # Part 1
    input = Path(__file__).parent / "input.txt"
    map = Map(input=input)
    detector = AntinodeDetector(map=map)
    detector.draw_antinodes()

    total_antinodes = sum([1 for position in map if position.is_antinode()])
    print(str(map))
    print("Total Antinodes:", total_antinodes)

    # Part2
    input = Path(__file__).parent / "input.txt"
    map = Map(input=input)
    detector = AntinodeDetector(map=map)
    detector.draw_antinodes_resonance()

    total_antinodes = sum([1 for position in map if position.is_antinode()])
    print(str(map))
    print("Total Antinodes (With Resonance):", total_antinodes)


if __name__ == "__main__":
    main()
