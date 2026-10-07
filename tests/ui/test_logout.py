import allure
import pytest
from playwright.sync_api import expect

from pages.login_page import LoginPage

pytestmark = [pytest.mark.ui, allure.feature("Login")]


@allure.title("User is redirected to login page after logout")
def test_logout(inventory, page):
    inventory.logout()

    login_page = LoginPage(page)
    expect(page).to_have_url("https://www.saucedemo.com/")
    expect(login_page.login_button).to_be_visible()

    page.goto("/inventory.html")
    expect(login_page.error).to_contain_text("You can only access")