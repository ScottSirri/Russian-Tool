import requests
import sys

url = ''

if len(sys.argv) > 1:
    word = sys.argv[1]
    url = 'https://en.wiktionary.org/wiki/' + word

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
    lis = elem.children

    for li in lis:

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
        print('\t' + line)

    return lines

# Returns the definitions, declensions, conjugations, and related terms
# (as applicable) in the Russian section of the given soup element.
def wiki_decl(soup):
    defns = []
    decl = []
    conj = []
    related = []

    # Finds the section header for Russian
    russian_sec_search = soup.find_all(id="Russian")

    if len(russian_sec_search) < 1:
        print("Russian section not found")
        return

    # Goes up one level to get out of the Russian header element
    current_elem = russian_sec_search[0].parent

    while True:
        current_elem = current_elem.next_sibling

        if current_elem == None:
            break

        # There are often empty 'NaviagableString's between elements.
        # This saves us from trying to query them
        if not hasattr(current_elem, 'attrs'):
            continue

        # If we're now past the Russian section, terminate the search
        if on_the_next_language(current_elem):
            break

        if on_definitions(current_elem):
            defns = extract_defns(current_elem)

        if on_new_subsection(current_elem):
            # Handle this
            print()

wiki_decl(soup_outer)
