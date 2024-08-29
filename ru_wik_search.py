import requests
import sys

try: 
    from BeautifulSoup import BeautifulSoup
    from bs4 import Tag, NavigableString
except ImportError:
    print("ImportError BeautifulSoup")
    from bs4 import Tag, NavigableString, BeautifulSoup

url_base_wiktionary = 'https://ru.wiktionary.org/wiki/'

# The elements corresponding to the header for a new language contain the
# attribute 'class' set to "mw-heading2". This returns whether the current
# has that, i.e., whether we've overflowed to the next language.
def on_the_next_language(elem):
    if elem_is_contains(elem, "class", "mw-heading1"):
        return True
    return False

# Returns whether the passed elem is the header for the definitions section
def on_definitions(elem):
    if elem_is_contains(elem, "class", "mw-heading4"):
        if len(elem.find_all(id="Значение")) > 0:
            return True
    return False

# Passed an ol element, returns its contents as individual lines (excluding
# any example sentences included with them)
def extract_defns(elem):

    lines = []

    for li in elem.children:
        if li.name == None:
            continue
        line = ''
        for kiddo in li.children:
            if kiddo.name == 'a' or type(kiddo) == NavigableString:
                line = line + kiddo.get_text()

        if line != '':
            line = line.strip()
            lines.append(line)

    return lines

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

# If the elem is None or is an empty NavigableString, return False
# TODO : Will this reject non-empty (valid) NavigableStrings?
def is_valid_elem(elem):
    if elem == None or not hasattr(elem, 'attrs'):
        return False
    return True

# Returns the next sibling element (ignoring invalid elements)
def next_elem(elem):
    elem = elem.next_sibling
    while not is_valid_elem(elem):
        if elem == None:
            return None
        elem = elem.next_sibling
    return elem

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

# Returns from Wiktionary the definitions of the word
def search_defn(word):


    url_wiktionary = url_base_wiktionary + word
    r = None
    try:
        r = requests.get(url_wiktionary)
    except:
        print(f"ru search_defn: Link not valid (%s)" % url_wiktionary)
        sys.exit()
    html_doc = r.text

    soup = BeautifulSoup(html_doc, 'html.parser')

    defns = []

    # Finds the section header for Russian
    russian_sec_search = soup.find_all(id="Русский")

    if len(russian_sec_search) < 1:
        print("ru search_defn: Russian section not found")
        return

    # Goes up one level to get out of the Russian header element
    current_elem = russian_sec_search[0].parent

    while True:

        if current_elem == None:
            break

        current_elem = next_elem(current_elem)

        # There are often empty 'NavigableString's between elements.
        # This saves us from trying to query them
        if not is_valid_elem(current_elem):
            continue

        # If we're now past the Russian section, terminate the search
        if on_the_next_language(current_elem):
            break

        if on_definitions(current_elem):
            while not is_valid_elem(current_elem) or current_elem.name != "ol":
                current_elem = next_elem(current_elem)
            assert current_elem.name == "ol"
            new_defns = extract_defns(current_elem)
            defns.extend(new_defns)

    return defns
