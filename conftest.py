from selenium import webdriver
from selenium.webdriver.chrome.options import Options as chromeOptions
from selenium.webdriver.firefox.options import Options as firefoxOptions
import time
import pytest


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
        webDriver = webdriver.Chrome(options=options)
        webDriver.implicitly_wait(1)

    elif browserName == "firefox":
        options = firefoxOptions()
        options.set_preference("intl.accept_languages", userLanguage)
        webDriver = webdriver.Firefox(options=options)
        webDriver.implicitly_wait(2)

    webDriver.maximize_window()

    yield webDriver
    time.sleep(1)
    print("\nTests are ending")
    webDriver.quit()


@pytest.fixture(scope="function")
def webDriver(request):
    yield next(init_web_driver(request))
    next(init_web_driver(request))


@pytest.fixture(scope="class")
def webDriver_(request):
    yield next(init_web_driver(request))
    next(init_web_driver(request))



