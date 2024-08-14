import requests
import sys
import re
import wik_search


freq_file = open("frequency.txt", "r")

# Oooooo magic numbers :o
DECL = 1001
CONJ = 1002
OTHR = 1003
NEW_SEC = 1004

section_codes = { DECL : "DECL", 
                  CONJ : "CONJ",
                  OTHR : "OTHR"}

url_base_yandex = 'https://translate.yandex.com/examples/Russian-English/'

query_word = 'яблоко'

if len(sys.argv) > 1:
    query_word = sys.argv[1]

# Given a string and an index in it, return the whole line containing
# that character corresponding to that index
def get_line(string, ind):
    start_ind = ind
    end_ind = ind
    while string[start_ind] != '\n':
        start_ind -= 1
    start_ind += 1
    if string[start_ind] == '\t':
        start_ind += 1
    while string[end_ind] != '\n':
        end_ind += 1
    return string[start_ind:end_ind]

info = wik_search.search(query_word)
defns = info['defns']
decls = info['decls']
conjs = info['conjs']
misc = info['misc']

print("\nDefinitions:")
for line in defns:
    print("\t" + line)
print()

if len(decls) > 0:
    print("\nDeclensions:")
    for line in decls:
        print("\t" + line)
    print()

if len(conjs) > 0:
    print("\nConjugations:")
    for line in conjs:
        print("\t" + line)
    print()

# TODO : Order words by frequency (first Russian word? split by spaces?)
if len(misc) > 0:
    print("\nMisc:")
    for line in misc:
        if line == NEW_SEC:
            print()
        else:
            print("\t" + line)
    print()

file_str = freq_file.read()

freq_matches = {}

for match in re.finditer(query_word, file_str):
    line = get_line(file_str, match.start())

    num_split = line.split('.')
    number = num_split[0]

    word_split = line.split('\t')
    word = word_split[1].split(' ')[0]

    freq_matches[word] = number

print()
elem_found = False
if query_word in freq_matches:
    elem_found = True
    print("Frequency list match found:")
    print('\t' + query_word + " (freq " + str(freq_matches[query_word]) + ")")
else:
    print("Query word not found on frequency list")

print()

print("Other honorable mentions from the frequency list:")
for key in freq_matches:
    if key != query_word:
        print('\t' + key + " (freq " + str(freq_matches[key]) + ")")


freq_file.close()
