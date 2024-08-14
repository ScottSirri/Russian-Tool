import requests
import sys

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

try: 
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup

url_base_yandex = "https://translate.yandex.com/examples/Russian-English/"
more_button_class = "dxri7VWzxK_2mtfgodWr"
wrong_class = "a"

# Returns from Wiktionary the definitions and misc information for a word or
# for each of a tuple of words
def search_exs(query):

    word = None
    exs = []

    if type(query) == list:
        for word in query:
            assert type(word) == str
            exs_word = search_exs(word)
            exs.extend(exs_word)
        return exs
    elif type(query) == str:
        word = query
    else:
        print("search_exs: Invalid query")
        return []

    url_yandex = url_base_yandex + word

    driver = webdriver.Chrome()
    driver.get(url_yandex)

    button_available = True
    try:
        driver.implicitly_wait(5)
        more_button = driver.find_element(By.CLASS_NAME, more_button_class)
    except NoSuchElementException:
        # Occurs if there is no "More examples" button. In theory could happen
        # if there's only one page of examples, but that seem unlikely because 
        # there's usually lots of sentences... check if something else went 
        # wrong!
        print("search_exs: No \"More examples\" button found")
        button_available = False

    while button_available:
        driver.implicitly_wait(2)
        try:
            more_button.click()
        except StaleElementReferenceException: 
            # Occurs when there are no more example sentences left (and 
            # therefore the "More examples" button disappears)
            #print("StaleElementReferenceException")
            button_available = False
    
    html_doc = driver.page_source
    print("search_exs: HTML DOC LEN: "  + str(len(html_doc)))
    soup = BeautifulSoup(html_doc, 'html.parser')
    ex_elems = soup.find_all("div", {"class" : "HPdYZk2E3bjTdcGIYdld"})
    if len(ex_elems) == 0:
        print("search_exs: No example sentences found in HTML doc")
        return []

    exs = []
    for elem in ex_elems:
        ex = []
        for kiddo in elem.children:
            ex.append(kiddo.get_text())
        exs.append(ex)
    for ex in exs:
        print(ex[0] + " = " + ex[1])
    return exs
