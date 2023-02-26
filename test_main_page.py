import os
import time
import pytest

from .pages.base_page import BasePage, BasePageLocators, LoginFrameLocators
from .pages.main_page import MainPage, MainPageLocators


@pytest.mark.usefixtures("webDriver_")
class TestGuestCanOpenCloseLoginFrameFromMainPage():

    @pytest.fixture(scope="class", autouse=True)
    def page(self, webDriver_):
        page = MainPage(webDriver_)
        page.open(MainPage.url)
        yield page
        webDriver_.delete_all_cookies()
        page.actChain.reset_actions()

    def test_guest_can_see_login_link(self, webDriver_, page):
        page.logoff_ensure()
        assert page.is_element_present(*BasePageLocators.LOGIN_BUTTON_HEADER), \
            "Login button is not present"

    @pytest.mark.parametrize("locator", [BasePageLocators.LOGIN_BUTTON_HEADER, BasePageLocators.LOGIN_BUTTON_MAIN])
    def test_guest_can_open_login_frame_with_header_and_main_button(self, webDriver_, page, locator):
        page.logoff_ensure()
        webDriver_.refresh()
        loginButton = page.wait_element(*locator)
        page.move_n_click(loginButton)
        assert page.is_element_present(*BasePageLocators.LOGIN_FRAME), \
            "Login frame is not present"
        assert page.is_element_visible(*BasePageLocators.LOGIN_FRAME), \
            "Login frame is not visible"

    def test_guest_can_close_login_frame_with_close_button_cross(self, webDriver_, page):
        webDriver_.refresh()
        page.logoff_ensure()
        page.open_login_frame()
        loginFrame = page.wait_element(*BasePageLocators.LOGIN_FRAME)
        webDriver_.switch_to.frame(loginFrame)
        closeButton = page.wait_element(*LoginFrameLocators.CLOSE_BUTTON_CROSS)
        page.move_n_click(closeButton)
        time.sleep(1)
        assert not page.is_element_visible(*BasePageLocators.LOGIN_FRAME), \
            "Login frame is still visible"
        webDriver_.switch_to.default_content()

    def test_guest_can_close_login_frame_with_escape_button(self, webDriver_, page):
        webDriver_.refresh()
        page.logoff_ensure()
        page.open_login_frame()
        page.actChain.key_down(page.keyTable.ESCAPE).pause(0.1).key_up(page.keyTable.ESCAPE).perform()
        time.sleep(1)
        assert not page.is_element_visible(*BasePageLocators.LOGIN_FRAME), \
            "Login frame is still visible"

    @pytest.mark.new
    def test_guest_can_close_login_frame_with_click_out_of_frame(self, webDriver_, page):
        webDriver_.refresh()
        page.logoff_ensure()
        page.open_login_frame()
        loginFrame = page.wait_element(*BasePageLocators.LOGIN_FRAME)
        webDriver_.switch_to.frame(loginFrame)
        page.wait_element(*LoginFrameLocators.CLOSE_BUTTON_CROSS, 10)
        webDriver_.switch_to.default_content()
        outOfFrameElement = page.wait_element(*BasePageLocators.LINK_HOME_HEADER)
        page.move_n_click(outOfFrameElement)
        time.sleep(1)
        assert not page.is_element_visible(*BasePageLocators.LOGIN_FRAME), \
            "Login frame is still visible"


@pytest.mark.usefixtures("webDriver_")
class TestLoginLogoff():

    def test_guest_can_log_in(self, webDriver_):
        page = MainPage(webDriver_)
        page.open(MainPage.url)
        page.logoff_ensure()
        page.log_in()
        page.should_be_authorized_user()

    def test_user_can_log_off(self, webDriver_):
        page = MainPage(webDriver_)
        page.open(MainPage.url)
        page.login_ensure()
        page.log_off()
        page.should_not_be_authorized_user()


@pytest.mark.usefixtures("webDriver_")
class TestLoginVariants():

    @pytest.fixture(scope="class", autouse=True)
    def page(self, webDriver_):
        page = MainPage(webDriver_)
        page.open(MainPage.url)
        yield page
        webDriver_.delete_all_cookies()
        page.actChain.reset_actions()

    def test_login_with_domain_typing(self, webDriver_, page):
        page.logoff_ensure()
        page.log_in(loginOption="valid", selectDomain=False)
        page.should_be_authorized_user()


@pytest.mark.new
@pytest.mark.usefixtures("webDriver")
class TestCheckboxSaveAuth():

    sessionID = None
    cookies = None

    def test_login_with_option_save_auth_checkbox_false(self, webDriver):
        page = MainPage(webDriver)
        page.open(MainPage.url)
        page.logoff_ensure()
        page.log_in(loginOption="valid", saveAuth=False)
        page.should_be_authorized_user()
        page.cookies_save()

    @pytest.mark.xfail(reason="At the moment, the site retains authorization even if you do not tick the checkbox")
    def test_auth_not_saved(self, webDriver):
        page = MainPage(webDriver)
        page.open(MainPage.url)
        page.cookies_load()
        time.sleep(1)
        webDriver.refresh()
        page.should_not_be_authorized_user()

    def test_login_with_option_save_auth_checkbox_true(self, webDriver):
        page = MainPage(webDriver)
        page.open(MainPage.url)
        page.logoff_ensure()
        page.log_in(loginOption="valid", saveAuth=True)
        page.should_be_authorized_user()
        page.cookies_save()

    def test_auth_is_saved(self, webDriver):
        page = MainPage(webDriver)
        page.open(MainPage.url)
        page.cookies_load()
        time.sleep(1)
        webDriver.refresh()
        page.should_be_authorized_user()


