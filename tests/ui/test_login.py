import allure
import pytest
from playwright.sync_api import expect

from data.test_data import SAUCE_PASSWORD, Errors, SauceUsers

pytestmark = [pytest.mark.ui, allure.feature("Login")]


@pytest.mark.smoke
@allure.title("Standard user can log in")
def test_successful_login(login_page, page):
    login_page.login(SauceUsers.STANDARD)
    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")


@allure.title("Locked-out user sees an error")
def test_locked_out_user(login_page):
    login_page.login(SauceUsers.LOCKED_OUT)
    expect(login_page.error).to_have_text(Errors.LOCKED_OUT)


@allure.title("Invalid credentials are rejected: {username!r} / {password!r}")
@pytest.mark.parametrize(
    "username, password, error",
    [
        (SauceUsers.STANDARD, "wrong_password", Errors.WRONG_CREDENTIALS),
        ("unknown_user", SAUCE_PASSWORD, Errors.WRONG_CREDENTIALS),
        ("", SAUCE_PASSWORD, Errors.USERNAME_REQUIRED),
        (SauceUsers.STANDARD, "", Errors.PASSWORD_REQUIRED),
        ("' OR 1=1 --", SAUCE_PASSWORD, Errors.WRONG_CREDENTIALS),  # injection attempt
    ],
)
def test_invalid_login(login_page, username, password, error):
    login_page.login(username, password)
    expect(login_page.error).to_have_text(error)


@allure.title("Protected page is not accessible without login")
def test_direct_access_requires_login(page):
    page.goto("/inventory.html")
    expect(page.locator('[data-test="error"]')).to_contain_text("You can only access")
