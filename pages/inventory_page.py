import allure

from pages.base_page import BasePage


class InventoryPage(BasePage):
    path = "/inventory.html"

    @property
    def items(self):
        return self.page.locator(".inventory_item")

    @property
    def item_names(self):
        return self.page.locator(".inventory_item_name")

    @property
    def item_prices(self):
        return self.page.locator(".inventory_item_price")

    @property
    def cart_badge(self):
        return self.page.locator(".shopping_cart_badge")

    @property
    def sort_dropdown(self):
        return self.by_test_id("product-sort-container")

    @staticmethod
    def _slug(product_name: str) -> str:
        return product_name.lower().replace(" ", "-")

    @allure.step("Add '{product_name}' to cart")
    def add_to_cart(self, product_name: str):
        self.by_test_id(f"add-to-cart-{self._slug(product_name)}").click()

    @allure.step("Remove '{product_name}' from cart")
    def remove_from_cart(self, product_name: str):
        self.by_test_id(f"remove-{self._slug(product_name)}").click()

    @allure.step("Sort products by '{option}'")
    def sort_by(self, option: str):
        """option: az | za | lohi | hilo"""
        self.sort_dropdown.select_option(option)

    def prices(self) -> list[float]:
        return [float(p.replace("$", "")) for p in self.item_prices.all_inner_texts()]

    def names(self) -> list[str]:
        return self.item_names.all_inner_texts()

    @allure.step("Open cart")
    def open_cart(self):
        self.page.locator(".shopping_cart_link").click()
