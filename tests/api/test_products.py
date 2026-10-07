import allure
import pytest

from data.test_data import fake

pytestmark = [pytest.mark.api, allure.feature("API: Products")]

PRODUCT_FIELDS = {"id": int, "title": str, "price": (int, float), "category": str, "stock": int}


def assert_product_schema(product: dict):
    for field, expected_type in PRODUCT_FIELDS.items():
        assert field in product, f"missing field: {field}"
        assert isinstance(product[field], expected_type), f"{field} has wrong type"


@pytest.mark.smoke
@allure.title("Product list respects limit and has a valid schema")
def test_products_list(api):
    resp = api.products(limit=10)
    assert resp.status == 200
    body = resp.json()
    assert body["limit"] == 10
    assert len(body["products"]) == 10
    for product in body["products"]:
        assert_product_schema(product)


@allure.title("Pagination: pages do not overlap")
def test_pagination(api):
    page1 = {p["id"] for p in api.products(limit=5, skip=0).json()["products"]}
    page2 = {p["id"] for p in api.products(limit=5, skip=5).json()["products"]}
    assert page1.isdisjoint(page2)


@allure.title("Get single product by id")
def test_get_product(api):
    resp = api.product(1)
    assert resp.status == 200
    assert_product_schema(resp.json())
    assert resp.json()["id"] == 1


@allure.title("Non-existent product returns 404: id={product_id}")
@pytest.mark.parametrize("product_id", [0, 99999])
def test_product_not_found(api, product_id):
    resp = api.product(product_id)
    assert resp.status == 404
    assert "not found" in resp.json()["message"]


@allure.title("Search returns only relevant products")
def test_search(api):
    resp = api.search("phone")
    assert resp.status == 200
    products = resp.json()["products"]
    assert products, "search returned nothing"
    for p in products:
        text = f'{p["title"]} {p.get("description", "")} {p.get("category", "")}'.lower()
        assert "phone" in text


@allure.title("Create product returns the sent data with a new id")
def test_add_product(api):
    payload = {"title": f"QA {fake.word()}", "price": 19.99, "category": "testing"}
    resp = api.add_product(payload)
    assert resp.status == 201
    body = resp.json()
    assert body["id"]
    for key, value in payload.items():
        assert body[key] == value
