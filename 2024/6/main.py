from pathlib import Path
from tqdm import tqdm


class Position:
    def __init__(self, value: str):
        # Represent a single position on the map
        self.value = value

    def __str__(self):
        # String repr
        return self.value

    def is_obstacle(self):
        return self.value == "#"

    def is_guard(self):
        return self.value == "^"


class Map:
    def __init__(self, input: Path):
        # Load input into Position objects
        with open(input) as f:
            map_lines = f.readlines()
        self.map = [[Position(val) for val in line.strip()] for line in map_lines]

    def __iter__(self):
        # Iteration method
        for row in self.map:
            yield row

    def __str__(self):
        # String repr
        return "\n".join(["".join([str(pos) for pos in row]) for row in self.map])

    def get_position(self, x: int, y: int):
        # Get the Position object for given coordinates
        if x < 0 or y < 0:
            raise IndexError()
        return self.map[y][x]


class Guard:
    def __init__(self, map: Map):
        self.map = map
        # Find the guard on the map
        self.starting_position = [(i, j) for j, row in enumerate(self.map) for i, position in enumerate(row) if position.is_guard()][0]
        # Initialize starting position and direction
        self.visited_positions = {self.starting_position}
        self.position = self.starting_position
        self.direction = "north"

    def step(self, position: tuple[int, int]) -> tuple[int, int]:
        # Take one step in the current direction
        if self.direction == "north":
            next_position = (position[0], position[1] - 1)
        elif self.direction == "south":
            next_position = (position[0], position[1] + 1)
        elif self.direction == "east":
            next_position = (position[0] + 1, position[1])
        elif self.direction == "west":
            next_position = (position[0] - 1, position[1])
        return next_position

    def rotate(self):
        # Rotate the guard 90 degrees
        rotation = {
            "north": "east",
            "east": "south",
            "south": "west",
            "west": "north",
        }
        self.direction = rotation[self.direction]

    def walk(self):
        next_position = self.step(position=self.position)

        # Get the next position object. If it's off the map, return True indicating walking is done
        try:
            next_position_obj = self.map.get_position(*next_position)
        except IndexError:
            return True

        # If the guard would run into an obstacle, rotate 90 degrees to the right
        if next_position_obj.is_obstacle():
            self.rotate()
            current_position_obj = self.map.get_position(*self.position)
            current_position_obj.value = "+"
        # Otherwise, move to the new position
        else:
            self.position = next_position
            self.visited_positions.add(next_position)
            if self.direction in ["north", "south"]:
                if next_position_obj.value == "-":
                    next_position_obj.value = "+"
                else:
                    next_position_obj.value = "|"
            else:
                if next_position_obj.value == "|":
                    next_position_obj.value = "+"
                else:
                    next_position_obj.value = "-"

        return False


def main():
    # Create Map and Guard
    input = Path(__file__).parent / "input.txt"
    map = Map(input=input)
    guard = Guard(map=map)

    # Have the guard walk until it exits the map
    done = False
    while not done:
        done = guard.walk()

    # Count how many positions were visited
    visited_positions = guard.visited_positions
    total_positions = len(visited_positions)
    print(str(map))
    print("Total Positions:", total_positions)

    positions_to_check = visited_positions.copy()
    positions_to_check.remove(guard.starting_position)
    loop_positions = set()
    for new_obstacle_position in tqdm(positions_to_check, desc="Checking loopable positions"):
        # Put a new obstacle at the visited position, and see if it loops
        map = Map(input=input)
        position = map.get_position(*new_obstacle_position)
        position.value = "#"
        # Create a new guard and have it walk the map
        guard = Guard(map=map)
        counter = {}
        done = False
        while not done:
            done = guard.walk()
            # Count how many times a the position is visited to see if there is a loop
            current_position = guard.position
            if current_position not in counter:
                counter[current_position] = 0
            counter[current_position] += 1
            # Use 4 because a position can be visited from every direction and still not be a loop (and one was)
            if counter[current_position] > 4:
                loop_positions.add(new_obstacle_position)
                done = True

    loopable_positions = len(loop_positions)
    print("Loopable Positions:", loopable_positions)


if __name__ == "__main__":
    main()
