"""Thin wrapper over Playwright's APIRequestContext for dummyjson.com."""
import allure
from playwright.sync_api import APIRequestContext, APIResponse


class DummyJsonClient:
    def __init__(self, request: APIRequestContext):
        self.request = request

    @allure.step("POST /auth/login")
    def login(self, username: str, password: str) -> APIResponse:
        return self.request.post("/auth/login", data={"username": username, "password": password})

    @allure.step("GET /auth/me")
    def me(self, token: str) -> APIResponse:
        return self.request.get("/auth/me", headers={"Authorization": f"Bearer {token}"})

    @allure.step("GET /products")
    def products(self, limit: int = 30, skip: int = 0) -> APIResponse:
        return self.request.get("/products", params={"limit": limit, "skip": skip})

    @allure.step("GET /products/{product_id}")
    def product(self, product_id: int) -> APIResponse:
        return self.request.get(f"/products/{product_id}")

    @allure.step("GET /products/search?q={query}")
    def search(self, query: str) -> APIResponse:
        return self.request.get("/products/search", params={"q": query})

    @allure.step("POST /products/add")
    def add_product(self, payload: dict) -> APIResponse:
        return self.request.post("/products/add", data=payload)
