
import os
import time
import pytest

from pages.base_page import BasePage, BasePageLocators
from pages.main_page import MainPage, MainPageLocators


@pytest.mark.usefixtures("driver")
class TestMainPageLoginLogout():

    def test_can_see_login_link(self, driver):
        page = MainPage(driver)
        page.open(MainPage.url)
        page.should_not_be_authorized_user()