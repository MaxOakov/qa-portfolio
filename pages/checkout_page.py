import allure

from data.test_data import Customer
from pages.base_page import BasePage


class CartPage(BasePage):
    path = "/cart.html"

    @property
    def cart_items(self):
        return self.page.locator(".cart_item")

    @allure.step("Proceed to checkout")
    def checkout(self):
        self.by_test_id("checkout").click()


class CheckoutPage(BasePage):
    @property
    def error(self):
        return self.by_test_id("error")

    @property
    def complete_header(self):
        return self.by_test_id("complete-header")

    @property
    def item_total(self):
        return self.page.locator(".summary_subtotal_label")

    @allure.step("Fill customer info")
    def fill_customer(self, customer: Customer):
        self.by_test_id("firstName").fill(customer.first_name)
        self.by_test_id("lastName").fill(customer.last_name)
        self.by_test_id("postalCode").fill(customer.postal_code)

    @allure.step("Continue to overview")
    def continue_(self):
        self.by_test_id("continue").click()

    @allure.step("Finish order")
    def finish(self):
        self.by_test_id("finish").click()
