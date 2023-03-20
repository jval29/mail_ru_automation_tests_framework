
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

    URL = r"https://e.mail.ru/inbox/"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def should_be_inbox_page(self):
        currentURL = self.webDriver.current_url
        assert "mail.ru/inbox" in currentURL, "Not an inbox page url"
        inboxButton = self.wait_element(*BasePageLocators.LINK_INBOX_HEADER)
        inboxButtonClass = inboxButton.get_attribute("class")
        assert "ph-project_current" in inboxButtonClass, "Inbox button is not marked as current"
        return True

    def should_not_be_inbox_page(self):
        currentURL = self.webDriver.current_url
        assert "mail.ru/inbox" not in currentURL, "It is inbox page url"
        inboxButton = self.wait_element(*BasePageLocators.LINK_INBOX_HEADER)
        inboxButtonClass = inboxButton.get_attribute("class")
        assert "ph-project_current" not in inboxButtonClass, "Inbox button is marked as current"
        return True

    def unread_emails_should_be_equal_to_counter(self, counterValue: int = None):
        if not counterValue:
            counter = self.wait_element(*BasePageLocators.UNREAD_EMAIL_COUNTER_HEADER)
            counterValue = int(counter.text.strip())
        unreadEmails = self.wait_elements(*InboxPageLocators.UNREAD_EMAIL_MARK)
        assert counterValue == len(unreadEmails),\
            f"Unread emails quantity ({len(unreadEmails)}) is not equal to counter ({counterValue})"
        return True

