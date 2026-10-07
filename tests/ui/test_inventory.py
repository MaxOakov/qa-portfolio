import allure
import pytest
from playwright.sync_api import expect

pytestmark = [pytest.mark.ui, allure.feature("Products & Cart")]

BACKPACK = "Sauce Labs Backpack"
BIKE_LIGHT = "Sauce Labs Bike Light"


@allure.title("Catalog shows 6 products")
def test_catalog_has_products(inventory):
    expect(inventory.items).to_have_count(6)


@allure.title("Sort by price: {option}")
@pytest.mark.parametrize("option, reverse", [("lohi", False), ("hilo", True)])
def test_sort_by_price(inventory, option, reverse):
    inventory.sort_by(option)
    prices = inventory.prices()
    assert prices == sorted(prices, reverse=reverse)


@allure.title("Sort by name: Z to A")
def test_sort_by_name_desc(inventory):
    inventory.sort_by("za")
    names = inventory.names()
    assert names == sorted(names, reverse=True)


@pytest.mark.smoke
@allure.title("Cart badge updates when adding and removing items")
def test_cart_badge(inventory):
    inventory.add_to_cart(BACKPACK)
    inventory.add_to_cart(BIKE_LIGHT)
    expect(inventory.cart_badge).to_have_text("2")

    inventory.remove_from_cart(BACKPACK)
    expect(inventory.cart_badge).to_have_text("1")

    inventory.remove_from_cart(BIKE_LIGHT)
    expect(inventory.cart_badge).to_be_hidden()


@allure.title("Cart persists after page reload")
def test_cart_persists_after_reload(inventory, page):
    inventory.add_to_cart(BACKPACK)
    page.reload()
    expect(inventory.cart_badge).to_have_text("1")
