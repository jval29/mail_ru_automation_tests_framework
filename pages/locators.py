from selenium.webdriver.common.by import By


class BasePageLocators():
    USER_PROFILE_BUTTON = (By.CSS_SELECTOR, "div[data-testid='whiteline-account']")
    EXIT_LOGOFF_BUTTON = (By.CSS_SELECTOR, "div[data-testid='whiteline-account-exit']")
    LOGIN_FRAME = (By.CSS_SELECTOR, "iframe[src^='https://account.mail.ru/login/']")
    LOGIN_BUTTON_MAIN = (By.CSS_SELECTOR, "button[data-testid='enter-mail-primary']")
    LOGIN_BUTTON_HEADER = (By.CSS_SELECTOR, "div#ph-whiteline button.ph-login")
    LINK_HOME_HEADER = (By.CSS_SELECTOR, "div#ph-whiteline>div:first-child>div:first-child>a:first-child")
    LINK_INBOX_HEADER = (By.CSS_SELECTOR, "div#ph-whiteline>div:first-child>div:first-child>a:nth-child(2)")
    LINK_CLOUD_HEADER = (By.CSS_SELECTOR, "div#ph-whiteline>div:first-child>div:first-child>a:nth-child(3)")
    COOKIE_ACCEPT_BUTTON = (By.CSS_SELECTOR, "span#cmpbntyestxt")
    COOKIE_DECLINE_BUTTON = (By.CSS_SELECTOR, "span#cmpbntnotxt")
    PROMO_CONTAINER = (By.CSS_SELECTOR, "*[data-test-id^='promo']")
    PROMO_CONTAINER_CLOSE_CROSS = (By.CSS_SELECTOR, "*[data-test-id^='promo'] *[data-test-id='cross']>svg")
    PROMO_CONTAINER_ACCEPT = (By.CSS_SELECTOR, "*[data-test-id^='promo'] *[data-test-id='submit']")
    PROMO_CONTAINER_DECLINE = (By.CSS_SELECTOR, "*[data-test-id^='promo'] *[data-test-id='cancel']")
    SERVICES_PROMO_CONTAINER = (By.CSS_SELECTOR, "div[class*='promo-container']")
    SERVICES_PROMO_CONTAINER_CLOSE_CROSS = (By.CSS_SELECTOR, "div[class*='promo-container'] div[class*='promo-close-icon'] svg")
    SERVICES_PROMO_CONTAINER_ACCEPT = (By.CSS_SELECTOR, "div[class*='promo-container'] button[class*='promo-button']")
    UNREAD_EMAIL_COUNTER_HEADER = (By.CSS_SELECTOR, "div#ph-whiteline a:nth-child(2)  span.ph-notify")


class LoginFrameLocators():
    LOGIN_FIELD = (By.CSS_SELECTOR, "div#root form[method='POST'] input[name='username']")
    PWD_FIELD = (By.CSS_SELECTOR, "input[name='password']")
    DOMAIN_SELECTOR = (By.CSS_SELECTOR, "div[data-test-id='domain-select']")
    DOMAIN_POINTS = (By.CSS_SELECTOR, f"div[id^='react-select-2-option']")
    SAVE_AUTH_CHECKBOX = (By.CSS_SELECTOR, "div.login-row div.submit-right-block>div.save-auth-field-wrap")
    NEXT_BUTTON = (By.CSS_SELECTOR, "button[data-test-id='next-button']")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[data-test-id='submit-button']")
    CLOSE_BUTTON_CROSS = (By.CSS_SELECTOR, "div[data-test-id='cross'] svg")


class LoginPageLocators():
    LOGIN_FORM = (By.CSS_SELECTOR, "div[data-test-id='login-app-ready']")


class MainPageLocators():
    pass


class InboxPageLocators():
    UNREAD_EMAIL_MARK = (By.CSS_SELECTOR, "a span.ll-rs_is-active")
    LINK_EMAIL_ORDINARY = (By.CSS_SELECTOR, "div#app-canvas div.letter-list a.llc")
    EMAIL_SUBJECT_BRIEF = (By.CSS_SELECTOR, "div#app-canvas div.letter-list a.llc span.llc__subject div span")
    UNREAD_EMAIL_COUNTER_SIDEBAR = (By.CSS_SELECTOR, "div#sideBarContent a[data-folder-link-id='0'] span.badge__text")

    OPENED_EMAIL_SUBJECT_H2 = (By.CSS_SELECTOR, "div.thread__header h2")
    OPENED_EMAIL_BACK_BUTTON = (By.CSS_SELECTOR, "div.portal-menu-logo div.portal-menu-element_back")

