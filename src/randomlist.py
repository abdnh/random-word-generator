import argparse
import sys
import random
import os

WORDLIST_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "wordlists")

wordlists = {}


def get_wordlist_labels():
    files = []
    for file in os.listdir(WORDLIST_DIR):
        if file.endswith(".txt"):
            file = file[:-4]
            files.append(file)

    return files


def get_wordlist(label: str):
    if words := wordlists.get(label, None):
        return words
    else:
        filename = os.path.join(WORDLIST_DIR, label + ".txt")
        with open(filename, encoding="utf-8") as f:
            words = f.read().split()
            wordlists[label] = words
            return words


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
