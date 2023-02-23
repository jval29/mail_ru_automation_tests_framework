
import time
import os
import json
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException, NoAlertPresentException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as expCond
from .locators import BasePageLocators


class BasePage():

    def __init__(self, webDriver, url=None, timeout=None):
        self.webDriver = webDriver
        if url:
            self.url = url
        else:
            self.url = webDriver.current_url
        if timeout:
            self.webDriver.implicitly_wait(timeout)
        if isinstance(webDriver, webdriver.Firefox):
            self.increaseTimeout = 5
        elif isinstance(webDriver, webdriver.Chrome):
            self.increaseTimeout = 0
        self.actChain = ActionChains(webDriver)

    def check_document_state(self, timeLimit=10):
        for _ in range(timeLimit*2):
            state = self.webDriver.execute_script("return document.readyState")
            if state == "complete":
                return True
            time.sleep(0.5)

    def is_element_present(self, by, locator, timeout=3):
        try:
            self.wait_element(by, locator, timeout)
            return True
        except TimeoutException:
            return False

    def is_not_element_present(self, by, locator, timeout=3):
        try:
            self.wait_element(by, locator, timeout)
            return False
        except TimeoutException:
            return True

    def is_element_disappeared(self, by, locator, timeout=3):
        timeout += self.increaseTimeout
        self.check_document_state()
        try:
            WebDriverWait(self.webDriver, timeout, 0.5, [TimeoutException]).until_not(
                expCond.presence_of_element_located((by, locator)))
            return True
        except TimeoutException:
            return False

    def move_n_click(self, element):
        self.actChain.reset_actions()
        self.actChain.move_to_element_with_offset(element, 1, 1).pause(0.05).click()
        self.actChain.perform()

    def open(self, url=None):
        if not url:
            url = self.url
        self.webDriver.get(url)

    def should_be_authorized_user(self):
        assert self.is_element_present(*BasePageLocators.USER_PROFILE_BUTTON), \
            "User profile icon not found, probably non-authorized user"
        assert self.is_not_element_present(*BasePageLocators.LOGIN_BUTTON_HEADER), \
            "Login button is present, probably non-authorized user"
        return True

    def should_not_be_authorized_user(self):
        assert self.is_not_element_present(*BasePageLocators.USER_PROFILE_BUTTON), \
            "User profile icon is present, probably authorized user"
        assert self.is_element_present(*BasePageLocators.LOGIN_BUTTON_HEADER), \
            "Login button not found, probably authorized user"
        return True

    def typing(self, text_string):
        for symbol in text_string:
            self.actChain.reset_actions()
            self.actChain.key_down(symbol).pause(0.02).key_up(symbol)
            self.actChain.perform()

    def wait_element(self, by, locator, timeout=3):
        timeout += self.increaseTimeout
        self.check_document_state()
        element = WebDriverWait(self.webDriver, timeout).until(expCond.presence_of_element_located((by, locator)))
        return element

    def wait_elements(self, by, locator, timeout=3):
        timeout += self.increaseTimeout
        self.check_document_state()
        elements = WebDriverWait(self.webDriver, timeout).until(expCond.presence_of_all_elements_located((by, locator)))
        return elements
