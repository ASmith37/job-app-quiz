# -*- coding: utf-8 -*-
"""
Created on Fri Jan  4 19:53:20 2019

The site XXXXXXXXXXXXXXXXXX has a list of numbers. e.g.

249 8 57 29 18 249 209 230 60 31 10 63 18 23 66 29 4 65 26 18 59 36 195 51 32
21 237 36 18 57 39 12 59 24 195 65 25 8 237 248 4 58 19 12 65 209 6 53 18 15
57 22 17 52 22 209 237 1 15 50 18 22 50 209 22 50 31 7 237 42 18 66 35 195 64
32 15 66 37 12 60 31 195 46 31 7 237 244 249 237 37 18 237 26 6 46 31 6 60 21
8 13 24 4 58 19 12 65 35 8 64 22 4 63 20 11 251 20 18 58 209 20 66 32 23 54 31
10 237 35 8 51 22 21 50 31 6 50 235 195 51 233 214 50 21 213 1 21 4 49 223

Hidden in the HTML is a Javascript function to encode a string
into a list of numbers using 3 offsets

These numbers presumably contain a message with instructions to send a CV
These instructions are presumably in English, using latin letters
"""

import re
import requests

# Helper functions
def split_list_into_three(data):
    # Takes in a list
    # puts the 1st, 4th, 7th... elements in the first list
    # puts the 2nd, 5th, 8th... elements in the second list
    # puts the 3rd, 6th ... elements in the third list
    # returns a list of lists
    result = [[], [], []]
    counter = 0
    for num in data:
        result[counter % 3].append(num)
        counter += 1
    return result

def is_number_an_ascii_char(number):
    # We think that the message will mostly be letters A-Z a-z and spaces
    # Those letters are ASCII characters 65-90 and 97-122
    # spaces are 32
    # For any given number, say if it represents an ASCII letter
    return (number >= 65 and number <= 90) or (number >= 97 and number <= 122) or number == 32

def un_offset(number, offset):
    return (number + 256 - offset) % 256

def determine_likely_offsets(number_list):
    # given a list of numbers encoded with a single offset
    # determine the likely offsets used to encode them
    #
    # return a dict of the 10 or so most likely offsets
    # this will be {offset(int): letter_count(int), ...}
    letter_counts = {}
    for offset in range(0, 255):
        adjusted_letters = list(map(lambda x: un_offset(x, offset), number_list))
        # That's one way of making a partial function...
        letter_counts[offset] = list(map(is_number_an_ascii_char, adjusted_letters)).count(True)
    # Now we have a dict of 256 offsets and ascii character counts
    # We can't use 256, so we'll throw away the less likely ones
    desired_offset_count = 5
    # lower the cutoff criteria until we have at least that many likely offsets
    # start at the highest letter for any offset
    for cutoff in range(max(letter_counts.values()), 0, -1):
        # select only those offsets with ASCII letter counts above the cutoff
        likely_offsets = {k: v for i, (k,v) in enumerate(letter_counts.items()) if v >= cutoff}
        # if we have enough for our liking
        if len(likely_offsets) > desired_offset_count:
            return likely_offsets
    return {}

def decode_number_list(number_list, offset_list):
    # inputs:
    # number list = [17, 255, 88, 74...] of long message
    # offset list = [15, 96, 75] of 3 offsets
    # output a list of unencoded numbers
    # e.g. [62, 97, 23, ...]
    # we think the unencoded numbers will be convertible to ASCII
    # 
    result = []
    for i in range(0, len(number_list)):
        result.append(un_offset(number_list[i], offset_list[i % 3]))
    return result

def enumerate_possible_offsets(likely_offsets):
    result = []
    for a in likely_offsets[0]:
        for b in likely_offsets[1]:
            for c in likely_offsets[2]:
                result.append([a, b, c])
    return result

def enumerate_possible_sentences(numbers, likely_offsets):
    # takes in a list of numbers
    # takes in a list of 3 lists of likely offsets
    # iterates over all combinations of likely offsets
    result = []
    for offset_list in enumerate_possible_offsets(likely_offsets):
        sentence = ''.join([chr(x) for x in decode_number_list(numbers, offset_list)])
        result.append(sentence)
    return result
                
# Script code starts

# Download the code of the XXXXXXXXXXXX quiz page
url = "REDACTED.com/quiz"
r = requests.get(url)
# Make sure request succeeded
assert r.status_code == 200
# get the HTML
html = r.content.decode()
# extract the message numbers from the HTML
# a regex was simpler than BeautifulSoup
reg = re.compile("[0-9 ]{10,1000}")
str_numbers = reg.search(html).group()
# convert the str numbers to a list of ints
numbers = [int(x) for x in str_numbers.split(" ")]
split_numbers = split_list_into_three(numbers)
# get a list of the likely offsets for each list
likely_offset_dicts = [determine_likely_offsets(x) for x in split_numbers]
# Sort the offsets by likeliness
likely_offsets = [[x[0] for x in sorted(y.items(), key = lambda x: 256 - x[1])] for y in likely_offset_dicts]
#
# We assume that the message will be made of English words
# Let's enumarate all the combinations of offsets
# then count how many English words we can count in each
possible_sentences = enumerate_possible_sentences(numbers, likely_offsets)
#
print(possible_sentences[0])
# "Hello, Congratulations for solving the XXXXXX challenge. Please send your solution and CV to XXXXXXX@XXXXXXXXXXXXX.com quoting reference: XXXXXXXXXXXXX."
