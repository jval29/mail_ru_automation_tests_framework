
import time
import os
import json
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException, NoAlertPresentException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as expCond
from .base_page import BasePage, BasePageLocators
from .locators import InboxPageLocators


class InboxPage(BasePage):

    url = r"https://e.mail.ru/inbox/"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def should_be_inbox_page(self):
        currentURL = self.webDriver.current_url
        print(currentURL)
        assert currentURL[:len(InboxPage.url)] == InboxPage.url, "Not an inbox page url"
        inboxButton = self.wait_element(*BasePageLocators.LINK_INBOX_HEADER)
        inboxButtonClass = inboxButton.get_attribute("class")
        assert "ph-project_current" in inboxButtonClass, "Inbox button is not marked as current"
        return True
