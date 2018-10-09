# !/usr/bin/python3

import random
import string


def generate_word(length):
    VOWELS = "aeiou"
    CONSONANTS = "".join(set(string.ascii_lowercase) - set(VOWELS))
    word = ""
    for i in range(length):
        if i % 2 == 0:
            word += random.choice(CONSONANTS)
        else:
            word += random.choice(VOWELS)
    return word


def get_random_name():
    one_str = generate_word(5)
    two_str = generate_word(6)
    new_name = one_str + " " + two_str
    print(new_name)


get_random_name()
