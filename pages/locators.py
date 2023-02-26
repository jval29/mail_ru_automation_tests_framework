from selenium.webdriver.common.by import By


class BasePageLocators():
    USER_PROFILE_BUTTON = (By.CSS_SELECTOR, "div[data-testid='whiteline-account']")
    EXIT_LOGOFF_BUTTON = (By.CSS_SELECTOR, "div[data-testid='whiteline-account-exit']")
    LOGIN_FRAME = (By.CSS_SELECTOR, "iframe[src^='https://account.mail.ru/login/']")
    LOGIN_BUTTON_MAIN = (By.CSS_SELECTOR, "button[data-testid='enter-mail-primary']")
    LOGIN_BUTTON_HEADER = (By.CSS_SELECTOR, "div#ph-whiteline button.ph-login")
    LINK_HOME_HEADER = (By.CSS_SELECTOR, "div#ph-whiteline>div:first-child>div:first-child>a:first-child")


class LoginFrameLocators():
    LOGIN_FIELD = (By.CSS_SELECTOR, "div#root form[method='POST'] input[name='username']")
    PWD_FIELD = (By.CSS_SELECTOR, "input[name='password']")
    DOMAIN_SELECTOR = (By.CSS_SELECTOR, "div[data-test-id='domain-select']")
    DOMAIN_POINTS = (By.CSS_SELECTOR, f"div[id^='react-select-2-option']")
    SAVE_AUTH_CHECKBOX = (By.CSS_SELECTOR, "div.login-row div.submit-right-block>div.save-auth-field-wrap")
    NEXT_BUTTON = (By.CSS_SELECTOR, "button[data-test-id='next-button']")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[data-test-id='submit-button']")
    CLOSE_BUTTON_CROSS = (By.CSS_SELECTOR, "div[data-test-id='cross'] svg")


class MainPageLocators():
    pass
