import collections
import hashlib
from pathlib import Path
import sys
import typing


def get_root_dir_response() -> Path:
    if len(sys.argv) < 2:
        print("Directory is not specified")
        sys.exit()
    return Path(sys.argv[1])


def get_ext_response() -> str:
    ext = input("Enter file format:\n")
    print()
    if ext == "" or ext.startswith("."):
        return ext
    return "." + ext


def get_sort_order_response() -> bool:
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


def get_matches(root_dir: Path, ext: str) -> typing.DefaultDict[int, typing.List[Path]]:
    matches = collections.defaultdict(list)
    for f in root_dir.glob("**/*"):
        if not f.is_file():
            continue
        if ext != "" and f.suffix != ext:
            continue
        matches[f.stat().st_size].append(f)
    return matches


def sort_matches(matches: typing.DefaultDict[int, typing.List[Path]], reverse: bool) -> typing.Dict[
    int, typing.List[Path]]:
    keys = sorted(matches.keys(), reverse=reverse)

    matches_sorted = {}
    for k in keys:
        v = matches[k]
        matches_sorted[k] = v
    return matches_sorted


def print_matches(matches: typing.Dict[int, typing.List[Path]]) -> None:
    for k, v in matches.items():
        print(f"{k} bytes")
        for p in v:
            print(p)
        print()


def get_check_for_duplicates_response() -> bool:
    while True:
        response = input("Check for duplicates?\n")
        if response == "yes":
            return True
        elif response == "no":
            return False
        else:
            print("Wrong option")
            continue


def get_and_print_duplicates(matches: typing.Dict[int, typing.List[Path]]) -> typing.Dict[int, Path]:
    count = 0
    dups = {}
    print()
    for k, v in matches.items():
        hashed = collections.defaultdict(list)
        print(f"{k} bytes")
        for p in v:
            with open(p, "rb") as f:
                h = hashlib.md5(f.read()).hexdigest()
            hashed[h].append(p)
        for h, v in hashed.items():
            if len(v) <= 1:
                continue
            print(f"Hash: {h}")
            for a in v:
                count += 1
                dups[count] = a
                print(f"{count}. {a}")
            print()
    return dups


def get_delete_duplicates_response() -> bool:
    while True:
        response = input("Delete files?\n")
        if response == "yes":
            print()
            return True
        elif response == "no":
            print()
            return False
        else:
            print("Wrong option")
        continue


def get_and_sort_matches() -> typing.Dict[int, typing.List[Path]]:
    # get user input
    root_dir = get_root_dir_response()
    ext = get_ext_response()
    is_reversed = get_sort_order_response()

    # get matches
    matches = get_matches(root_dir, ext)

    # sort matches
    return sort_matches(matches, is_reversed)


def delete_duplicates(dups: typing.Dict[int, Path]) -> None:
    freed_space = 0
    while True:
        try:
            nbrs = [int(i) for i in input("Enter file numbers to delete:\n").split(" ")]
            for nbr in nbrs:
                if nbr not in dups:
                    raise ValueError
        except ValueError:
            print("\nWrong format\n")
            continue
        print()
        break

    for nbr in nbrs:
        f = dups.get(nbr, None)
        if not f:
            continue
        freed_space += f.stat().st_size
        f.unlink()
    print(f"Total freed up space: {freed_space} bytes")


if __name__ == "__main__":
    matches = get_and_sort_matches()
    print_matches(matches)
    check_for_duplicates = get_check_for_duplicates_response()
    if not check_for_duplicates:
        exit()
    duplicates = get_and_print_duplicates(matches)
    should_delete_duplicates = get_delete_duplicates_response()
    if not should_delete_duplicates:
        exit()
    print(duplicates)
    delete_duplicates(duplicates)
