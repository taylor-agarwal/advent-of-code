import re
from pathlib import Path


def extract_muls(text: str):
    pattern = r"mul\([0-9]+,[0-9]+\)"
    matches = re.findall(pattern=pattern, string=text)
    return matches

def extract_muls_and_dos(text: str):
    pattern = r"mul\([0-9]+,[0-9]+\)|do\(\)|don't\(\)"
    matches = re.findall(pattern=pattern, string=text)
    return matches
    
def total_muls(muls: list[str]):
    total = 0
    for mul in muls:
        mul = mul.strip("mul()")
        a, b = mul.split(",")
        total += int(a) * int(b)
    return total

def total_muls_and_dos(muls: list[str]):
    total = 0
    count = True
    for mul in muls:
        if mul == "do()":
            count = True
        elif mul == "don't()":
            count = False
        elif count:
            mul = mul.strip("mul()")
            a, b = mul.split(",")
            total += int(a) * int(b)
    return total
    
def part_one(text: str):
    muls = extract_muls(text)
    total = total_muls(muls)
    print(total)
    
    
def part_two(text: str):
    muls_and_dos = extract_muls_and_dos(text)
    total = total_muls_and_dos(muls_and_dos)
    print(total)
    
    
def main():
    path = Path(__file__).parent / "input.txt"
    text = path.read_text()
    part_one(text)
    part_two(text)
    


if __name__ == "__main__":
    main()
