from selenium import webdriver
from selenium.webdriver.chrome.options import Options as chromeOptions
from selenium.webdriver.firefox.options import Options as firefoxOptions
import sys
import os
import time
import datetime
import pytest
try:  # win / linux cases
    import winreg
except ModuleNotFoundError:
    import subprocess

testsResults = []
timeStamp = ""
WD = webdriver


def pytest_configure():
    global timeStamp, testsResults
    timeStamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')


def pytest_sessionstart(session):
    session.results = dict()


@pytest.hookimpl(tryfirst=False, hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    result = outcome.get_result()
    if result.when == 'call':
        item.session.results[item] = result


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    global testsResults
    outcome = yield
    result = outcome.get_result()
    if result.outcome == "failed":
        exception = call.excinfo.value
        exception_class = call.excinfo.type
        exception_class_name = call.excinfo.typename
        exception_type_and_message_formatted = call.excinfo.exconly()
        exception_traceback = call.excinfo.traceback
        testsResults.append([item, exception, exception_class, exception_class_name,
                             exception_type_and_message_formatted, exception_traceback])


def pytest_sessionfinish(session):
    pass


def pytest_unconfigure():
    try:
        os.rename("./tmp/logs/report.html",
                  fr"./tmp/logs/report_{timeStamp}.html")
    except FileNotFoundError:
        print("No report file to rename")
    global testsResults
    with open("tmp/logs/tests_error_log.log", "a") as logFile:
        for result in testsResults:
            logFile.write(f"\n\n<<<{timeStamp}>>>\n{result[0]}\n{result[4]}")
            for traceBack in result[5]:
                logFile.write(f"\n{traceBack}")


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
        webDriver.implicitly_wait(1)

    webDriver.maximize_window()
    yield webDriver

    time.sleep(1)
    webDriver.quit()
    print("\nBrowser quit")
    yield


@pytest.fixture(scope="function", autouse=False)
def webDriver(request):
    init_call = init_web_driver(request)
    yield next(init_call)
    next(init_call)


@pytest.fixture(scope="class", autouse=False)
def webDriver_(request):
    init_call = init_web_driver(request)
    yield next(init_call)
    next(init_call)
