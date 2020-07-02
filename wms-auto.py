import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

# ===========================
#         CONSTANTS
# ===========================
APP_ENV = 'TEST'
SLEEP_SHORT = 2
SLEEP_LONG = 4

MANAGER_APP_IFRAME_SRC = 'http://fs3s-wms/mc_web/onsite/mc_appchoice.htm'
MODULE_ID = 'CM'

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



# ===========================
#          NEW ITEM
# ===========================
# Fill out inputs using a list of dicts
newItemsList = [
    {
        'txtCompany': 'test-0',
        'txtCompanyName': 'Test Company 0',
        'txtType': 'V',
        'txtAddress': '9999 Test Drive',
        'txtCity': 'Testtown',
        'txtState': 'Teststate',
        'txtZip': '99999',
        'txtTaxRate': '9'
    },
     {
        'txtCompany': 'test-1',
        'txtCompanyName': 'Test Company 1',
        'txtType': 'V',
        'txtAddress': '9999 Test Drive',
        'txtCity': 'Testtown',
        'txtState': 'Teststate',
        'txtZip': '99999',
        'txtTaxRate': '9'
    },
     {
        'txtCompany': 'test-2',
        'txtCompanyName': 'Test Company 2',
        'txtType': 'V',
        'txtAddress': '9999 Test Drive',
        'txtCity': 'Testtown',
        'txtState': 'Teststate',
        'txtZip': '99999',
        'txtTaxRate': '9'
    },
     {
        'txtCompany': 'test-3',
        'txtCompanyName': 'Test Company 3',
        'txtType': 'V',
        'txtAddress': '9999 Test Drive',
        'txtCity': 'Testtown',
        'txtState': 'Teststate',
        'txtZip': '99999',
        'txtTaxRate': '9'
    },
     {
        'txtCompany': 'test-4',
        'txtCompanyName': 'Test Company 4',
        'txtType': 'V',
        'txtAddress': '9999 Test Drive',
        'txtCity': 'Testtown',
        'txtState': 'Teststate',
        'txtZip': '99999',
        'txtTaxRate': '9'
    },
]

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
        alertIframe = browser.find_element_by_css_selector(
            "iframe[src='/mc_web/mapp_v12/mcalert.asp?title=Company Message'")
    except NoSuchElementException:
        print("Item added")

    # Wait for DOM to load
    time.sleep(SLEEP_SHORT)

    cancelBtn = browser.find_element_by_css_selector(
        "img[src='images/toolbar/cancelit.jpg']")
    cancelBtn.click()

