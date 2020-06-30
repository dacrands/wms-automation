import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

APP_ENV = "TEST"
SLEEP_SHORT = 2
SLEEP_LONG = 4

MANAGER_APP_IFRAME_SRC = 'http://fs3s-wms/mc_web/onsite/mc_appchoice.htm'
MODULE_ID = 'CM'

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

# Login
# This is an img with a click event
loginBtn = browser.find_element_by_css_selector("img[src='images/mc_okbutton_opt.jpg']")
loginBtn.send_keys(Keys.RETURN)

# Wait for DOM to load
time.sleep(SLEEP_SHORT)

# There are two buttons, one for each env (TEST and PROD)
# Click the first to access TEST click the second to access PROD
testEnvBtns = browser.find_elements_by_class_name('browseicon')

if APP_ENV == 'TEST':
    testEnvBtns[0].click()
elif APP_ENV == 'PROD':
    testEnvBtns[1].click()
else:
    print('Please set APP_ENV to either TEST or PROD')

# TODO Replace sleeps with WebDriverWait
# Wait for DOM to load
time.sleep(SLEEP_SHORT)

# Select `managerapp` from iframe
appIframes = browser.find_elements_by_tag_name('iframe')
for frame in appIframes:    
    if frame.get_attribute('src') == MANAGER_APP_IFRAME_SRC:        
        browser.switch_to.frame(frame)        
        managerApp = browser.find_element_by_id('managerapp')
        managerApp.click()
        break

# Wait for DOM to load
time.sleep(SLEEP_LONG)

# Select the module by ID
modulesDropdown = browser.find_element_by_id('greenbardropdowntable')
modulesDropdown.click()
moduleItems = browser.find_elements_by_class_name('mitem')
for mod in moduleItems:
    if mod.get_attribute('modid') == MODULE_ID:        
        mod.click()
        break

# Wait for DOM to load
time.sleep(SLEEP_SHORT)

# Select the new button to create
# an inventory item
newItemBtn = browser.find_element_by_css_selector("img[src='images/toolbar/new.jpg']")
newItemBtn.click()

# Wait for DOM to load
time.sleep(SLEEP_SHORT)

# Switch to iFrame containing inputs
inputsIframe = browser.find_element_by_id('fraTopic')
browser.switch_to.frame(inputsIframe)

# Fill out inputs
inputsDict = {
    'txtCompany': '999999',
    'txtCompanyName': 'Test Company',
    'txtType': 'V'
}

for inputId, val in inputsDict.items():
    companyIdInput = browser.find_element_by_id(inputId)
    companyIdInput.send_keys(val)
