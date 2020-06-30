import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

APP_ENV = "SDI test"

browser = webdriver.Chrome()
browser.get('http://fs3s-wms/mc_web/onsite/default.htm')

# Access the login page
loginPageBtn = browser.find_element_by_name('alogin')
loginPageBtn.send_keys(Keys.RETURN)

# Login using admin credentials
usernameInput = browser.find_element_by_name('fld_membername')
usernameInput.send_keys('admin')

passwordInput = browser.find_element_by_name('fld_password')
passwordInput.send_keys(os.environ['WMS_PW'])

# This is an img with a click event
loginBtn = browser.find_element_by_css_selector("img[src='images/mc_okbutton_opt.jpg']")
loginBtn.send_keys(Keys.RETURN)

time.sleep(2)

testEnvBtns = browser.find_elements_by_class_name('browseicon')
print(testEnvBtns)
for el in testEnvBtns:
    print(el.text)
    # if el.text == APP_ENV:
    #     el.send_keys(Keys.RETURN)

