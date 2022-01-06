import argparse
import sys
import random
import os
from typing import Optional, List, Set

wordlist_dirs = [
    os.path.join(os.path.dirname(__file__), "user_files/wordlists"),
    os.path.join(os.path.dirname(__file__), "default_wordlists"),
]

wordlists = {}


def get_wordlist_labels() -> Set[str]:
    labels = set()
    for wordlist_dir in wordlist_dirs:
        if not os.path.exists(wordlist_dir):
            continue
        for file in os.listdir(wordlist_dir):
            if file.endswith(".txt"):
                file = file[:-4]
                labels.add(file)

    return labels


def get_wordlist_filename_from_label(label: str) -> Optional[str]:
    for wordlist_dir in wordlist_dirs:
        filename = os.path.join(wordlist_dir, label + ".txt")
        if os.path.exists(filename):
            return filename
    return None


def get_wordlist(label: str) -> List[str]:
    if words := wordlists.get(label):
        return words
    else:
        filename = get_wordlist_filename_from_label(label)
        if filename:
            with open(filename, encoding="utf-8") as f:
                words = f.read().split()
                wordlists[label] = words
                return words
        return []


def randomlist(words, start=0, end=-1, length=7):
    start = int(start)
    end = int(end)
    length = int(length)
    if end == -1:
        end = len(words)
    words = words[start:end]
    length = length if length <= len(words) else len(words)
    chosen = random.sample(words, k=length)
    return chosen


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="generate a random list of words from an input file"
    )
    parser.add_argument("file")
    parser.add_argument(
        "-l", "--length", type=int, default=7, help="length of generated list"
    )
    parser.add_argument(
        "-s",
        "--start",
        type=int,
        default=0,
        help="position in input list to start choosing words from",
    )
    parser.add_argument(
        "-e",
        "--end",
        type=int,
        default=-1,
        help="position in input list to limit chosen words to the ones before it",
    )

    args = parser.parse_args()

    if args.file == "-":
        infile = sys.stdin
    else:
        infile = open(args.file)

    words = infile.read().split()
    chosen = randomlist(words, args.start, args.end, args.length)
    print(" ".join(chosen))
