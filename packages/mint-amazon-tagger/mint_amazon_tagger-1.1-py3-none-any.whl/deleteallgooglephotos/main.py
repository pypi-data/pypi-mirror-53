#!/usr/bin/env python3

# This script deletes all of your Photos from Google Photos.

import argparse
import io
import logging
import os
from sys import platform as _platform
import time
import zipfile

#from outdated import check_outdated, warn_if_outdated
import requests
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException, StaleElementReferenceException, TimeoutException, WebDriverException
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver

from deleteallgooglephotos import VERSION

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)


def main():
    # Enable once PyPI is setup.
    # warn_if_outdated('delete-all-google-photos', VERSION)
    # is_outdated, latest_version = check_outdated(
    #     'delete-all-google-photos', VERSION)
    # if is_outdated:
    #     print('Please update your version by running:\n'
    #           'pip3 install delete-all-google-photos --upgrade')

    parser = argparse.ArgumentParser(
        description='Deletes all of your Photos from Google Photos.')
    parser.add_argument(
        '-V', '--version', action='store_true',
        help='Shows the app version and quits.')
    args = parser.parse_args()

    if args.version:
        print('delete-all-google-photos {}\nBy: Jeff Prouty'.format(VERSION))
        exit(0)

    logger.info('Launching a browser window and waiting for you to login to '
                'Google Photos.')
    driver = get_web_driver()
    logger.info('Now logged into Google Photos. Time to delete!')

    more_to_check = True
    while more_to_check:
        more_to_check = False
        checkboxes = driver.find_elements_by_xpath('//*[@role="checkbox"]')
        ordered_boxes = [
            c for c in checkboxes
            if 'Select all photos from ' in c.get_attribute('aria-label')
        ] + [
            c for c in checkboxes
            if 'Select all photos from ' not in c.get_attribute('aria-label')
        ]
        for c in checkboxes:
            try:
                # Skip already checked boxes
                if 'true' == c.get_attribute('aria-checked'):
                    continue
                ActionChains(driver).move_to_element(c).click().pause(
                    0.25).perform()
                more_to_check = True
            except StaleElementReferenceException:
                # This can happen when scrolling around too much while selecting
                pass

        selected_label = driver.find_element_by_xpath(
            '//*[contains(text(), " selected")]')
        logger.info(selected_label.text)
        delete_button = driver.find_element_by_xpath(
            '//*[@aria-label="Delete"]')
        logger.info('Pressing delete now')
        ActionChains(driver).move_to_element(
            delete_button).pause(1).click().perform()
        # One is hidden, only click the visible one.
        logger.info('Pressing confirm/move to trash now')
        trashes = driver.find_elements_by_xpath('//*[text()="Move to trash"]')
        for t in trashes:
            if not t.is_displayed():
                continue
            ActionChains(driver).move_to_element(t).pause(1).click().perform()
            # Only click once!
            break
        # Wait for the delete to complete (by looking for the search bar again)
        wait_cond = EC.visibility_of_element_located(
            (By.XPATH, '//*[@aria-label="Search your photos"]'))
        WebDriverWait(driver, 20).until(wait_cond)

    logger.info('All done')

CHROME_DRIVER_VERSION = 2.41
CHROME_DRIVER_BASE_URL = 'https://chromedriver.storage.googleapis.com/%s/chromedriver_%s.zip'
CHROME_ZIP_TYPES = {
    'linux': 'linux64',
    'linux2': 'linux64',
    'darwin': 'mac64',
    'win32': 'win32',
    'win64': 'win32'
}

def get_web_driver():
    zip_type = ""
    executable_path = os.getcwd() + os.path.sep + 'chromedriver'
    if _platform in ['win32', 'win64']:
        executable_path += '.exe'

    zip_type = CHROME_ZIP_TYPES.get(_platform)

    if not os.path.exists(executable_path):
        zip_file_url = CHROME_DRIVER_BASE_URL % (CHROME_DRIVER_VERSION, zip_type)
        request = requests.get(zip_file_url)

        if request.status_code != 200:
            raise RuntimeError('Error finding chromedriver at %r, status = %d' %
                               (zip_file_url, request.status_code))
        zip_file = zipfile.ZipFile(io.BytesIO(request.content))
        zip_file.extractall()
        os.chmod(executable_path, 0o755)

    chrome_options = ChromeOptions()
    driver = webdriver.Chrome(options=chrome_options, executable_path="%s" % executable_path)
    driver.get("https://photos.google.com")
    driver.implicitly_wait(2)  # seconds

    # Wait up to 5 minutes for the user to login.
    wait_cond = EC.presence_of_element_located((By.XPATH, '//*[@aria-label="Search your photos"]'))
    WebDriverWait(driver, 60 * 5).until(wait_cond)
    return driver


if __name__ == '__main__':
    main()
