from selenium.webdriver.common.by import By


class BasePageLocators():
    USER_PROFILE_BUTTON = (By.CSS_SELECTOR, "div[data-testid='whiteline-account']")
    LOGIN_FRAME = (By.CSS_SELECTOR, "iframe[src^='https://account.mail.ru/login/']")
    LOGIN_BUTTON_MAIN = (By.CSS_SELECTOR, "button[data-testid='enter-mail-primary']")
    LOGIN_BUTTON_HEADER = (By.CSS_SELECTOR, "div#ph-whiteline button.ph-login")


class LoginFrameLocators():
    LOGIN_FIELD = (By.CSS_SELECTOR, "div#root form[method='POST'] input[name='username']")


class MainPageLocators():
    pass
