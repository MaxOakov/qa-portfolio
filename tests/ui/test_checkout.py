import allure
import pytest
from playwright.sync_api import expect

from data.test_data import Customer, Errors
from pages.checkout_page import CartPage, CheckoutPage

pytestmark = [pytest.mark.ui, allure.feature("Checkout")]


@pytest.mark.smoke
@allure.title("End-to-end: buy two products")
def test_full_checkout(inventory, page):
    inventory.add_to_cart("Sauce Labs Backpack")      # $29.99
    inventory.add_to_cart("Sauce Labs Bike Light")    # $9.99
    inventory.open_cart()

    cart = CartPage(page)
    expect(cart.cart_items).to_have_count(2)
    cart.checkout()

    checkout = CheckoutPage(page)
    checkout.fill_customer(Customer.random())
    checkout.continue_()
    expect(checkout.item_total).to_have_text("Item total: $39.98")

    checkout.finish()
    expect(checkout.complete_header).to_have_text("Thank you for your order!")


@allure.title("Checkout requires first name")
def test_checkout_requires_first_name(inventory, page):
    inventory.add_to_cart("Sauce Labs Backpack")
    inventory.open_cart()
    CartPage(page).checkout()

    checkout = CheckoutPage(page)
    customer = Customer.random()
    customer.first_name = ""
    checkout.fill_customer(customer)
    checkout.continue_()
    expect(checkout.error).to_have_text(Errors.FIRST_NAME_REQUIRED)
