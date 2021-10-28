import json
import os
from collections import Counter
from typing import Dict

from gensim.models import FastText


def edit_distance(s1: str, s2: str) -> int:
    """Compute edit distance between two strings using dynamic programmic.
    Lifted from: https://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Levenshtein_distance#Python"""
    if len(s1) < len(s2):
        return edit_distance(s2, s1)

    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1  # j+1 instead of j since previous_row and
            # current_row are one character longer than s2
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


def load_vocab(json_filepath: str) -> Counter:
    """Load vocab from json file"""
    with open(json_filepath, 'r', encoding='utf-8') as f:
        s = f.read()
    vocab_dict = json.loads(s)
    vocab_counter = Counter(vocab_dict)
    return vocab_counter


def find_correct_spelling(model: FastText, incorrect_word: str, num_neighbours: int, clean_vocab_counter: Counter,
                          mixed_vocab_counter: Counter, mixed_vocab_min_freq: int,
                          max_edit_distance: int) -> Dict[str, str]:
    """Find correct spelling for a given word which is incorrectly spelled"""

    correct_word, message = '', ''

    mixed_vocab_set = set()
    for word, freq in mixed_vocab_counter.most_common():
        if freq >= mixed_vocab_min_freq:
            mixed_vocab_set.add(word)

    if incorrect_word in clean_vocab_counter or incorrect_word in mixed_vocab_set:
        message = f'{incorrect_word} is already correctly spelled'
    else:
        tups = model.wv.most_similar(incorrect_word, topn=num_neighbours)
        candidates = [candidate for candidate, _ in tups]

        for candidate in candidates:
            if candidate in clean_vocab_counter and edit_distance(incorrect_word, candidate) <= max_edit_distance:
                correct_word = candidate
                break

        if correct_word == '':
            for candidate in candidates:
                if candidate in mixed_vocab_set and edit_distance(incorrect_word, candidate) <= max_edit_distance:
                    correct_word = candidate
                    break
        if correct_word == '':
            message = 'Correct spelling not found'
    return {'incorrect_word': incorrect_word, 'correct_word': correct_word, 'message': message}


if __name__ == "__main__":
    _incorrect_word = 'ସାପ୍ତାହୀକ'
    _num_neighbours = 10
    _mixed_vocab_min_freq = 50
    _max_edit_distance = 2

    _model = FastText.load(os.path.join('embeddings.txt'))
    _clean_vocab_counter = load_vocab(os.path.join('clean_vocab_counter.json'))
    _mixed_vocab_counter = load_vocab(os.path.join('mixed_vocab_counter.json'))
    out = find_correct_spelling(model=_model, incorrect_word=_incorrect_word, num_neighbours=_num_neighbours,
                                clean_vocab_counter=_clean_vocab_counter,
                                mixed_vocab_counter=_mixed_vocab_counter, mixed_vocab_min_freq=_mixed_vocab_min_freq,
                                max_edit_distance=_max_edit_distance)
    print(out)
