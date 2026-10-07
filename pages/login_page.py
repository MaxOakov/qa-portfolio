import allure

from data.test_data import SAUCE_PASSWORD
from pages.base_page import BasePage


class LoginPage(BasePage):
    path = "/"

    @property
    def username(self):
        return self.by_test_id("username")

    @property
    def password(self):
        return self.by_test_id("password")

    @property
    def login_button(self):
        return self.by_test_id("login-button")

    @property
    def error(self):
        return self.by_test_id("error")

    @allure.step("Log in as '{username}'")
    def login(self, username: str, password: str = SAUCE_PASSWORD):
        self.username.fill(username)
        self.password.fill(password)
        self.login_button.click()
