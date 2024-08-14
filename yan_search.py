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

# Returns from Wiktionary the definitions and misc information for a word
def search_exs(query):

    word = None
    exs = []

    if type(query) == list:
        for word in query:
            exs_word = search_exs(word)
            exs.extend(exs_word)
        return exs
    elif type(query) == str:
        word = query
    else:
        print("search_exs: Invalid query")

    url_yandex = url_base_yandex + word

    driver = webdriver.Chrome()
    driver.get(url_yandex)
    print("search_exs: driver.title = " + driver.title)

    wait = WebDriverWait(driver, 3)
    driver.implicitly_wait(5)
    more_button = driver.find_element(By.CLASS_NAME, more_button_class)

    while True:
        print("waiting (loop)")
        driver.implicitly_wait(2)
        print("clicking")

        try:
            more_button.click()
        except StaleElementReferenceException:
            print("StaleElementReferenceException")
            break
    
    html_doc = driver.page_source
    print("search_exs: HTML DOC LEN: "  + str(len(html_doc)))
    soup = BeautifulSoup(html_doc, 'html.parser')
    ex_app = soup.find(id="examplesApp")
    print(ex_app.get_text())

    
