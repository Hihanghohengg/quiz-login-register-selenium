from __future__ import annotations

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from tests.page_objects.login_page import LoginPage


def test_lgn_001_page_elements_are_visible(driver, base_url):
    page = LoginPage(driver, base_url).open()
    assert driver.find_element(*page.TITLE).text.strip() == "Sign-In"
    assert driver.find_element(*page.USERNAME).is_displayed()
    assert driver.find_element(*page.PASSWORD).is_displayed()
    assert driver.find_element(*page.SUBMIT).is_enabled()


def test_lgn_002_register_link_navigation(driver, base_url):
    page = LoginPage(driver, base_url).open()
    page.click_register()
    WebDriverWait(driver, 10).until(EC.url_contains("register.php"))
    assert driver.find_element(By.CSS_SELECTOR, "h4").text.strip() == "Sign-Up"


def test_lgn_003_empty_fields_show_validation(driver, base_url):
    page = LoginPage(driver, base_url).open()
    page.login("", "")
    assert page.alert_text() == "Data tidak boleh kosong !!"


def test_lgn_004_valid_credentials_redirect_to_stub(driver, base_url):
    page = LoginPage(driver, base_url).open()
    page.login("testuser", "Password123!")
    WebDriverWait(driver, 10).until(EC.url_contains("index.php"))
    assert driver.find_element(By.ID, "stub-marker").text == "TEST_STUB_INDEX"
    assert "testuser" in driver.find_element(By.ID, "welcome").text


@pytest.mark.xfail(
    reason="Known defect: username yang tidak ditemukan menampilkan 'Register User Gagal', bukan pesan autentikasi generik.",
    strict=True,
)
def test_lgn_005_unknown_username_shows_generic_error(driver, base_url):
    page = LoginPage(driver, base_url).open()
    page.login("unknown-user", "Password123!")
    assert page.alert_text() == "Username atau password salah !!"


@pytest.mark.xfail(
    reason="Known defect: password salah untuk username valid tidak menghasilkan pesan error.",
    strict=True,
)
def test_lgn_006_wrong_password_shows_error(driver, base_url):
    page = LoginPage(driver, base_url).open()
    page.login("testuser", "WrongPassword!")
    assert page.alert_text() == "Username atau password salah !!"


def test_lgn_007_sql_injection_does_not_authenticate(driver, base_url):
    page = LoginPage(driver, base_url).open()
    page.login("' OR 1=1 -- ", "anything")
    assert "login.php" in driver.current_url
    assert "index.php" not in driver.current_url


def test_lgn_008_password_input_is_masked(driver, base_url):
    page = LoginPage(driver, base_url).open()
    assert driver.find_element(*page.PASSWORD).get_attribute("type") == "password"
