"""
File: anagram.py
Name:Jim Chan
----------------------------------
This program recursively finds all the anagram(s)
for the word input by user and terminates when the
input string matches the EXIT constant defined
at line 19

If you correctly implement this program, you should see the
number of anagrams for each word listed below:
    * arm -> 3 anagrams
    * contains -> 5 anagrams
    * stop -> 6 anagrams
    * tesla -> 10 anagrams
    * spear -> 12 anagrams
"""

# Constants
FILE = 'dictionary.txt'  # This is the filename of an English dictionary
EXIT = '-1'  # Controls when to stop the loop
DICT = []  # lst holding all the words in the FILE


def main():
    print('Welcome to stanCode \"Anagram Generator\" (or -1 to quit)')
    read_dictionary()
    while True:
        word = input('Find anagrams for: ')
        word = word.lower()
        # making sure the program works even the inputted word contains upper cases
        if word == EXIT:
            break
        if error_format(word):
            print('Error format')
        else:
            print('Searching...')
            dict_new = []
            dict_n2 = []
            # narrowing the DICT down to words that start with the letter in inputted word.
            for letter in word:
                if has_prefix(letter):
                    global DICT
                    for words in DICT:
                        if words.startswith(letter):
                            dict_new.append(words)
            # narrowing the DICT down to words that have the same length as the inputted word.
            for words in dict_new:
                if len(words) == len(word):
                    dict_n2.append(words)
            DICT = dict_n2
            anagram = []
            for target in find_anagrams(word):
                # print('Found: ' + target)
                # print('Searching...')
                anagram += [target]
            print(len(anagram), 'anagrams: ', anagram)
            # returning the DICT to original status
            read_dictionary()


def error_format(search):
    """
    :param search: inputted word
    :return: bool.
    Checking every element in the inputted word is in alphabet.
    """
    for letter in search:
        if letter.isalpha() is False:
            return True


def read_dictionary():
    """
    This function creates a list with words in FILE, assigning to the global variable DICT.
    """
    global DICT
    with open(FILE, mode='r') as f:
        for line in f:
            if line != '':
                DICT.append(line[0:len(line) - 1])


def find_anagrams(s):
    """
    :param s: str. inputted word
    :return: lst. the anagrams of the inputted word
    """
    anagram_list = []
    find_anagrams_helper(s, anagram_list, '')
    return anagram_list


def find_anagrams_helper(s, anagram_lst, new_s):
    if len(new_s) == len(s):
        # print(new_s)
        if new_s not in anagram_lst:
            print('Found: ' + new_s)
            print('Searching...')
            anagram_lst.append(new_s)
    else:
        for letter in s:
            if letter_occurrence(letter, new_s) != letter_occurrence(letter, s):
                new_s += letter
                if has_prefix(new_s):
                    find_anagrams_helper(s, anagram_lst, new_s)
                new_s = new_s[0:len(new_s) - 1]


def letter_occurrence(letter, new_s):
    """
    :param letter: str. the letter in new_s
    :param new_s: str. the created word
    :return: int. the number of occurrence of the letter in the new_s
    """
    times = 0
    for each_letter in new_s:
        if each_letter == letter:
            times += 1
    return times


def has_prefix(sub_s):
    """
    :param sub_s: str. the beginning words
    :return: bool.
    """
    for word in DICT:
        if word.startswith(sub_s):
            return True
    return False


if __name__ == '__main__':
    main()
