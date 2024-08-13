import requests
import sys
import re
from russtress import Accent
accent = Accent()

freq_file = open("frequency.txt", "r")

# Oooooo magic numbers :o
DECL = 1001
CONJ = 1002
OTHR = 1003
NEW_SEC = 1004

section_codes = { DECL : "DECL", 
                  CONJ : "CONJ",
                  OTHR : "OTHR"}

url = ''

if len(sys.argv) > 1:
    query_word = sys.argv[1]
    url = 'https://en.wiktionary.org/wiki/' + query_word

url_google = 'https://www.google.com/'

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


# The elements corresponding to the header for a new language contain the
# attribute 'class' set to "mw-heading2". This returns whether the current
# has that, i.e., whether we've overflowed to the next language.
def on_the_next_language(elem):
    if "class" in elem.attrs and "mw-heading2" in elem["class"]:
        return True
    return False

# New subsections for the same language (e.g., declensions or conjugations)
# after the definition have 'class' attribute value 'mw-heading4'. I specially
# handle these, and throw the rest into a grab bag
def on_special_subsection(elem):
    # TODO : May be worth implementing handling of mw-heading3 elements as well
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

# Passed an ol element, returns its contents as individual lines (excluding
# any example sentences included with them)
def extract_defns(elem):
    # TODO : Returns the included example sentences separately (?)
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

# Returns the section type of the passed element
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
            else:
                # There are so many types of sections, not worth handling them all. 
                # Lots of interesting miscellaneous sections are followed by a ul 
                # element, so I just pass up any special handling of "other" 
                # sections and stuff all their ul's in the same bag
                return OTHR

# Returns whether the passed element is the topmost element of a table (NavFrame)
def is_table(elem):
    if is_valid_elem(elem):
        if elem_is_contains(elem, 'class', 'NavFrame'):
            return True
    return False

# Some attributes are multi-valued, so it's hard to tell whether you're
# querying for an exact value or membership. This tests both.
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
def get_all_ru_table_contents(table_elem):
    
    contents = []

    if not elem_is_contains(table_elem, 'class', 'NavFrame'):
        print("Non-table element has been passed to get_all_ru_table_contents")
        return

    table_contents_elem = table_elem.find("div", "NavContent")

    if table_contents_elem == None:
        print("table contents not found")
    else:
        ru_cells = table_contents_elem.find_all("span", lang="ru")
        for cell in ru_cells:
            contents.append(cell.get_text())
        return contents

# Returns all non-header cell Russian language table contents
def get_body_ru_table_contents(table_elem):
    
    contents = []

    if not elem_is_contains(table_elem, 'class', 'NavFrame'):
        print("Non-table element has been passed to get_body_ru_table_contents")
        return

    table_contents_elem = table_elem.find("div", "NavContent")

    if table_contents_elem == None:
        print("table contents not found")
    else:
        body_cells = table_contents_elem.find_all("td")
        for cell in body_cells:
            # TODO : In table cells with more than one line/russian word,
            # this currently appends them. It should break on the comma.
            cell_str = ""
            ru_text = cell.find_all("span", lang="ru")
            for ru in ru_text:
                cell_str = cell_str + ru.get_text()
            if len(cell_str) > 0:
                contents.append(cell_str)
        return contents

# If the elem is None or is an empty NavigableString, return False
def is_valid_elem(elem):
    if elem == None or not hasattr(elem, 'attrs'):
        return False
    return True

# Returns the next sibling element (ignoring invalid elements)
def next_elem(elem):
    elem = elem.next_sibling
    while not is_valid_elem(elem):
        elem = elem.next_sibling
    return elem

# Returns all contents of the table following the passed mw-heading4 element 
def extract_decl(elem):

    elem = next_elem(elem)

    # Declensions are a NavFrame inside a div element
    for elem_child in elem.children:
        if is_table(elem_child):
            return get_all_ru_table_contents(elem_child)

# Returns the russian contents of all body cells in the table following the
# passed mw-heading4 element
def extract_conj(elem):

    # TODO : Reorder conjugations, same tense consecutive

    # There is a style tag preceding conjugation tables
    elem = next_elem(elem)
    elem = next_elem(elem)

    # Conjugation table is a NavFrame rawdogging it out on its own in the open
    if is_table(elem):
        return get_body_ru_table_contents(elem)

def is_ul(elem):
    if is_valid_elem(elem) and elem.name == "ul":
        return True
    return False

def extract_ul(elem):
    contents = []
    lis = elem.find_all("li")
    for li in lis:
        contents.append(li.get_text())
    return contents

# Returns the definitions, declensions, conjugations, and related terms
# (as applicable) in the Russian section of the given soup element.
def wiki_decl(soup):
    defns = []
    decls = []
    conjs = []
    misc = []

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
            new_defns = extract_defns(current_elem)
            defns.extend(new_defns)
        elif on_special_subsection(current_elem):
            type_subsection = get_subsection_type(current_elem)
            print("SECTION FOUND: " + section_codes[type_subsection])
            if type_subsection == DECL:
                new_decls = extract_decl(current_elem)
                decls.extend(new_decls)
            elif type_subsection == CONJ:
                new_conjs = extract_conj(current_elem)
                conjs.extend(new_conjs)
        else:
            uls = current_elem.find_all("ul")
            if is_ul(current_elem):
                uls.append(current_elem)

            for ul in uls:
                new_misc = extract_ul(current_elem)
                misc.extend(new_misc)
                misc.append(NEW_SEC)
                    
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
