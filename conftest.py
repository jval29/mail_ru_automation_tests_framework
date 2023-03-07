from selenium import webdriver
from selenium.webdriver.chrome.options import Options as chromeOptions
from selenium.webdriver.firefox.options import Options as firefoxOptions
import time
import pytest
try:  # win / linux cases
    import winreg
except ModuleNotFoundError:
    import subprocess


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="choose browser name")
    parser.addoption("--language", action="store", default="ru", help="choose the language: en / ru / de ....etc")
    parser.addoption("--headless", action="store", default="off", help="turn on / off browser UI")


def init_web_driver(request):
    browserName = request.config.getoption("browser").lower().strip()
    userLanguage = request.config.getoption("language").lower().strip()
    headlessOption = request.config.getoption("headless").lower().strip()

    if browserName == "chrome" or browserName != "firefox":
        options = chromeOptions()
        options.add_experimental_option("prefs", {"intl.accept_languages": userLanguage})
        options.add_argument("--start-maximized")
        if headlessOption == "on":
            options.add_argument("--headless")
        try:  # search for chrome.exe path in Windows registry
            reg_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe"
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path) as key:
                chrome_path = winreg.QueryValue(key, None)
        except NameError:  # linux case
            chrome_path = "/app/bin/chrome"
        finally:
            options.binary_location = chrome_path
        webDriver = webdriver.Chrome(options=options)
        webDriver.implicitly_wait(1)

    elif browserName == "firefox":
        options = firefoxOptions()
        options.set_preference("intl.accept_languages", userLanguage)
        try:  # search for firefox.exe path in Windows registry
            reg_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\firefox.exe"
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path) as key:
                firefox_path = winreg.QueryValue(key, None)
        except NameError:  # linux case
            firefox_path = subprocess.check_output(['which', 'firefox']).decode().strip()
        finally:
            options.binary_location = firefox_path
        webDriver = webdriver.Firefox(options=options)
        webDriver.implicitly_wait(2)

    webDriver.maximize_window()

    yield webDriver
    time.sleep(1)
    webDriver.quit()
    print("\nBrowser quit")
    yield


@pytest.fixture(scope="function")
def webDriver(request):
    init_call = init_web_driver(request)
    yield next(init_call)
    next(init_call)


@pytest.fixture(scope="class")
def webDriver_(request):
    init_call = init_web_driver(request)
    yield next(init_call)
    next(init_call)



