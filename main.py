#!/usr/bin/env python3

from typing import Dict, List
from enum import Enum
import sys

class Feedback(Enum):
    NOT_IN_WORD = 1
    WRONG_POSITION = 2
    EXACT_POSITION = 3

class LetterFeedback:
    letter: str
    feedback: Feedback

    def __init__(self, letter: str, feedback: Feedback):
        self.letter = letter
        self.feedback = feedback

class WordFeedback:
    letters: List[LetterFeedback]

    def __init__(self, letters: List[LetterFeedback]):
        self.letters = letters

def read_word_list() -> List[str]:
    words = []
    with open("/usr/share/dict/words") as wordfile:
        for line in wordfile:
            word = line.strip()
            if len(word) == 5:
                words.append(word)
    return words

def compute_letter_frequency(wordlist: List[str]) -> Dict[str, int]:
    letter_histogram = {}
    for word in wordlist:
        for letter in word:
            current_count = letter_histogram.get(letter, 0)
            letter_histogram[letter] = current_count + 1
    return letter_histogram

def wordscore(word: str, letter_frequency: Dict[str, int]) -> int:
    value = 0
    for letter in word:
        value += letter_frequency.get(letter, 0)
    return value

def word_has_only_unique_letters(word: str) -> bool:
    return len(set(letter for letter in word)) == 5

def suggest_word(wordlist: List[str], letter_frequency: Dict[str, int], initial_guess: bool) -> str:
    word_scores = [(word, wordscore(word, letter_frequency)) for word in wordlist]

    if initial_guess:
        word_scores = [wordscore for wordscore in word_scores if word_has_only_unique_letters(wordscore[0])]

    return max(word_scores, key=lambda x: x[1])[0]

def parse_feedback(result: str, word: str) -> WordFeedback:
    result_parse = {
        "x": Feedback.NOT_IN_WORD,
        "y": Feedback.WRONG_POSITION,
        "g": Feedback.EXACT_POSITION,
        "b": Feedback.WRONG_POSITION,
        "o": Feedback.EXACT_POSITION,
    }
    feedbacks = [result_parse[letter] for letter in result]
    letter_feedback = [LetterFeedback(z[0], z[1]) for z in zip(word, feedbacks)]
    return WordFeedback(letter_feedback)

def process_wordlist_with_feedback(wordlist: List[str], feedback: WordFeedback) -> List[str]:
    letters_with_position = []

    filtered_wordlist = wordlist

    for index, letter in enumerate(feedback.letters):
        if letter.feedback == Feedback.NOT_IN_WORD:
            # There are two cases where a word can be black: Not in word, OR, too much of that letter in the word.
            number = len([l for l in feedback.letters if letter.letter == l.letter and l.feedback != Feedback.NOT_IN_WORD])
            filtered_wordlist = [word for word in filtered_wordlist if word.count(letter.letter) == number]
        if letter.feedback == Feedback.WRONG_POSITION:
            filtered_wordlist = [word for word in filtered_wordlist if (letter.letter in word) and (word[index] != letter.letter)]
        if letter.feedback == Feedback.EXACT_POSITION:
            filtered_wordlist = [word for word in filtered_wordlist if word[index] == letter.letter]

    return filtered_wordlist


def main():
    print("Provide feedback in terms of initial of color of feedback. Use 'x' for when the letter is marked as black. This script does recognize the high-contrast colors. e.g. xxygx if the result was 'black', 'black', 'yellow', 'green', black'. Hit ^D (control+D) if you've solved it. Type \"invalid\" if the suggested word is not in wordle's word bank.")
    initial_word_list = read_word_list()
    letter_freq = compute_letter_frequency(initial_word_list)

    wordlist = initial_word_list
    all_feedback = []

    while True:
        suggested_word = suggest_word(wordlist, letter_freq, len(all_feedback) == 0)
        print("Try the word \"{}\"".format(suggested_word))
        # get feedback
        try:
            result = input("How was it? ").strip()
        except EOFError:
            print("Congratulations!")
            return
        if result.lower() == "invalid":
            wordlist = [word for word in wordlist if word != suggested_word]
            continue
        word_feedback = parse_feedback(result, suggested_word)
        if all(lf.feedback == Feedback.EXACT_POSITION for lf in word_feedback.letters):
            print("Congratulations!")
            return
        wordlist = process_wordlist_with_feedback(wordlist, word_feedback)
        all_feedback.append(word_feedback)

if __name__ == "__main__":
    main()
