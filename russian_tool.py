import sys, my_translate, img_scrape
import en_wik_search, syno_search
from en_wik_search import NEW_SEC
import yan_search
import freq_processing
import pymarc.marc8

# When searching for synonyms of a word, how many recursive levels does the 
# search go (e.g., do you include synonyms of synonyms)
synonym_num_recursive_levels = 0
# Upper limit on the number of synonyms that may be read during synonym search
synonyms_cutoff = 999
# Number of synonyms that will be printed
num_synos = 20

DEFNS_EN = "defns_en"
DEFNS_RU = "defns_ru"
DECLS = "decls"
CONJS = "conjs"
FREQ = "freq"
EXAMPLES = "examples"
IMGS_DIR = "imgs_dir"
SYNOS = "synos"
MISC = "misc"

debug = True

def debug_print(string):
    if debug == True:
        print(string)

def strip_accents(word):
    #
    #
    #
    #
    word.replace('á','')
    word.replace('é','')
    word.replace('и́','')
    word.replace('ó','')
    word.replace('у́','')
    word.replace('ы́','')
    word.replace('э́','')
    word.replace('я́','')
    word.replace('ю́','')
    word.replace('á','')
    word.replace('é','')
    word.replace('и́','')
    word.replace('ó','')
    word.replace('у́','')
    word.replace('ы́','')
    word.replace('э́','')
    word.replace('я́','')
    word.replace('ю́','')


def quick_search(query_word='яблоко'):

    out = {DEFNS_EN : None, DECLS : None, CONJS : None, MISC : None}

    # Scrape English definitions
    info = en_wik_search.search(query_word)
    if info != None:
        out[DEFNS_EN] = info['defns']
        out[DECLS]    = info['decls']
        out[CONJS]    = info['conjs']
        out[MISC]     = info['misc']
    debug_print("Finished scraping English definitions")

    return out

def generate_card_fields(query_word='яблоко'):

    out = {DEFNS_EN : None, DECLS : None, CONJS : None, 
           MISC : None, SYNOS : None, EXAMPLES : None , IMGS_DIR : None}

    # Scrape English definitions
    info = en_wik_search.search(query_word)
    if info != None:
        out[DEFNS_EN] = info['defns']
        out[DECLS]    = info['decls']
        out[CONJS]    = info['conjs']
        out[MISC]     = info['misc']
    debug_print("Finished scraping English definitions")

    # Determine word frequency
    freq = freq_processing.get_freq(query_word)
    out[FREQ] = freq
    debug_print("Found word frequency")

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
                syno_defn = syno + " = " + defn_str
            else:
                defn_str = my_translate.translate(syno)
                syno_defn = syno + " = [machine translation] " + defn_str

            synos_defns.append(syno_defn)

    out[SYNOS] = synos_defns
    debug_print("\tTranslated and formatted synonyms")

    # Scrape and format example sentences
    exs = yan_search.search_exs(query_word)
    exs_strs = []

    for i in range(min(10, len(exs))):
        ex = exs[i]
        if ex[0][len(ex[0]) - 1] == ".":
            ex[0] = ex[0][:len(ex[0]) - 1]
        ex_str = ex[0] + " = " + ex[1]
        exs_strs.append(ex_str)
    out[EXAMPLES] = exs_strs
    debug_print("Scraped example sentences")

    # Scrape images
    out_dir = img_scrape.get_imgs(query_word)
    out[IMGS_DIR] = out_dir
    debug_print("Scraped images")

    return out

def sort_first_elem(elem):
    return elem[0]
