import sys, my_translate, img_scrape
import en_wik_search, syno_search
from en_wik_search import NEW_SEC
import yan_search
import freq_processing
import pymarc.marc8
import threading

# When searching for synonyms of a word, how many recursive levels does the 
# search go (e.g., do you include synonyms of synonyms)
synonym_num_recursive_levels = 0
# Upper limit on the number of synonyms that may be read during synonym search
synonyms_cutoff = 50
# Number of synonyms that will be printed
num_synos = 999

DEFNS_EN = "defns_en"
DEFNS_RU = "defns_ru"
DECLS = "decls"
CONJS = "conjs"
FREQ = "freq"
EXAMPLES = "examples"
IMGS_DIR = "imgs_dir"
SYNOS = "synos"
MISC = "misc"

debug = False

def debug_print(string):
    if debug == True:
        print(string)

def strip_accents(word):

    word = word.replace('а́','а')
    word = word.replace('é','е')
    word = word.replace('и́','и')
    word = word.replace('ó','о')
    word = word.replace('у́','у')
    word = word.replace('ы́','ы')
    word = word.replace('э́','э')
    word = word.replace('я́','я')
    word = word.replace('ю́','ю')
    
    word = word.replace('А́','А')
    word = word.replace('Е́','Е')
    word = word.replace('И́','И')
    word = word.replace('О́','О')
    word = word.replace('У́','У')
    word = word.replace('Ы́','Ы')
    word = word.replace('Э́','Э')
    word = word.replace('Ю́','Ю')
    word = word.replace('Я́','Я')

    return word

def generate_field_en(query_word):
    
    query_word = strip_accents(query_word)

    out = {DEFNS_EN : None, DECLS : None, CONJS : None, MISC : None}

    # Scrape English definitions
    info = en_wik_search.search(query_word)
    if info != None:
        out[DEFNS_EN] = info['defns']
        out[DECLS]    = info['decls']
        out[CONJS]    = info['conjs']
        out[MISC]     = info['misc']

    return out

def generate_field_exs(query_word):

    query_word = strip_accents(query_word)

    # Scrape and format example sentences
    exs = yan_search.search_exs(query_word)
    exs_strs = []

    for i in range(len(exs)):
        ex = exs[i]
        if ex[0][len(ex[0]) - 1] == ".":
            ex[0] = ex[0][:len(ex[0]) - 1]
        ex_str = ex[0] + " = " + ex[1]
        exs_strs.append(ex_str)

    print(len(exs_strs))
    return exs_strs

def generate_field_synos(query_word):

    query_word = strip_accents(query_word)

    # Identify synonyms and their respective definitions
    synos = syno_search.get_synonyms(query_word, synonym_num_recursive_levels,
                                     synonyms_cutoff)
    debug_print("Obtained synonyms")
    sorted_synos = []
    for syno in synos:
        freq = freq_processing.get_freq(syno)
        if freq > 0:
            sorted_synos.append([freq, syno])

    sorted_synos.sort(key=sort_first_elem)
    synos_defns = []

    for i in range(min(num_synos, len(sorted_synos))):
        
        syno_tup = sorted_synos[i]
        freq = int(syno_tup[0])
        print(freq)
        syno = syno_tup[1]

        if ((i == len(sorted_synos) - 1 or sorted_synos[i+1][1] != syno)
            and syno != query_word):
            
            syno_defns = en_wik_search.search_defn(syno)

            # Merge synonym definitions into a single line
            if syno_defns != None:
                defn_str = ""
                for defn in syno_defns:
                    defn_str = defn_str + defn + "; "
                defn_str = defn_str[:len(defn_str)-2]

            # Combine synonym and definition string into a single line
            syno_defn = ""
            if syno_defns != None:
                syno_defn = f"[{freq}] " + syno + " = " + defn_str
            else:
                defn_str = my_translate.translate(syno)
                syno_defn = syno + " = [machine translation] " + defn_str

            synos_defns.append(syno_defn)

    return synos_defns

def sort_first_elem(elem):
    return elem[0]
