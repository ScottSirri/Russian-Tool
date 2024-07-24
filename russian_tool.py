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


"""
sentences = soup.find("div", "section sentences").find_all("li")
for sentence in sentences:
    parts = sentence.find_all("span", recursive=False)
    russ_pre = parts[0].get_text()
    russ = russ_pre
    eng = parts[1].get_text()
    if russ[len(russ) - 1] == '.':
        print("period")
        russ = russ_pre[:len(russ_pre) - 2]
    print(russ + " = " + eng)
"""

def open_decl(soup):
    declension_cells = soup.find("div", "section declension noun").find_all("td")
    for cell in declension_cells:
        decls = cell.find_all("p")
        for decl in decls:
            print(decl.get_text())


def wiki_decl(soup):

    russian_sec_search = soup.find_all(id="Russian")

    if len(russian_sec_search) < 1:
        print("Russian section not found")
        return

    current_elem = russian_sec_search[0].parent

    while True:
        #print()
        current_elem = current_elem.next_sibling

        if current_elem == None:
            #print("current_elem == None")
            break

        #print(type(current_elem))

        """
        if hasattr(current_elem, 'attrs'):
            print('attrs:', end='')
            print(current_elem.attrs)
            print('content:', end='')
            print(current_elem)
        else:
            print("skipping:", end='')
            print(current_elem)
            continue
        """
        if not hasattr(current_elem, 'attrs'):
            continue

        if "class" in current_elem.attrs and "mw-heading2" in current_elem["class"]:
            #print("CAPTAIN WE'RE OVERFLOWING")
            break

        if current_elem.name == 'ol':
            #print("current_elem.name == ol")
            lis = current_elem.children
            for li in lis:
                line = ''
                if li.name == None:
                    continue
                j = 0
                for kiddo in li.children:
                    j += 1
                    if kiddo.name != 'a' and kiddo.name != None and kiddo.name != 'span':
                        break
                    line  = line + kiddo.get_text()
                line = line.strip()
                print('\t' + line)
        #current_elem = current_elem.next_sibling

wiki_decl(soup_outer)
