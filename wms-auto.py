import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

APP_ENV = "TEST"
MANAGER_APP_IFRAME_SRC = "http://fs3s-wms/mc_web/onsite/mc_appchoice.htm"
SLEEP_TIME = 2

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
time.sleep(SLEEP_TIME)

# There are two buttons, one for each env (TEST and PROD)
# Click the first to access TEST click the second to access PROD
testEnvBtns = browser.find_elements_by_class_name('browseicon')

if APP_ENV == 'TEST':
    testEnvBtns[0].click()
elif APP_ENV == 'PROD':
    testEnvBtns[1].click()
else:
    print('Please set APP_ENV to either TEST or PROD')

# Wait for DOM to load
time.sleep(SLEEP_TIME)

# Select `managerapp` from iframe
appIframes = browser.find_elements_by_tag_name('iframe')
for frame in appIframes:    
    if frame.get_attribute('src') == MANAGER_APP_IFRAME_SRC:        
        browser.switch_to.frame(frame)        
        managerApp = browser.find_element_by_id('managerapp')
        managerApp.click()
        break

# Wait for DOM to load
time.sleep(4)

# greenbardropdowntable
modulesDropdown = browser.find_element_by_id('greenbardropdowntable')
modulesDropdown.click()
moduleItems = browser.find_elements_by_class_name('mitem')
for mod in moduleItems:
    if mod.get_attribute('modid') == 'IN':        
        mod.click()
        break
