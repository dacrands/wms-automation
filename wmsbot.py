import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
browser.get(os.environ['BASE_URL'])
browser.set_network_conditions(latency=200, download_throughput=150 * 1024, upload_throughput=150 * 1024,)
wait = WebDriverWait(browser, 20)


# ===========================
#           LOGIN
# ===========================
# Access the login page
loginPageBtn = wait.until(
    EC.presence_of_element_located((By.ID, 'MCLogin'))
).send_keys(Keys.RETURN)

# Username input
wait.until(
    EC.presence_of_element_located((By.ID, 'Email'))
).send_keys('admin')

# Password input
wait.until(
    EC.presence_of_element_located((By.ID, 'Password'))
).send_keys(os.environ['WMS_PW'])

# Login input
wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="submit"]'))
).send_keys(Keys.RETURN)

# Log login
logging.info('Bot logged in.')


# ===========================
#          APP ENV
# ===========================
# There are two buttons, one for each env (TEST and PROD)
# Click the first to access TEST click the second to access PROD
testEnvBtns = wait.until(
    EC.visibility_of_all_elements_located((By.CLASS_NAME, 'panel-with-icon'))
)

if APP_ENV == 'TEST':
    testEnvBtns[0].click()
elif APP_ENV == 'PROD':
    testEnvBtns[1].click()
else:
    print('Please set APP_ENV to either TEST or PROD')

# ===========================
#         APP SELECT
# ===========================
# Select `managerapp`
wait.until(
    EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "Maintenance, Repair & Operations Work Center")]'))
).click()

# Select the module dropdown
modulesDropdown = wait.until(
    EC.element_to_be_clickable((By.ID, 'greenbardropdowntable'))
)

# Overlay intercepts click so wait for it to be gone, then click
checkOverlayIsGone = wait.until(
    EC.invisibility_of_element((By.ID, 'mccover'))
)
modulesDropdown.click()

# Select the proper module
wait.until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, 'span[modid="{}"]'.format(MODULE_ID)))
).click()


# ===========================
#          NEW ITEM
# ===========================
# Fill out inputs using a list of dicts
for newItem in newItemsList:    
    # Select the new button to create an inventory item
    newItemBtn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "img[src='images/toolbar/new.jpg']"))
    ).click()

    # Wait for DOM to load
    time.sleep(SLEEP_SHORT)

    # Switch to iFrame containing inputs
    wait.until(
        EC.frame_to_be_available_and_switch_to_it((By.ID, 'fraTopic'))
    )
    for inputId, val in newItem.items():        
        wait.until(
            EC.element_to_be_clickable((By.ID, inputId))
        ).send_keys(val)

    # Switch back to main page
    browser.switch_to.default_content()

    # Save the new item
    wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "img[src='images/toolbar/saveit.jpg']"))
    ).click()    

    try:
        # Wait for DOM to load
        time.sleep(SLEEP_SHORT)

        # Find alert for item ID exists
        alertIframe = browser.find_element_by_css_selector(
            "iframe[src='/mc_web/mapp_v12/mcalert.asp?title=Company Message']")
        browser.switch_to.frame(alertIframe)

        # Close alert
        wait.until(
            EC.presence_of_element_located((By.XPATH, '//div[@id="bg_okprint"]/button'))
        ).click()        

        # Switch back to main page
        browser.switch_to.default_content()       

        # Write error to log
        logging.error('{0} was not added.'.format(newItem['txtCompany'])) 
    except NoSuchElementException:
        logging.info('{0} was added.'.format(newItem['txtCompany']))

    # Occasionally the cancel button does not appear
    try:
        # Click the `cancel` button
        wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'img[src="images/toolbar/cancelit.jpg"]'))
        ).click()
    except TimeoutException:
        pass 


# ===========================
#          LOG OFF
# ===========================
# Log off bot
wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'img[src="images/toolbar/logoff3.jpg"]'))
).click()

# Log log off
logging.info('Bot logged out.')


# ===========================
#       CLOSE BROWSER
# ===========================
browser.close()