
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
        page.open(page.mainURL)
        page.log_in(saveAuth=True)
        page.cookies_save(writeCookies=True)
        page = InboxPage(webDriver_)
        page.open(InboxPage.URL)
        page.promo_containers_action("close")
        yield page
        webDriver_.delete_all_cookies()
        page.actChain.reset_actions()

    def test_unread_emails_quantity_is_equal_to_counter_in_header(self, webDriver_, page):
        page.login_ensure()
        page.open(InboxPage.URL)
        page.should_be_inbox_page()
        page.check_document_state(3)
        page.unread_emails_should_be_equal_to_counter()

    def test_unread_emails_quantity_is_equal_to_counter_in_left_sidebar(self, webDriver_, page):
        page.login_ensure()
        page.open(InboxPage.URL)
        page.should_be_inbox_page()
        page.check_document_state(3)
        counterSidebar = page.wait_element(*InboxPageLocators.UNREAD_EMAIL_COUNTER_SIDEBAR)
        counterValue = int(counterSidebar.text)
        page.unread_emails_should_be_equal_to_counter(counterValue)


@pytest.mark.new
@pytest.mark.usefixtures("webDriver_")
class TestOpenCloseEmails():

    @pytest.fixture(scope="class", autouse=True)
    def page(self, webDriver_):
        page = BasePage(webDriver_)
        page.open(page.mainURL)
        page.login_ensure()
        page = InboxPage(webDriver_)
        page.open(InboxPage.URL)
        page.promo_containers_action("close")
        yield page
        webDriver_.delete_all_cookies()
        page.actChain.reset_actions()

    def test_can_open_first_email(self, webDriver_, page):
        page.login_ensure()
        page.open(InboxPage.URL)
        page.should_be_inbox_page()
        emailLink = page.wait_element(*InboxPageLocators.LINK_EMAIL_ORDINARY)
        emailSubject = page.wait_element(*InboxPageLocators.EMAIL_SUBJECT_BRIEF).text
        page.move_n_click(emailLink)
        time.sleep(1)
        page.should_be_opened_email()
        emailHeader = page.wait_element(*InboxPageLocators.OPENED_EMAIL_SUBJECT_H2).text
        assert emailSubject == emailHeader, \
            f"Email subject in description is '{emailSubject}', but email header is '{emailHeader}'"

    def test_can_close_email_with_escape_key(self, webDriver_, page):
        page.should_be_opened_email()
        page.actChain.key_down(page.keyTable.ESCAPE).pause(0.1).key_up(page.keyTable.ESCAPE).perform()
        assert page.is_element_disappeared(*InboxPageLocators.OPENED_EMAIL_SUBJECT_H2, 1), \
            "There is email topic in header, probably email is still open"

    def test_can_open_second_email(self, webDriver_, page):
        page.login_ensure()
        page.open(InboxPage.URL)
        page.should_be_inbox_page()
        emailLink = page.wait_elements(*InboxPageLocators.LINK_EMAIL_ORDINARY)[1]
        emailSubject = page.wait_elements(*InboxPageLocators.EMAIL_SUBJECT_BRIEF)[1].text
        page.move_n_click(emailLink)
        time.sleep(1)
        page.should_be_opened_email()
        emailHeader = page.wait_element(*InboxPageLocators.OPENED_EMAIL_SUBJECT_H2).text
        assert emailSubject == emailHeader, \
            f"Email subject in description is '{emailSubject}', but email header is '{emailHeader}'"

    def test_close_email_with_back_button(self, webDriver_, page):
        page.should_be_opened_email()
        backButton = page.wait_element(*InboxPageLocators.OPENED_EMAIL_BACK_BUTTON)
        page.move_n_click(backButton)
        assert page.is_element_disappeared(*InboxPageLocators.OPENED_EMAIL_SUBJECT_H2, 1), \
            "There is email topic in header, probably email is still open"

