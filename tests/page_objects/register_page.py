from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from .base_page import BasePage


class RegisterPage(BasePage):
    NAME = (By.ID, "name")
    EMAIL = (By.ID, "InputEmail")
    USERNAME = (By.ID, "username")
    PASSWORD = (By.ID, "InputPassword")
    REPASSWORD = (By.ID, "InputRePassword")
    SUBMIT = (By.CSS_SELECTOR, "button[name='submit']")
    ALERT = (By.CSS_SELECTOR, ".alert.alert-danger")
    VALIDATION = (By.CSS_SELECTOR, "p.text-danger")
    LOGIN_LINK = (By.LINK_TEXT, "Login")
    TITLE = (By.CSS_SELECTOR, "h4")

    def open(self) -> "RegisterPage":
        self.open_path("register.php")
        self.wait.until(EC.visibility_of_element_located(self.TITLE))
        return self

    def register(self, name: str, email: str, username: str, password: str, repassword: str) -> None:
        values = {
            self.NAME: name,
            self.EMAIL: email,
            self.USERNAME: username,
            self.PASSWORD: password,
            self.REPASSWORD: repassword,
        }
        for locator, value in values.items():
            element = self.driver.find_element(*locator)
            element.clear()
            element.send_keys(value)
        self.driver.find_element(*self.SUBMIT).click()

    def alert_text(self) -> str:
        return self.wait.until(EC.visibility_of_element_located(self.ALERT)).text

    def validation_texts(self) -> list[str]:
        return [element.text for element in self.driver.find_elements(*self.VALIDATION)]

    def click_login(self) -> None:
        self.driver.find_element(*self.LOGIN_LINK).click()
