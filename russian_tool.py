import requests
import sys
import re

freq_file = open("frequency.txt", "r")

# Oooooo magic numbers :o
DECL = 1001
CONJ = 1002
SIMILAR = 1003
OTHER = 1004

section_codes = { DECL : "DECL", 
                 CONJ : "CONJ",
                 SIMILAR : "SIMILAR",
                 OTHER : "OTHER"}

url = ''

if len(sys.argv) > 1:
    query_word = sys.argv[1]
    url = 'https://en.wiktionary.org/wiki/' + query_word

url_google = 'https://www.google.com/'
url_open_sister = 'https://en.openrussian.org/ru/сестра'
url_open_strike = 'https://en.openrussian.org/ru/забастовка'
url_wiki_sister = 'https://en.wiktionary.org/wiki/сестра'
url_wiki_strike = 'https://en.wiktionary.org/wiki/забастовка'
url_wiki_improve = 'https://en.wiktionary.org/wiki/наладить'

if url == '':
    url = url_wiki_improve

r = None

try:
    r = requests.get(url)
except:
    print("Link not valid")
    sys.exit()
html_doc = r.text

print("HTML DOC LEN: "  + str(len(html_doc)))

try: 
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup
soup_outer = BeautifulSoup(html_doc, 'html.parser')


def open_decl(soup):
    declension_cells = soup.find("div", "section declension noun").find_all("td")
    for cell in declension_cells:
        decls = cell.find_all("p")
        for decl in decls:
            print(decl.get_text())

# The elements corresponding to the header for a new language contain the
# attribute 'class' set to "mw-heading2". This returns whether the current
# has that, i.e., whether we've overflowed to the next language.
def on_the_next_language(elem):
    if "class" in elem.attrs and "mw-heading2" in elem["class"]:
        return True
    return False

# New subsections for the same language (e.g., declensions or conjugations)
# after the definition have 'class' attribute value 'mw-heading4'
def on_new_subsection(elem):
    if "class" in elem.attrs and "mw-heading4" in elem["class"]:
        return True
    return False

# Returns whether the passed elem is contains the definitions for this word
def on_definitions(elem):
    # A tag is an ordered list iff it's the definitions section
    # (so far as I can tell)
    if elem.name == 'ol':
        return True
    return False

def extract_defns(elem):

    lines = []

    for li in elem.children:
        if li.name == None:
            continue
        line = ''
        for kiddo in li.children:
            if(kiddo.name != 'a' and kiddo.name != None 
                            and kiddo.name != 'span'):
                break
            line  = line + kiddo.get_text()

        line = line.strip()
        lines.append(line)

    return lines

def get_subsection_type(elem):

    h4_elems = elem.find_all("h4")

    for elem in h4_elems:

        if not hasattr(elem, 'attrs'):
            continue

        if 'id' in elem.attrs:
            elem_id = elem['id']

            # Sometimes theres weird suffixes on the id's, so it's more
            # reliable to check for substring than exact match
            if "Declension" in elem_id:
                return DECL
            elif "Conjugation" in elem_id:
                return CONJ
            elif "Related" in elem_id or "Derived" in elem_id:
                return SIMILAR
            else:
                return OTHER

def is_table(elem):
    if is_valid_elem(elem):
        if elem_is_contains(elem, 'class', 'NavFrame'):
            return True
    return False

# Some attributes are multi-valued, so it's hard to tell whether you're
# querying for an exact membership or membership. This tests both.
def elem_is_contains(elem, key, query):
    if not is_valid_elem(elem):
        return False
    if key not in elem.attrs:
        return False
    if type(elem[key]) == list:
        return query in elem[key]
    else:
        return query == elem[key]

# Returns a list of all Russian-language table contents
def get_all_table_contents(table_elem):
    
    contents = []

    if not elem_is_contains(table_elem, 'class', 'NavFrame'):
        print("Non-table element has been passed to get_all_table_contents")
        return

    table_contents_elem = table_elem.find("div", "NavContent")

    if table_contents_elem == None:
        print("table contents not found")
    else:
        ru_cells = table_contents_elem.find_all("span", lang="ru")
        for cell in ru_cells:
            contents.append(cell.get_text())
        return contents

# If the elem is None or is an empty NavigableString, return False
def is_valid_elem(elem):
    if elem == None or not hasattr(elem, 'attrs'):
        return False
    return True

def extract_decl(elem):

    elem = elem.next_sibling

    while not is_valid_elem(elem):
        elem = elem.next_sibling

    for elem_child in elem.children:
        if is_table(elem_child):
            return get_all_table_contents(elem_child)

def extract_conj(elem):
    # TODO : Implement
    print("called extract_conj")

def extract_similar(elem):
    # TODO : Implement
    print("called extract_similar")

# Returns the definitions, declensions, conjugations, and related terms
# (as applicable) in the Russian section of the given soup element.
def wiki_decl(soup):
    defns = []
    decls = []
    conjs = []
    related = []

    # Finds the section header for Russian
    russian_sec_search = soup.find_all(id="Russian")

    if len(russian_sec_search) < 1:
        print("Russian section not found")
        return

    # Goes up one level to get out of the Russian header element
    current_elem = russian_sec_search[0].parent

    while True:

        if current_elem == None:
            break

        current_elem = current_elem.next_sibling

        # There are often empty 'NaviagableString's between elements.
        # This saves us from trying to query them
        if not is_valid_elem(current_elem):
            continue

        # If we're now past the Russian section, terminate the search
        if on_the_next_language(current_elem):
            break

        if on_definitions(current_elem):
            defns.extend(extract_defns(current_elem))

        if on_new_subsection(current_elem):
            type_subsection = get_subsection_type(current_elem)
            # TODO : Implement
            print("SECTION FOUND: " + section_codes[type_subsection])
            if type_subsection == DECL:
                decls.extend(extract_decl(current_elem))

    print("\nDefinitions:")
    for line in defns:
        print("\t" + line)

    print("\nDeclensions:")
    for line in decls:
        print("\t" + line)

wiki_decl(soup_outer)

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

file_str = freq_file.read()

freq_matches = {}

#print("Frequency file matches:")
for match in re.finditer(query_word, file_str):
    line = get_line(file_str, match.start())

    num_split = line.split('.')
    number = num_split[0]

    word_split = line.split('\t')
    word = word_split[1].split(' ')[0]

    freq_matches[word] = number
    
    #print(line + " " + str(number) + " " + word)

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
