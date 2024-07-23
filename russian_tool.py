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
    russian_sec = soup.find_all(id="Russian")
    if len(russian_sec) < 1:
        print("Page not found")
        return
    elem = russian_sec[0].parent
    while True:
        if elem == None: # or elem is a tag ????
            break
        print(type(elem))
        if hasattr(elem, 'attrs'):
            print('attrs:', end='')
            print(elem.attrs)
            print('content:', end='')
            print(elem)
        else:
            print("skipping")
            elem = elem.next_sibling
            continue
        if "mw-heading2" in elem["class"]:
            print("CAPTAIN WE'RE OVERFLOWING")
        if elem.name == 'ol':
            lis = elem.children
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
        elem = elem.next_sibling

wiki_decl(soup_outer)
