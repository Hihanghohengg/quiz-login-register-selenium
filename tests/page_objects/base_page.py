from __future__ import annotations

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    """Operasi umum untuk seluruh page object."""

    def __init__(self, driver: WebDriver, base_url: str, timeout: int = 10) -> None:
        self.driver = driver
        self.base_url = base_url.rstrip("/")
        self.wait = WebDriverWait(driver, timeout)

    def open_path(self, path: str) -> None:
        self.driver.get(f"{self.base_url}/{path.lstrip('/')}")

    @property
    def current_url(self) -> str:
        return self.driver.current_url
