import sys
import wik_search, yan_search, freq_processing, syno_search
import pymarc.marc8


# Oooooo magic numbers :o
DECL = 1001
CONJ = 1002
OTHR = 1003
NEW_SEC = 1004

section_codes = { DECL : "DECL", 
                  CONJ : "CONJ",
                  OTHR : "OTHR"}

query_word = 'яблоко'

if len(sys.argv) > 1:
    query_word = sys.argv[1]

info = wik_search.search(query_word)
if info == None:
    print("wik_search returned None")
    sys.exit()

defns = info['defns']
decls = info['decls']
conjs = info['conjs']
misc  = info['misc']

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

freq = freq_processing.get_freq(query_word)
print(f"Frequency of word: %d" % freq)

synos = syno_search.get_synonyms(query_word)
sorted_synos = []
print(f"Synonyms of %s:" % query_word)
for syno in synos:
    freq = freq_processing.get_freq(syno)
    sorted_synos.append([freq, syno])

def s(elem):
    return elem[0]
sorted_synos.sort(key=s)

for i in range(len(sorted_synos)):
    syno = sorted_synos[i]
    if syno[0] > 0 and (i == len(sorted_synos) - 1 or sorted_synos[i+1][1] != syno[1]) and syno[1] != query_word:
        print("\t" + str(syno[0]) + ": " + syno[1])
print()

print("\nExample sentences:")
exs = yan_search.search_exs(query_word)
for i in range(10):
    print("\t" + exs[i][0] + " = " + exs[i][1])
