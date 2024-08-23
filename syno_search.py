import sys, requests
from math import ceil, floor

try: 
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup

url_base_syn = "https://ruwordnet.ru/en/search/"

def get_synonyms(word, recursive_level=0, cutoff=99999):
    url = url_base_syn + word
    r = None
    try:
        r = requests.get(url)
    except:
        print(f"search_defn: Link not valid (%s)" % url)
        sys.exit()
    html_doc = r.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    syno_frame = soup.find("div", "senses")
    if syno_frame == None:
        return []
    links = syno_frame.find_all("a")
    synos = []
    for syno_a in links:
        syno = syno_a.get_text()

        if "." in syno or "(" in syno or ")" in syno:
            continue

        synos.append(syno.lower())
        cutoff -= 1
        if cutoff <= 0:
            break

    if recursive_level > 0 and cutoff > 0:
        # To get an even sampling across recursive branches
        adj_per_syno = floor(cutoff/len(synos))
        for syno in synos:
            adjacent_synos = get_synonyms(syno, recursive_level - 1, adj_per_syno)
            synos.extend(adjacent_synos)
    return synos
