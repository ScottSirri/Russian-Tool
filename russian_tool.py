import sys
import wik_search, yan_search, freq_processing, syno_search
import pymarc.marc8


# Oooooo magic numbers :o
DECL = 1001
CONJ = 1002
OTHR = 1003
NEW_SEC = 1004

synonym_num_recursive_levels = 0
synonyms_cutoff = 9999

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

synos = syno_search.get_synonyms(query_word, synonym_num_recursive_levels, synonyms_cutoff)
sorted_synos = []
for syno in synos:
    freq = freq_processing.get_freq(syno)
    if freq > 0:
        sorted_synos.append([freq, syno])

def s(elem):
    return elem[0]
sorted_synos.sort(key=s)

for i in range(len(sorted_synos)):
    
    syno_tup = sorted_synos[i]
    freq = int(syno_tup[0])
    syno = syno_tup[1]

    if (i == len(sorted_synos) - 1 or sorted_synos[i+1][1] != syno) and syno != query_word:
        
        syno_defns = wik_search.search_defn(syno)

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
            print("\t" + syno)
print()

print("\nExample sentences:")
exs = yan_search.search_exs(query_word)
for i in range(10):
    ex = exs[i]
    if ex[0][len(ex[0]) - 1] == ".":
        ex[0] = ex[0][:len(ex[0]) - 1]
    print("\t" + ex[0] + " = " + ex[1])
