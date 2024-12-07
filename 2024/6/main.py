from pathlib import Path
from tqdm import tqdm


class Position:
    def __init__(self, value: str):
        self.value = value

    def __str__(self):
        return self.value

    def is_obstacle(self):
        return self.value == "#"

    def is_guard(self):
        return self.value == "^"


class Map:
    def __init__(self, input: Path):
        with open(input) as f:
            map_lines = f.readlines()
        self.map = [[Position(val) for val in line.strip()] for line in map_lines]

    def __iter__(self):
        for row in self.map:
            yield row

    def __str__(self):
        return "\n".join(["".join([str(pos) for pos in row]) for row in self.map])

    def get_position(self, x: int, y: int):
        if x < 0 or y < 0:
            raise IndexError()
        return self.map[y][x]


class Guard:
    def __init__(self, map: Map):
        self.map = map
        self.starting_position = [(i, j) for j, row in enumerate(self.map) for i, position in enumerate(row) if position.is_guard()][0]
        self.visited_positions = {self.starting_position}
        self.position = self.starting_position
        self.direction = "north"
        self.rotate = {
            "north": "east",
            "east": "south",
            "south": "west",
            "west": "north",
        }

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

    def walk(self):
        next_position = self.step(position=self.position)

        # Get the next position object. If it's off the map, return True indicating walking is done
        try:
            next_position_obj = self.map.get_position(*next_position)
        except IndexError:
            return True

        # If the guard would run into an obstacle, rotate 90degrees to the right
        if next_position_obj.is_obstacle():
            self.direction = self.rotate[self.direction]
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
    input = Path(__file__).parent / "input.txt"
    map = Map(input=input)
    guard = Guard(map=map)
    done = False
    while not done:
        done = guard.walk()

    visited_positions = guard.visited_positions
    total_positions = len(visited_positions)
    print(str(map))
    print("Total Positions:", total_positions)

    positions_to_check = visited_positions.copy()
    positions_to_check.remove(guard.starting_position)
    loop_positions = set()
    for new_obstacle_position in tqdm(positions_to_check, desc="Checking loopable positions"):
        # Put a new obstacle at the visited position
        map = Map(input=input)
        position = map.get_position(*new_obstacle_position)
        position.value = "#"
        guard = Guard(map=map)
        counter = {}
        done = False
        while not done:
            done = guard.walk()
            current_position = guard.position
            if current_position not in counter:
                counter[current_position] = 0
            counter[current_position] += 1
            if counter[current_position] > 4:
                loop_positions.add(new_obstacle_position)
                done = True

    loopable_positions = len(loop_positions)
    print("Loopable Positions:", loopable_positions)


if __name__ == "__main__":
    main()
