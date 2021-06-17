"""
File: boggle.py
Name: Jim Chan
----------------------------------------
This program runs a boggle game, in which players attempt to find words in sequences of adjacent letters.
"""

# This is the file name of the dictionary txt file
# we will be checking if a word exists by searching through it
FILE = 'dictionary.txt'
DICT = {}

# DICT = {(1, 1): 'f', (1, 2): 'y', (1, 3): 'c', (1, 4): 'l', (2, 1): 'i', (2, 2): 'o', (2, 3): 'm', (2, 4): 'g',
#         (3, 1): 'o', (3, 2): 'r', (3, 3): 'i', (3, 4): 'l', (4, 1): 'h', (4, 2): 'j', (4, 3): 'h', (4, 4): 'u'}
DICTIONARY = []


def main():
    """
    User will input 4 rows of letter with space between each letter, and the program will find all the word(s)
    for the letters input by user.

    If the user correctly implement this program, you should see the
    possible words for the 4 rows of letters below:
    Found "xxx"
    There are X words in total.
    """
    letters = []
    read_dictionary()
    boggle_dict = {}
    for j in range(1, 5, 1):
        for k in range(1, 5, 1):
            boggle_dict[(j, k)] = ''
    # Initializing the dictionary for the letters the user will input
    for i in range(1, 5, 1):
        while True:
            a = (input(f'{i} row of letters: '))
            if check(a):
                for l in range(1, 5, 1):
                    boggle_dict[(i, l)] = (a.lower().split(' '))[l - 1]
                    letters.append(boggle_dict[(i, l)])
                break
            else:
                print('Illegal input')
    # Requesting user to input letter, and return the input if it is not in correct order.
    global DICT
    DICT = boggle_dict
    path = []
    # Recording the path of the searching spots, avoiding searching at the same spot.
    found_lst = []
    # Recording the words that were found.
    dict_n2 = []
    # narrowing the DICT down to words that start with the letter in inputted word.
    for letter in letters:
        if has_prefix(letter):
            global DICTIONARY
            # Narrowing down the word dictionary down to those begin with the letters that the user inputs.
            for words in DICTIONARY:
                if words.startswith(letter):
                    dict_n2.append(words)
    DICTIONARY = dict_n2
    for x in range(1, 5, 1):
        for y in range(1, 5, 1):
            start_letter = DICT[(x, y)]
            path.append((x, y))
            boggle(start_letter, path, (x, y), found_lst)
            path = []
    print(f'There are {len(found_lst)} words in total.')


def boggle(s, path, current_spot, found_lst):
    """
    :param s: str. the letters which were inputs
    :param path: lst[tuple] tuple the with the correspond spot of each letter.
    :param current_spot: tuple. the current spot where the searching is
    :param found_lst: lst[str] lst with the words found
    """
    if len(s) > 3 and s in DICTIONARY:
        if s not in found_lst:
            print(f'Found \"{s}\"')
            found_lst.append(s)
            # Codes below make sure the searching continues even when there are other longer words with the same
            # beginning letters as the short word was found. For example, "room" and "roomy".
            for i in range(-1, 2, 1):
                for j in range(-1, 2, 1):
                    near_x = current_spot[0] + i
                    near_y = current_spot[1] + j
                    if 1 <= near_x < 5:
                        if 1 <= near_y < 5:
                            if (near_x, near_y) not in path:
                                s += DICT[(near_x, near_y)]
                                path.append((near_x, near_y))
                                if has_prefix(s):
                                    boggle(s, path, (near_x, near_y), found_lst)
                                path.pop()
                                s = s[:-1]
    else:
        for i in range(-1, 2, 1):
            for j in range(-1, 2, 1):
                near_x = current_spot[0] + i
                near_y = current_spot[1] + j
                if 1 <= near_x < 5:
                    if 1 <= near_y < 5:
                        if (near_x, near_y) not in path:
                            s += DICT[(near_x, near_y)]
                            path.append((near_x, near_y))
                            if has_prefix(s):
                                boggle(s, path, (near_x, near_y), found_lst)
                            # print(path)
                            path.pop()
                            # print(path)
                            s = s[:-1]


def check(s):
    """
    :param s:str. the input of letters
    :return: bool.
    """
    if len(s) == 7 and len(s.split(' ')) == 4:
        for unit in s.split(' '):
            if unit.isalpha():
                return True


def read_dictionary():
    """
    This function reads file "dictionary.txt" stored in FILE
    and appends words in each line into a Python list
    """
    global DICTIONARY
    with open(FILE, mode='r') as f:
        for line in f:
            if line != '':
                DICTIONARY.append(line[0:len(line) - 1])


def has_prefix(sub_s):
    """
    :param sub_s: (str) A substring that is constructed by neighboring letters on a 4x4 square grid
    :return: (bool) If there is any words with prefix stored in sub_s
    """
    for word in DICTIONARY:
        if word.startswith(sub_s):
            return True
    return False


if __name__ == '__main__':
    main()
