
import time
import os
import json
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException, NoAlertPresentException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as expCond
from .base_page import BasePage, BasePageLocators
from .locators import MainPageLocators, LoginFrameLocators


class MainPage(BasePage):

    URL = r"https://mail.ru"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def should_be_main_page(self):
        currentURL = self.webDriver.current_url
        assert currentURL[:len(MainPage.URL)] == MainPage.URL, "Not a main page url"
        homeButton = self.wait_element(*BasePageLocators.LINK_HOME_HEADER)
        homeButtonClass = homeButton.get_attribute("class")
        assert "ph-project_current" in homeButtonClass, "Home button is not marked as current"
        return True

