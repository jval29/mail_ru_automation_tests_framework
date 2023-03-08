
import time
import os
import json
import pickle
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException, NoAlertPresentException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as expCond
from .locators import BasePageLocators, LoginFrameLocators


authDataPath = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "auth_data.json"))
cookiesDirectory = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "tmp", "cookies"))


class BasePage():

    def __init__(self, webDriver: webdriver, url=None, timeout=None):
        self.webDriver = webDriver
        if url:
            self.URL = url
        else:
            self.URL = webDriver.current_url
        if timeout:
            self.webDriver.implicitly_wait(timeout)
        if isinstance(webDriver, webdriver.Firefox):
            self.increaseTimeout = 1
        elif isinstance(webDriver, webdriver.Chrome):
            self.increaseTimeout = 0
        self.actChain = ActionChains(webDriver)
        self.keyTable = Keys
        self.sessionID = None
        self.cookies = None

    def check_document_state(self, timeLimit=10):
        for _ in range(timeLimit*2):
            state = self.webDriver.execute_script("return document.readyState")
            if state == "complete":
                return True
            time.sleep(0.5)

    def cookies_accept(self):
        try:
            cookiesAcceptButton = self.wait_element(*BasePageLocators.COOKIE_ACCEPT_BUTTON)
            self.move_n_click(cookiesAcceptButton)
        except TimeoutException:
            pass

    def cookies_decline(self):
        try:
            cookiesDeclineButton = self.wait_element(*BasePageLocators.COOKIE_DECLINE_BUTTON)
            self.move_n_click(cookiesDeclineButton)
        except TimeoutException:
            pass

    def cookies_save(self, cookies_path=None, writeCookies=False):
        if not cookies_path:
            cookies_path = os.path.abspath(os.path.join(cookiesDirectory, "cookies"))
        cookies = self.webDriver.get_cookies()
        if not writeCookies:
            return cookies
        else:
            with open(cookies_path, 'wb') as fileObj:
                pickle.dump(cookies, fileObj)

    def cookies_load(self, cookies_path=None, tempCookies=None):
        if not cookies_path:
            cookies_path = os.path.abspath(os.path.join(cookiesDirectory, "cookies"))
        if tempCookies:
            cookies = tempCookies
        else:
            with open(cookies_path, 'rb') as fileObj:
                cookies = pickle.load(fileObj)
        for cookie in cookies:
            cookie["domain"] = ".mail.ru"
            try:
                self.webDriver.add_cookie(cookie)
            finally:
                continue

    def get_auth_data(self, option=None, path=None):
        if not option:
            option = "valid"
        if not path:
            path = authDataPath
        with open(path, "r") as fileObj:
            authData = json.load(fileObj)
        __user = authData[option]["user"]
        __domainOption = authData[option]["domain"]
        __domainName = authData["domain_options"][__domainOption]
        __pwd = authData[option]["pwd"]
        return __user, __domainOption, __domainName, __pwd

    def is_element_present(self, by, locator, timeout=3):
        try:
            self.wait_element(by, locator, timeout)
            return True
        except TimeoutException:
            return False

    def is_not_element_present(self, by, locator, delay=1):
        delay += self.increaseTimeout
        time.sleep(delay)
        try:
            self.wait_element(by, locator, 1)
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

    def is_element_visible(self, by, locator, timeout=3):
        timeout += self.increaseTimeout
        self.check_document_state()
        try:
            WebDriverWait(self.webDriver,timeout, 0.5, [TimeoutException]).until(
                expCond.visibility_of_element_located((by, locator)))
            return True
        except TimeoutException:
            return False

    def log_in(self, loginOption=None, __user=None, __domainOption=None, __domainName=None, __pwd=None,
               selectDomain=True, authDataPathLocal=None, saveAuth=False):
        if not __user:
            __user, __domainOption, __domainName, __pwd = self.get_auth_data(loginOption, authDataPathLocal)
        saveAuth = "true" if saveAuth else "false"
        self.open_login_frame()
        loginFrame = self.wait_element(*BasePageLocators.LOGIN_FRAME)
        self.webDriver.switch_to.frame(loginFrame)
        loginField = self.wait_element(*LoginFrameLocators.LOGIN_FIELD)
        self.move_n_click(loginField)
        self.typing(__user)
        if selectDomain:
            domainSelector = self.wait_element(*LoginFrameLocators.DOMAIN_SELECTOR)
            self.move_n_click(domainSelector)
            domainPoint = self.wait_elements(*LoginFrameLocators.DOMAIN_POINTS)[int(__domainOption)]
            self.move_n_click(domainPoint)
        else:
            self.move_n_click(loginField)
            self.typing(f"@{__domainName}")
        saveAuthCheckbox = self.wait_element(*LoginFrameLocators.SAVE_AUTH_CHECKBOX)
        autoAuthCheck = saveAuthCheckbox.get_attribute("data-checked")
        if autoAuthCheck.lower() != saveAuth:
            self.move_n_click(saveAuthCheckbox)
        nextButton = self.wait_element(*LoginFrameLocators.NEXT_BUTTON)
        self.move_n_click(nextButton)
        time.sleep(1)
        pwdField = self.wait_element(*LoginFrameLocators.PWD_FIELD)
        self.move_n_click(pwdField)
        self.typing(__pwd)
        submitButton = self.wait_element(*LoginFrameLocators.SUBMIT_BUTTON)
        self.move_n_click(submitButton)
        self.webDriver.switch_to.default_content()

    def login_ensure(self, cookiesLogin=True):
        try:
            self.should_be_authorized_user()
            return
        except AssertionError:
            if not cookiesLogin:
                self.log_in()
            else:
                try:
                    self.cookies_load()
                    time.sleep(1)
                    self.webDriver.refresh()
                    self.should_be_authorized_user()
                except (FileNotFoundError, AssertionError):
                    self.login_ensure(cookiesLogin=False)

    def log_off(self):
        profileButton = self.wait_element(*BasePageLocators.USER_PROFILE_BUTTON)
        self.move_n_click(profileButton)
        time.sleep(0.1)
        exitButton = self.wait_element(*BasePageLocators.EXIT_LOGOFF_BUTTON)
        self.move_n_click(exitButton)

    def logoff_ensure(self, retryLogoff=False):
        try:
            self.should_not_be_authorized_user()
        except (AssertionError, TimeoutException):
            self.log_off()
            if not retryLogoff:
                self.logoff_ensure(retryLogoff=True)

    def move_n_click(self, element):
        self.actChain.reset_actions()
        self.actChain.move_to_element_with_offset(element, 1, 1).pause(0.05).click()
        self.actChain.perform()

    def open(self, url=None):
        if not url:
            url = self.URL
        self.webDriver.get(url)

    def open_login_frame(self):
        loginButton = self.wait_element(*BasePageLocators.LOGIN_BUTTON_HEADER)
        self.move_n_click(loginButton)

    def promo_containers_action(self, action="close"):
        try:
            assert self.wait_element(*BasePageLocators.PROMO_CONTAINER, 1)
            if action == "close":
                targetButton = self.wait_element(*BasePageLocators.PROMO_CONTAINER_CLOSE_CROSS)
            if action == "accept":
                targetButton = self.wait_element(*BasePageLocators.PROMO_CONTAINER_ACCEPT)
            if action == "decline":
                targetButton = self.wait_element(*BasePageLocators.PROMO_CONTAINER_DECLINE)
            self.move_n_click(targetButton)
        except TimeoutException:
            pass
        try:
            assert self.wait_element(*BasePageLocators.SERVICES_PROMO_CONTAINER, 1)
            if action in ("close", "decline"):
                targetButton = self.wait_element(*BasePageLocators.SERVICES_PROMO_CONTAINER_CLOSE_CROSS)
            if action == "accept":
                targetButton = self.wait_element(*BasePageLocators.SERVICES_PROMO_CONTAINER_ACCEPT)
            self.move_n_click(targetButton)
        except TimeoutException:
            pass

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
