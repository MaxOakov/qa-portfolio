from playwright.sync_api import Page


class BasePage:
    path = "/"

    def __init__(self, page: Page):
        self.page = page

    def open(self):
        self.page.goto(self.path)
        return self

    def by_test_id(self, value: str):
        """saucedemo marks elements with data-test attributes."""
        return self.page.locator(f'[data-test="{value}"]')
