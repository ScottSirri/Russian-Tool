from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Simple proof of concept that a string of Russian text may be submitted to
# russiangram.com to add appropriate stress marks to the text

driver = webdriver.Chrome()
driver.get("https://russiangram.com/")
print(driver.title)
assert "Russian" in driver.title
text_box = driver.find_element(By.NAME, "ctl00$MainContent$UserSentenceTextbox")
text_box.clear()
text_box.send_keys("яблоко")

submit_button = driver.find_element(By.NAME, "ctl00$MainContent$SubmitButton")
submit_button.click()

text_box = driver.find_element(By.NAME, "ctl00$MainContent$UserSentenceTextbox")
wait = WebDriverWait(driver, 10)
wait.until(EC.visibility_of(text_box))

print(text_box.text)
