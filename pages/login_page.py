
import time
import os
import json
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException, NoAlertPresentException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as expCond
from .base_page import BasePage, BasePageLocators
from .locators import LoginPageLocators


class LoginPage(BasePage):

    url = r"https://account.mail.ru/login"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def should_be_login_page(self):
        currentURL = self.webDriver.current_url
        assert currentURL[:len(LoginPage.url)] == LoginPage.url, "Not a login page url"
        assert self.is_element_present(*LoginPageLocators.LOGIN_FORM), "Login form is not present"
        return True
