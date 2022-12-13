import collections
import hashlib
from pathlib import Path
import sys
import typing


def get_root_dir() -> Path:
    if len(sys.argv) < 2:
        print("Directory is not specified")
        sys.exit()
    return Path(sys.argv[1])


def get_ext() -> str:
    ext = input("Enter file format:\n")
    print()
    return ext


def get_sort_order() -> bool:
    while True:
        print(
            "Size sorting options:\n"
            "1. Descending\n"
            "2. Ascending\n"
        )
        sort = input("Enter a sorting option:\n")
        print()

        if sort == "1":
            return True
        elif sort == "2":
            return False
        else:
            print("Wrong option\n")
            continue


def get_matches(root_dir: Path, ext: str) -> typing.DefaultDict[int, Path]:
    matches = collections.defaultdict(list)
    for f in root_dir.glob("**/*"):
        if not f.is_file():
            continue
        if ext != "" and f.suffix != ext:
            continue
        matches[f.stat().st_size].append(f)
    return matches


def print_matches(matches: typing.DefaultDict[int, Path], reverse: bool) -> None:
    keys = sorted(matches.keys(), reverse=reverse)
    for k in keys:
        print(f"{k} bytes")
        for j in matches[k]:
            print(j)
        print()


def get_check_for_duplicates() -> bool:
    while True:
        response = input("Check for duplicates?\n")
        if response == "yes":
            return True
        elif response == "no":
            return False
        else:
            print("Wrong option")
            continue


def print_duplicates(matches: typing.DefaultDict[int, Path], reverse: bool) -> None:
    count = 0
    print()
    keys = sorted(matches.keys(), reverse=reverse)
    for k in keys:
        hashed = collections.defaultdict(list)
        print(f"{k} bytes")
        for p in matches[k]:
            with open(p, "rb") as f:
                h = hashlib.md5(f.read()).hexdigest()
            hashed[h].append(p)
        for h, v in hashed.items():
            if len(v) <= 1:
                continue
            print(f"Hash: {h}")
            for a in v:
                count += 1
                print(f"{count}. {a}")
            print()


root_dir = get_root_dir()
ext = get_ext()
reverse = get_sort_order()

matches = get_matches(root_dir, ext)
print_matches(matches, reverse)
check_for_duplicates = get_check_for_duplicates()
if check_for_duplicates:
    print_duplicates(matches, reverse)
