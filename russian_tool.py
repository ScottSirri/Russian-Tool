import sys
import en_wik_search, ru_wik_search, yan_search, freq_processing, syno_search
import pymarc.marc8


# Oooooo magic numbers :o
DECL = 1001
CONJ = 1002
OTHR = 1003
NEW_SEC = 1004

section_codes = { DECL : "DECL", 
                  CONJ : "CONJ",
                  OTHR : "OTHR"}

# When searching for synonyms of a word, how many recursive levels does the 
# search go (e.g., do you include synonyms of synonyms)
synonym_num_recursive_levels = 0
# Upper limit on the number of synonyms that may be read during synonym search
synonyms_cutoff = 999
# Number of synonyms that will be printed
num_synos = 40

# Arbitrary default query word
query_word = 'яблоко'

if len(sys.argv) > 1:
    query_word = sys.argv[1]

en_defns = []
en_decls = []
en_conjs = []
en_misc  = []
ru_defns = []

# Scrape the English Wiktionary page for the query word
info = en_wik_search.search(query_word)
ru_defns = ru_wik_search.search_defn(query_word)
if info == None:
    print("en_wik_search.search returned None")
    if ru_defns == None:
        print("ru_wik_search.search returned None")
        sys.exit()
else:
    en_defns = info['defns']
    en_decls = info['decls']
    en_conjs = info['conjs']
    en_misc  = info['misc']

print("\nEnglish Definitions:")
for line in en_defns:
    print("\t" + line)
print()

print("\nRussian Definitions:")
for line in ru_defns:
    print("\t" + line)
print()



if len(en_decls) > 0:
    print("\nEnglish Declensions:")
    for line in en_decls:
        print("\t" + line)
    print()

if len(en_conjs) > 0:
    print("\nEnglish Conjugations:")
    for line in en_conjs:
        print("\t" + line)
    print()

# TODO : Create a second copy of the string where every Russian word's 
# frequency is printed after it in parentheses, and then the viewier can 
# toggle between the views.
if len(en_misc) > 0:
    print("\nEnglish Misc:")
    for line in en_misc:
        if line == NEW_SEC:
            print()
        else:
            print("\t" + line)
    print()

freq = freq_processing.get_freq(query_word)
print(f"Frequency of word: %d" % freq)

synos = syno_search.get_synonyms(query_word, synonym_num_recursive_levels,
                                 synonyms_cutoff)
sorted_synos = []
for syno in synos:
    freq = freq_processing.get_freq(syno)
    if freq > 0:
        sorted_synos.append([freq, syno])

def s(elem):
    return elem[0]
sorted_synos.sort(key=s)

for i in range(min(num_synos, len(sorted_synos))):
    
    syno_tup = sorted_synos[i]
    freq = int(syno_tup[0])
    syno = syno_tup[1]

    if ((i == len(sorted_synos) - 1 or sorted_synos[i+1][1] != syno)
        and syno != query_word):
        
        syno_defns = en_wik_search.search_defn(syno)

        if syno_defns != None:
            defn_str = ""
            for defn in syno_defns:
                defn_str = defn_str + defn + "; "
            defn_str = defn_str[:len(defn_str)-2]

        freq_str = str(freq).rjust(5, " ")
        if freq <= 20000 and syno_defns != None:
            print("\t" + freq_str + ": " + syno + " = " + defn_str)
        elif syno_defns != None:
            print("\t" + syno + " = " + defn_str)
        else:
            # TODO : Insert machine translations of words/phrases not found in Wiktionary
            # (with an asterisk denoting it's a machine translation)
            print("\t" + syno)
print()

print("\nExample sentences:")
exs = yan_search.search_exs(query_word)
for i in range(10):
    ex = exs[i]
    if ex[0][len(ex[0]) - 1] == ".":
        ex[0] = ex[0][:len(ex[0]) - 1]
    print("\t" + ex[0] + " = " + ex[1])
