import allure
import pytest
from playwright.sync_api import Playwright

from api.client import DummyJsonClient
from data.test_data import API_BASE_URL, UI_BASE_URL, SauceUsers
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


# UI fixtures
@pytest.fixture(scope="session")
def base_url():
    return UI_BASE_URL


@pytest.fixture
def login_page(page) -> LoginPage:
    return LoginPage(page).open()


@pytest.fixture
def inventory(login_page) -> InventoryPage:
    """Logged-in standard user on the products page."""
    login_page.login(SauceUsers.STANDARD)
    return InventoryPage(login_page.page)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Attach a screenshot to the Allure report when a UI test fails."""
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page:
            allure.attach(page.screenshot(full_page=True), name="screenshot",
                          attachment_type=allure.attachment_type.PNG)


# API fixtures
@pytest.fixture(scope="session")
def api_request(playwright: Playwright):
    ctx = playwright.request.new_context(base_url=API_BASE_URL)
    yield ctx
    ctx.dispose()


@pytest.fixture(scope="session")
def api(api_request) -> DummyJsonClient:
    return DummyJsonClient(api_request)
