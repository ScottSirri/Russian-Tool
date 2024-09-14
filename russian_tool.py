import sys, my_translate, img_scrape
import en_wik_search, ru_wik_search, syno_search
from en_wik_search import NEW_SEC
import yan_search
import freq_processing
import pymarc.marc8
from tkinter import *
from tkinter import ttk
import my_gui

# When searching for synonyms of a word, how many recursive levels does the 
# search go (e.g., do you include synonyms of synonyms)
synonym_num_recursive_levels = 0
# Upper limit on the number of synonyms that may be read during synonym search
synonyms_cutoff = 999
# Number of synonyms that will be printed
num_synos = 40

root = Tk()
gui = my_gui.GUI(root)
root.mainloop()
print("russian_tool mainloop ended")
sys.exit()

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
        en_defn = "[machine translation] " + my_translate.translate(query_word)
        en_defns.append(en_defn)
        ru_defns = []
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
for i in range(len(ru_defns)):
    defn_ru = ru_defns[i]
    defn_en = my_translate.translate(defn_ru)
    print("\t" + defn_ru + " = [machine translation] " + defn_en)
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
# frequency is printed after it in parentheses, and then the viewer can 
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
            defn_str = my_translate.translate(syno)
            print("\t" + syno + " = [machine translation] " + defn_str)
print()

print("\nExample sentences:")
exs = yan_search.search_exs(query_word)

for i in range(min(10, len(exs))):
    ex = exs[i]
    if ex[0][len(ex[0]) - 1] == ".":
        ex[0] = ex[0][:len(ex[0]) - 1]
    print("\t" + ex[0] + " = " + ex[1])

out_dir = img_scrape.get_imgs(query_word)
print("Downloaded images available in " + out_dir)
