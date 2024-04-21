# from typing import LiteralString

Puzzle = dict[
    str,
    tuple[
        str,
        str,
        str,
        str,
        str,
        str,
        str,
        str,
        str,
    ],
]


def load_words() -> dict[str, list[str]]:
    alphabet = {}
    with open("collins_scrabble_words.txt", "r") as f:
        words = [word.strip().lower() for word in f]
        letter = words[0][0]
        start = 0
        i = 1
        while i < len(words):
            if words[i][0] != letter:
                alphabet[letter] = words[start:i]
                letter = words[i][0]
                start = i + 1
                i += 1
            i += 1
        alphabet[letter] = words[start:]
    return alphabet


def load_puzzle() -> Puzzle:
    while True:
        line = input()
        # line = "ghzbrtiakepl"
        if len(line) != 12:
            print("input exactly 12 characters")
            continue
        if not line.isalpha():
            print("please input only letters")
            continue
        [a1, a2, a3, b1, b2, b3, c1, c2, c3, d1, d2, d3] = line.lower()
        puzzle = {
            a1: (b1, b2, b3, c1, c2, c3, d1, d2, d3),
            a2: (b1, b2, b3, c1, c2, c3, d1, d2, d3),
            a3: (b1, b2, b3, c1, c2, c3, d1, d2, d3),
            b1: (a1, a2, a3, c1, c2, c3, d1, d2, d3),
            b2: (a1, a2, a3, c1, c2, c3, d1, d2, d3),
            b3: (a1, a2, a3, c1, c2, c3, d1, d2, d3),
            c1: (a1, a2, a3, b1, b2, b3, d1, d2, d3),
            c2: (a1, a2, a3, b1, b2, b3, d1, d2, d3),
            c3: (a1, a2, a3, b1, b2, b3, d1, d2, d3),
            d1: (a1, a2, a3, b1, b2, b3, c1, c2, c3),
            d2: (a1, a2, a3, b1, b2, b3, c1, c2, c3),
            d3: (a1, a2, a3, b1, b2, b3, c1, c2, c3),
        }
        if len(puzzle) != 12:
            print("no duplicate letters allowed")
            continue
        return puzzle


def is_legal(puzzle: Puzzle, word: str) -> bool:
    if word[0] not in puzzle.keys():
        return False
    options = puzzle[word[0]]
    for letter in word[1:]:
        if letter not in options:
            return False
        options = puzzle[letter]
    return True


def search(
    words: list[str],
    used_words: list[str],
    missing_letters: list[str],
    starting_letter: str,
    max_depth: int,
):
    if not missing_letters:
        yield []
    if max_depth <= len(used_words):
        return
    best_words = []
    for word in words:
        if word in used_words:
            continue
        if not word.startswith(starting_letter):
            continue
        new_missing_letters = [
            letter for letter in missing_letters if letter not in word
        ]
        if len(new_missing_letters) < len(missing_letters):
            best_words.append((word, new_missing_letters))
    best_words.sort(key=lambda tup: len(tup[1]))
    for word, new_missing_letters in best_words:
        for search_result in search(
            words, used_words +
                [word], new_missing_letters, word[-1], max_depth
        ):
            yield [word] + search_result


def main():
    word_map = load_words()
    puzzle = load_puzzle()

    words = []
    for letter in puzzle.keys():
        for word in word_map[letter]:
            if is_legal(puzzle, word):
                words.append(word)
    words.sort(key=lambda w: -len(w))

    max_depth = 1
    while True:
        print(f"checking depth {max_depth}")
        solutions = []
        for letter in puzzle.keys():
            solutions += list(
                search(
                    words,
                    [],
                    list(puzzle.keys()),
                    letter,
                    max_depth,
                )
            )
        if solutions:
            for s in solutions:
                print(s)
            return
        max_depth += 1
