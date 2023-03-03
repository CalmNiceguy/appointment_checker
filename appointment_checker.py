from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
import time
import random

options = Options()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(chrome_options=options)


xpaths = [
    # Sick or injured
    '//*[@id="page"]/section[2]/div/div/div[2]/div[1]/div[1]/a',

    # Current Patient
    '/html/body/app-root/div[1]/div/app-patient-type-selection-page/div/div[2]/app-select-patient-type/div/div[2]',

    # Dropdown arrow
    '/html/body/app-root/div[1]/div/app-slot-questions-page/div[2]/app-custom-questions/app-custom-form/form/div/div/div[2]/app-custom-search-input/div/div/phreesia-search-input/div/div/span',

    # In Clinic
    '/html/body/app-root/div[1]/div/app-slot-questions-page/div[2]/app-custom-questions/app-custom-form/form/div/div/div[2]/app-custom-search-input/div/div/phreesia-search-input/div/ul/li[1]',

    # Continue
    '/html/body/app-root/div[1]/div/app-slot-questions-page/div[2]/app-custom-questions/div/div/button',

    # # Visit type dropdown
    # '/html/body/app-root/div[1]/div/app-select-slot-page/div/app-slot-search/app-appt-details/div/div[1]/div[1]/app-visit-type/div/phreesia-search-input/div/div/input',

    # didn't get dropdown items for Visit type yet

    # Location dropdown
    '/html/body/app-root/div[1]/div/app-select-slot-page/div/app-slot-search/app-appt-details/div/div[1]/div[2]/app-location/div/div[2]/app-location-multiple/phreesia-search-input-multiple/div/phreesia-search-input-text/div/input',

    # Location - Any, first available checkbox
    '/html/body/app-root/div[1]/div/app-select-slot-page/div/app-slot-search/app-appt-details/div/div[1]/div[2]/app-location/div/div[2]/app-location-multiple/phreesia-search-input-multiple/div/div/div/ul/li[1]/span/input',

    # Provider dropdown
    '/html/body/app-root/div[1]/div/app-select-slot-page/div/app-slot-search/app-appt-details/div/div[1]/div[3]/app-provider/div/div[2]/app-provider-multiple/phreesia-search-input-multiple/div/phreesia-search-input-text/div/input',

    # Provider- Any, first available checkbox
    '/html/body/app-root/div[1]/div/app-select-slot-page/div/app-slot-search/app-appt-details/div/div[1]/div[3]/app-provider/div/div[2]/app-provider-multiple/phreesia-search-input-multiple/div/div/div/ul/li/span/input',
    
    # Background of page
    '/html/body/app-root',

    # Calendar button
    # '/html/body/app-root/div[1]/div/app-select-slot-page/div/app-slot-search/div[3]/app-slot-search-days/app-slot-search-days-header/div[1]/button[1]', 

]

lastCheckAppointmentsAvailable = False

def mywait():
    driver.implicitly_wait(10)

def document_initialised(driver):    
    # check for Available Appointments text showing
    return driver.find_element(By.XPATH, '/html/body/app-root/div[1]/div/app-select-slot-page/div/app-slot-search/div[3]/app-slot-search-days/app-slot-search-days-header/div[1]/div[1]').is_displayed()

def checkPage():
    global lastCheckAppointmentsAvailable

    # Load a web page
    driver.get("https://www.allegropediatrics.com/scheduling-an-appointment")
    for xp in xpaths:
        mywait()
        # Find the button on the web page and click it
        driver.find_element(By.XPATH, xp).click()
    print('Starting to wait for appointments to load..')

    try:
        WebDriverWait(driver, timeout=20).until(document_initialised)
    except TimeoutException:
        print('TimeoutException happened')

    time.sleep(1)
    print('Now checking for warning sign...')

    # check if warning icon img is showing
    if driver.find_element(By.XPATH, '/html/body/app-root/div[1]/div/app-select-slot-page/div/app-slot-search/app-no-slots-messages/div/div[1]/img').is_displayed():
        print("Found Warning Sign")
        lastCheckAppointmentsAvailable = False
    else:
        print('No warning sign was found, so there must be some available appointments')
        lastCheckAppointmentsAvailable = False

while True:
    checkPage()
    numSecondsToWait = random.randrange(9, 50, 1)
    if lastCheckAppointmentsAvailable:
        print('Last check there were some new appointments!')
    else:
        print('Last check there were no appointments available.')
    print('waiting for ' + str(numSecondsToWait) + ' seconds...')
    time.sleep(numSecondsToWait)

