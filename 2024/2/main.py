from pathlib import Path


class Report:
    def __init__(self, lst: list[int]):
        self.lst = lst

    def is_safe(self):
        # If start == end then we know it's not increasing or decreasing and is unsafe
        start, end = self.lst[0], self.lst[-1]
        if start == end:
            return 0
        # If the changes are between 1 and 3, all increasing or decreasing, then it is safe
        changes = [b - a for a, b in zip(self.lst[:-1], self.lst[1:])]
        all_increasing = all(1 <= change and change <= 3 for change in changes)
        all_decreasing = all(-1 >= change and change >= -3 for change in changes)
        if all_increasing or all_decreasing:
            return 1
        return 0

    def is_safe_dampened(self):
        # Follows the same rules as is_safe
        if self.is_safe():
            return 1
        # But if removing any level produces a safe report, then it is safe
        one_level_removed_reports = [Report(self.lst[:i] + self.lst[i + 1 :]) for i in range(len(self.lst))]
        if any(rept.is_safe() for rept in one_level_removed_reports):
            return 1
        return 0


class Data:
    def __init__(self, path: Path):
        # Parse the input into lists of ints
        with open(path) as f:
            self.lines = f.readlines()
        reports = [[int(val) for val in rept.split()] for rept in self.lines]

        # Make report objects
        self.reports = [Report(rept) for rept in reports]

    def count_safe(self):
        return sum([rept.is_safe() for rept in self.reports])

    def count_safe_dampened(self):
        return sum([rept.is_safe_dampened() for rept in self.reports])


def part_one(data: Data):
    print(data.count_safe())


def part_two(data: Data):
    print(data.count_safe_dampened())


def main():
    path = Path(__file__).parent / "input.txt"
    data = Data(path)
    part_one(data)
    part_two(data)


if __name__ == "__main__":
    main()
