from __future__ import annotations

import os
import shutil
from pathlib import Path
from typing import Generator

import pymysql
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webdriver import WebDriver

PROJECT_ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"
PASSWORD_HASH = "$2y$12$cGjrr7Yc9Kio2utnmVPp6OyMuFceCiOWQ6mTvtcwXUTKaWQbKGH0y"


def _database_connection() -> pymysql.connections.Connection:
    return pymysql.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "quiz_pengupil"),
        charset="utf8mb4",
        autocommit=True,
    )


def _find_chromedriver() -> str | None:
    explicit = os.getenv("CHROMEDRIVER_PATH")
    if explicit and Path(explicit).is_file():
        return explicit

    command = shutil.which("chromedriver")
    if command:
        return command

    runner_dir = os.getenv("CHROMEWEBDRIVER")
    if runner_dir:
        candidates = list(Path(runner_dir).rglob("chromedriver"))
        if candidates:
            return str(candidates[0])
    return None


@pytest.fixture(scope="session")
def base_url() -> str:
    return os.getenv("BASE_URL", "http://127.0.0.1:8000").rstrip("/")


@pytest.fixture(autouse=True)
def reset_database() -> Generator[None, None, None]:
    """Driver basis data: setiap testcase dimulai dari data deterministik."""
    with _database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("TRUNCATE TABLE users")
            cursor.execute(
                "INSERT INTO users (name, username, email, password) VALUES (%s, %s, %s, %s)",
                ("Test User", "testuser", "testuser@example.com", PASSWORD_HASH),
            )
    yield


@pytest.fixture
def db_connection() -> Generator[pymysql.connections.Connection, None, None]:
    connection = _database_connection()
    try:
        yield connection
    finally:
        connection.close()


@pytest.fixture
def driver(request: pytest.FixtureRequest) -> Generator[WebDriver, None, None]:
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1440,1200")
    options.add_argument("--disable-gpu")

    chrome_binary = os.getenv("CHROME_BINARY") or shutil.which("google-chrome") or shutil.which("chromium")
    if chrome_binary:
        options.binary_location = chrome_binary

    driver_path = _find_chromedriver()
    browser = webdriver.Chrome(service=Service(driver_path) if driver_path else Service(), options=options)
    browser.set_page_load_timeout(20)
    request.node._selenium_driver = browser  # type: ignore[attr-defined]
    yield browser
    browser.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo[object]):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        browser = getattr(item, "_selenium_driver", None)
        if browser is not None:
            ARTIFACTS_DIR.mkdir(exist_ok=True)
            safe_name = item.nodeid.replace("/", "_").replace("::", "__")
            browser.save_screenshot(str(ARTIFACTS_DIR / f"FAILED_{safe_name}.png"))
