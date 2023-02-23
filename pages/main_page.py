
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

    url = r"https://mail.ru"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

