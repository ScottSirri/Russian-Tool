import sys, requests

try: 
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup

url_base_syn = "https://www.textsale.ru/index.php?sword="

# DO NOT TRY TO WRAP THESE STRINGS WEIRD THINGS HAPPEN ITS NOT WORTH IT
cyrillic_key = """АаБбВвГгДдЕеЁёЖжЗзИиЙйКкЛлМмНнОоПпРрСсТтУуФфХхЦцЧчШшЩщЪъЫыЬьЭэЮюЯя"""

# The URL system converts Cyrillic systems to this encoding I'm not familiar
# with and I'm not shedding any more of my blood sweat or tears trying to
# figure it out (I googled aimlessly for like 20 minutes), just used it to
# generate a key for me
encoded_key = """%C0%E0%C1%E1%C2%E2%C3%E3%C4%E4%C5%E5%A8%B8%C6%E6%C7%E7%C8%E8%C9%E9%CA%EA%CB%EB%CC%EC%CD%ED%CE%EE%CF%EF%D0%F0%D1%F1%D2%F2%D3%F3%D4%F4%D5%F5%D6%F6%D7%F7%D8%F8%D9%F9%DA%FA%DB%FB%DC%FC%DD%FD%DE%FE%DF%FF"""

# Given a Cyrillic character, return the URL encoding of it
def encode_char(char):
    if type(char) != str or len(char) != 1:
        print("char_to_marc8 received invalid input")
    try:
        ind = cyrillic_key.index(char)
    except ValueError:
        print("""encode_char: Passed string contained a non-Cyrillic character 
              (did you remember to strip accented characters?)""")
        return ""
    return encoded_key[3*ind:3*ind+3]

# Encode a Cyrillic string to the URL encoding
def encode(string):
    ret = ""
    for char in string:
        ret = ret + encode_char(char)
    return ret

def get_synonyms(word):
    encoded_word = encode(word)
    url = url_base_syn + encoded_word
    r = None
    try:
        r = requests.get(url)
    except:
        print(f"search_defn: Link not valid (%s)" % url)
        sys.exit()
    html_doc = r.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    syno_frame = soup.find("div", "panel panel-default panel-body lead")
    syno_frame = syno_frame.parent
    syno_as = syno_frame.find_all("a")
    synos = []
    for syno_a in syno_as:
        syno = syno_a.get_text()
        synos.append(syno)
    return synos

word = "сталкиваться"
synos = get_synonyms(word)
print("Synonyms for " + word)
for syno in synos:
    print("\t" + syno)
