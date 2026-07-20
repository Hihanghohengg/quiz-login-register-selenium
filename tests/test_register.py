from __future__ import annotations

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from tests.page_objects.register_page import RegisterPage


def test_reg_001_page_elements_are_visible(driver, base_url):
    page = RegisterPage(driver, base_url).open()
    assert driver.find_element(*page.TITLE).text.strip() == "Sign-Up"
    for locator in (page.NAME, page.EMAIL, page.USERNAME, page.PASSWORD, page.REPASSWORD, page.SUBMIT):
        assert driver.find_element(*locator).is_displayed()


def test_reg_002_login_link_navigation(driver, base_url):
    page = RegisterPage(driver, base_url).open()
    page.click_login()
    WebDriverWait(driver, 10).until(EC.url_contains("login.php"))
    assert driver.find_element(By.CSS_SELECTOR, "h4").text.strip() == "Sign-In"


def test_reg_003_empty_fields_show_validation(driver, base_url):
    page = RegisterPage(driver, base_url).open()
    page.register("", "", "", "", "")
    assert page.alert_text() == "Data tidak boleh kosong !!"


def test_reg_004_password_mismatch_is_rejected(driver, base_url):
    page = RegisterPage(driver, base_url).open()
    page.register("Budi", "budi@example.com", "budi", "Password123!", "Different123!")
    assert page.validation_texts() == ["Password tidak sama !!", "Password tidak sama !!"]
    assert "register.php" in driver.current_url


@pytest.mark.xfail(
    reason="Known defect: INSERT memakai variabel $nama yang tidak didefinisikan sehingga nama tersimpan kosong.",
    strict=True,
)
def test_reg_005_valid_registration_persists_all_fields(driver, base_url, db_connection):
    page = RegisterPage(driver, base_url).open()
    page.register("Budi Santoso", "budi@example.com", "budi", "Password123!", "Password123!")
    WebDriverWait(driver, 10).until(EC.url_contains("index.php"))

    with db_connection.cursor() as cursor:
        cursor.execute("SELECT name, username, email FROM users WHERE username=%s", ("budi",))
        record = cursor.fetchone()
    assert record == ("Budi Santoso", "budi", "budi@example.com")


@pytest.mark.xfail(
    reason="Known defect: pengecekan duplikasi memakai field nama, bukan username; skema juga tidak memiliki UNIQUE(username).",
    strict=True,
)
def test_reg_006_duplicate_username_is_rejected(driver, base_url, db_connection):
    page = RegisterPage(driver, base_url).open()
    page.register("Nama Berbeda", "other@example.com", "testuser", "Password123!", "Password123!")
    assert page.alert_text() == "Username sudah terdaftar !!"

    with db_connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM users WHERE username=%s", ("testuser",))
        count = cursor.fetchone()[0]
    assert count == 1


def test_reg_007_invalid_email_is_blocked_by_browser(driver, base_url):
    page = RegisterPage(driver, base_url).open()
    page.register("Budi", "bukan-email", "budi", "Password123!", "Password123!")
    email = driver.find_element(*page.EMAIL)
    assert "register.php" in driver.current_url
    assert email.get_attribute("validationMessage")


def test_reg_008_password_fields_are_masked(driver, base_url):
    page = RegisterPage(driver, base_url).open()
    assert driver.find_element(*page.PASSWORD).get_attribute("type") == "password"
    assert driver.find_element(*page.REPASSWORD).get_attribute("type") == "password"


def test_reg_009_whitespace_only_is_rejected(driver, base_url):
    page = RegisterPage(driver, base_url).open()
    page.register("   ", "   ", "   ", "   ", "   ")
    assert page.alert_text() == "Data tidak boleh kosong !!"
