"""Test data: fixed accounts from the demo apps + generated data via Faker."""
from dataclasses import dataclass

from faker import Faker

fake = Faker()

UI_BASE_URL = "https://www.saucedemo.com"
API_BASE_URL = "https://dummyjson.com"

SAUCE_PASSWORD = "secret_sauce"


class SauceUsers:
    STANDARD = "standard_user"
    LOCKED_OUT = "locked_out_user"


class ApiUsers:
    VALID = {"username": "emilys", "password": "emilyspass"}


class Errors:
    LOCKED_OUT = "Epic sadface: Sorry, this user has been locked out."
    WRONG_CREDENTIALS = "Epic sadface: Username and password do not match any user in this service"
    USERNAME_REQUIRED = "Epic sadface: Username is required"
    PASSWORD_REQUIRED = "Epic sadface: Password is required"
    FIRST_NAME_REQUIRED = "Error: First Name is required"


@dataclass
class Customer:
    first_name: str
    last_name: str
    postal_code: str

    @classmethod
    def random(cls) -> "Customer":
        return cls(fake.first_name(), fake.last_name(), fake.postcode())
