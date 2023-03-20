
import time
import pytest

from .pages.base_page import BasePage, BasePageLocators, LoginFrameLocators
from .pages.inbox_page import InboxPage, InboxPageLocators


@pytest.mark.new
@pytest.mark.usefixtures("webDriver_")
class TestCompareEmailsWithCounters():

    @pytest.fixture(scope="class", autouse=True)
    def page(self, webDriver_):
        page = BasePage(webDriver_)
        page.open(InboxPage.URL)
        page.log_in(saveAuth=True)
        page = InboxPage(webDriver_)
        page.cookies_save(writeCookies=True)
        page.promo_containers_action("close")
        yield page
        webDriver_.delete_all_cookies()
        page.actChain.reset_actions()

    def test_unread_emails_quantity_is_equal_to_counter_in_header(self, webDriver_, page):
        page.login_ensure()
        page.open(InboxPage.URL)
        page.should_be_inbox_page()
        page.unread_emails_should_be_equal_to_counter()


@pytest.mark.new
@pytest.mark.usefixtures("webDriver_")
class TestOpenCloseEmails():

    @pytest.fixture(scope="class", autouse=True)
    def page(self, webDriver_):
        page = BasePage(webDriver_)
        page.open(InboxPage.URL)
        page.login_ensure()
        page = InboxPage(webDriver_)
        page.promo_containers_action("close")
        yield page
        webDriver_.delete_all_cookies()
        page.actChain.reset_actions()

    def test_open_first_email(self, webDriver_, page):
        page.login_ensure()
        page.open(InboxPage.URL)
        page.should_be_inbox_page()
        emailLink = page.wait_element(*InboxPageLocators.LINK_EMAIL_ORDINARY)
        emailSubject = page.wait_element(*InboxPageLocators.EMAIL_SUBJECT_BRIEF).text
        page.move_n_click(emailLink)
        assert page.is_element_present(*InboxPageLocators.EMAIL_SUBJECT_H2), \
            "There is no email topic in header, probably email is not opened"
        emailHeader = page.wait_element(*InboxPageLocators.EMAIL_SUBJECT_H2).text
        assert emailSubject == emailHeader, \
            f"Email subject in description is '{emailSubject}' but email header is '{emailHeader}'"

