from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from .base_page import BasePage


class LoginPage(BasePage):
    USERNAME = (By.ID, "username")
    PASSWORD = (By.ID, "InputPassword")
    SUBMIT = (By.CSS_SELECTOR, "button[name='submit']")
    ALERT = (By.CSS_SELECTOR, ".alert.alert-danger")
    REGISTER_LINK = (By.LINK_TEXT, "Register")
    TITLE = (By.CSS_SELECTOR, "h4")

    def open(self) -> "LoginPage":
        self.open_path("login.php")
        self.wait.until(EC.visibility_of_element_located(self.TITLE))
        return self

    def login(self, username: str, password: str) -> None:
        self.driver.find_element(*self.USERNAME).clear()
        self.driver.find_element(*self.USERNAME).send_keys(username)
        self.driver.find_element(*self.PASSWORD).clear()
        self.driver.find_element(*self.PASSWORD).send_keys(password)
        self.driver.find_element(*self.SUBMIT).click()

    def alert_text(self) -> str:
        return self.wait.until(EC.visibility_of_element_located(self.ALERT)).text

    def click_register(self) -> None:
        self.driver.find_element(*self.REGISTER_LINK).click()
