import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

from seed import newItemsList


# ===========================
#         CONSTANTS
# ===========================
LOG_FILENAME = 'app.log'

APP_ENV = 'TEST'
SLEEP_SHORT = 2
SLEEP_LONG = 4

MODULE_ID = 'CM'


# ===========================
#       LOGGING INIT
# ===========================
logging.basicConfig(filename=LOG_FILENAME, format='%(asctime)s %(levelname)s:%(message)s', level=logging.INFO)


# ===========================
#        DRIVER INIT
# ===========================
browser = webdriver.Chrome()
browser.get('http://fs3s-wms/mc_web/onsite/default.htm')


# ===========================
#           LOGIN
# ===========================
# Access the login page
loginPageBtn = browser.find_element_by_name('alogin')
loginPageBtn.send_keys(Keys.RETURN)

# Login using admin credentials
usernameInput = browser.find_element_by_name('fld_membername')
usernameInput.send_keys('admin')

passwordInput = browser.find_element_by_name('fld_password')
passwordInput.send_keys(os.environ['WMS_PW'])

# Click the login btn, which is an img with a click event
loginBtn = browser.find_element_by_css_selector(
    "img[src='images/mc_okbutton_opt.jpg']")
loginBtn.send_keys(Keys.RETURN)

# Log login
logging.info('Bot logged in.')

# TODO Replace sleeps with WebDriverWait
# Wait for DOM to load
time.sleep(SLEEP_SHORT)


# ===========================
#          APP ENV
# ===========================
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
time.sleep(SLEEP_SHORT)


# ===========================
#         APP SELECT
# ===========================
# Select `managerapp` from iframe
managerAppIframe = browser.find_element_by_css_selector('iframe[src="mc_appchoice.htm"]')
browser.switch_to.frame(managerAppIframe)
managerApp = browser.find_element_by_id('managerapp')
managerApp.click()

# Wait for DOM to load
time.sleep(SLEEP_LONG)

# Select the module by ID
modulesDropdown = browser.find_element_by_id('greenbardropdowntable')
modulesDropdown.click()
module = browser.find_element_by_css_selector('span[modid="{}"]'.format(MODULE_ID))
module.click()


# ===========================
#          NEW ITEM
# ===========================
# Fill out inputs using a list of dicts
for newItem in newItemsList:
    # Wait for DOM to load
    time.sleep(SLEEP_SHORT)

    # Select the new button to create an inventory item
    newItemBtn = browser.find_element_by_css_selector(
        "img[src='images/toolbar/new.jpg']")
    newItemBtn.click()

    # Wait for DOM to load
    time.sleep(SLEEP_SHORT)

    # Switch to iFrame containing inputs
    inputsIframe = browser.find_element_by_id('fraTopic')
    browser.switch_to.frame(inputsIframe)
    for inputId, val in newItem.items():
        companyIdInput = browser.find_element_by_id(inputId)
        companyIdInput.send_keys(val)

    # Switch back to main page
    browser.switch_to.default_content()

    # Wait for DOM to load
    time.sleep(SLEEP_SHORT)

    # Save the new item
    saveBtn = browser.find_element_by_css_selector(
        "img[src='images/toolbar/saveit.jpg']")
    saveBtn.click()

    # Wait for DOM to load
    time.sleep(SLEEP_SHORT)

    try:
        # Find alert for item ID exists
        alertIframe = browser.find_element_by_css_selector(
            "iframe[src='/mc_web/mapp_v12/mcalert.asp?title=Company Message']")
        browser.switch_to.frame(alertIframe)

        # Wait for DOM to load
        time.sleep(SLEEP_SHORT)

        # Close alert
        okBtn = browser.find_element_by_xpath(
            '//div[@id="bg_okprint"]/button')        
        okBtn.click()

        # Switch back to main page
        browser.switch_to.default_content()       

        # Write error to log
        logging.error('{0} was not added.'.format(newItem['txtCompany'])) 
    except NoSuchElementException:
        logging.info('{0} was added.'.format(newItem['txtCompany']))

    # Wait for DOM to load
    time.sleep(SLEEP_SHORT)

    cancelBtn = browser.find_element_by_css_selector(
        "img[src='images/toolbar/cancelit.jpg']")
    cancelBtn.click()

# Wait for DOM to load
time.sleep(SLEEP_SHORT)


# ===========================
#          LOG OFF
# ===========================
logoffBtn = browser.find_element_by_css_selector('img[src="images/toolbar/logoff3.jpg"]')
logoffBtn.click()

# Log logoff
logging.info('Bot logged out.')


# ===========================
#       CLOSE BROWSER
# ===========================
browser.close()