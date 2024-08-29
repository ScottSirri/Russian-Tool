import requests
import sys

try: 
    from BeautifulSoup import BeautifulSoup
    from bs4 import Tag, NavigableString
except ImportError:
    print("ImportError BeautifulSoup")
    from bs4 import Tag, NavigableString, BeautifulSoup

# Oooooo magic numbers :o
DECL = 1001
CONJ = 1002
OTHR = 1003
NEW_SEC = 1005

section_codes = { DECL : "DECL", 
                  CONJ : "CONJ",
                  OTHR : "OTHR"}

url_base_wiktionary = 'https://en.wiktionary.org/wiki/'

# The elements corresponding to the header for a new language contain the
# attribute 'class' set to "mw-heading2". This returns whether the current
# has that, i.e., whether we've overflowed to the next language.
def on_the_next_language(elem):
    if elem_is_contains(elem, "class", "mw-heading2"):
        return True
    return False

# New subsections for the same language (e.g., declensions or conjugations)
# after the definition have 'class' attribute value 'mw-heading4'. I specially
# handle these, and throw the rest into a grab bag
def on_special_subsection(elem):
    # TODO : May be worth implementing handling of mw-heading3 elements as well
    if elem_is_contains(elem, "class", "mw-heading4"):
        return True
    return False

# Returns whether the passed elem is contains the definitions for this word
def on_definitions(elem):
    # A top-level tag is an ordered list iff it's the definitions section
    # (so far as I can tell)
    if elem.name == 'ol':
        return True
    return False

# Passed an ol element, returns its contents as individual lines (excluding
# any example sentences included with them)
def extract_defns(elem):
    # TODO : Return the included example sentencesn, synonyms, etc included 
    # as a dl following an li
    lines = []

    for li in elem.children:
        if li.name == None:
            continue
        line = ''
        for kiddo in li.children:
            if elem_is_contains(kiddo, "class", "nyms-toggle") or kiddo.name=="style" or kiddo.name == "dl" or kiddo.name == "ul":
                continue
            line = line + kiddo.get_text()

        if line != '':
            line = line.strip()
            line = line.replace("\n", " ")
            lines.append(line)

    return lines

# Returns the section type of the passed mw-heading4 element
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
                # There are so many types of sections, not worth handling them 
                # all. Lots of interesting miscellaneous sections are followed 
                # by a ul element, so I just pass up any special handling of
                # "other" sections and stuff all their ul's in the same bag
                return OTHR

# Returns whether the passed element is the topmost element of 
# a table (NavFrame element)
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
        print("en Non-table element has been passed to get_all_ru_table_contents")
        return

    table_contents_elem = table_elem.find("div", "NavContent")

    if table_contents_elem == None:
        print("en table contents not found")
    else:
        ru_cells = table_contents_elem.find_all("span", lang="ru")
        for cell in ru_cells:
            contents.append(cell.get_text())
        return contents

# Returns all non-header cell Russian language table contents
def get_body_ru_table_contents(table_elem):
    
    contents = []

    if not elem_is_contains(table_elem, 'class', 'NavFrame'):
        print("en Non-table element passed to get_body_ru_table_contents")
        return

    table_contents_elem = table_elem.find("div", "NavContent")

    if table_contents_elem == None:
        print("en table contents not found")
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

# Returns the previous sibling element (ignoring invalid elements)
def prev_elem(elem):
    elem = elem.previous_sibling
    while not is_valid_elem(elem):
        elem = elem.previous_sibling
    return elem

# Returns all contents of the table following the passed mw-heading4 element 
def extract_decl(elem):

    elem = next_elem(elem)
    
    # Sometimes the table is at a table at the topmost level
    if is_table(elem):
        return get_all_ru_table_contents(elem)

    # But usually, declensions are a NavFrame inside a div element
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
        contents.append(str(li.get_text()))
    return contents


# Returns from Wiktionary the definitions and misc information for a word
def search(word):
    defns = search_defn(word)
    ret = search_misc(word)
    if defns == None or ret == None:
        print("en search: search_defn and/or search_misc returned 'None'")
        return None
    ret['defns'] = defns
    return ret


# Returns from Wiktionary the definitions of the word
def search_defn(word):

    url_wiktionary = url_base_wiktionary + word
    r = None
    try:
        r = requests.get(url_wiktionary)
    except:
        print(f"en search_defn: Link not valid (%s)" % url_wiktionary)
        sys.exit()
    html_doc = r.text

    #print("search_defn: HTML DOC LEN: "  + str(len(html_doc)))

    soup = BeautifulSoup(html_doc, 'html.parser')

    defns = []

    # Finds the section header for Russian
    russian_sec_search = soup.find_all(id="Russian")

    if len(russian_sec_search) < 1:
        #print("search_defn: Russian section not found")
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
            # Right before definitions is usually a headline containing
            # useful misc info like aspectual partners, diminuitives, etc
            headword_elem = prev_elem(current_elem)
            headword_list = headword_elem.find_all("span", "headword-line")
            if len(headword_list) > 0:
                headword = headword_list[0].get_text()
                headword = headword.replace("• ","")
                defns.append(headword)

            new_defns = extract_defns(current_elem)
            defns.extend(new_defns)

    return defns


# Returns from Wiktionary the conjugation, declension, and misc information 
# as applicable
# TODO : Omit the ru-glish pronunciations in parentheses after words
def search_misc(word):

    url_wiktionary = url_base_wiktionary + word
    r = None
    try:
        r = requests.get(url_wiktionary)
    except:
        print(f"en search_defn: Link not valid (%s)" % url_wiktionary)
        sys.exit()
    html_doc = r.text

    #print("search_misc: HTML DOC LEN: "  + str(len(html_doc)))

    soup = BeautifulSoup(html_doc, 'html.parser')

    decls = []
    conjs = []
    misc = []

    # Finds the section header for Russian
    russian_sec_search = soup.find_all(id="Russian")

    if len(russian_sec_search) < 1:
        print("en search_misc: Russian section not found")
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

        if on_special_subsection(current_elem):
            type_subsection = get_subsection_type(current_elem)
            #print("search_misc: SECTION FOUND: " 
            #      + section_codes[type_subsection])
            if type_subsection == DECL:
                new_decls = extract_decl(current_elem)
                if new_decls == None:
                    print("en search_misc: extract_decl returned None")
                    return None
                decls.extend(new_decls)
            elif type_subsection == CONJ:
                new_conjs = extract_conj(current_elem)
                if new_conjs == None:
                    print("en search_misc: extract_conj returned None")
                    return None
                conjs.extend(new_conjs)
        else:
            uls = current_elem.find_all("ul")
            if is_ul(current_elem):
                uls.append(current_elem)

            for ul in uls:
                new_misc = extract_ul(ul)
                # Manually omitting a common and uninteresting ul element
                if len(new_misc) >= 1 and ("IPA" in new_misc[0] 
                                           or "Audio:" in new_misc[0]):
                    continue
                misc.extend(new_misc)
                misc.append(NEW_SEC)
    return {'conjs' : conjs, 'decls' : decls, 'misc' : misc}
                    
