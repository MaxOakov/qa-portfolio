# QA Automation Portfolio (Playwright + Python)

![Tests](https://github.com/MaxOakov/qa-portfolio/actions/workflows/tests.yml/badge.svg)

UI and API tests for two public demo apps: [saucedemo.com](https://www.saucedemo.com) for the UI and [dummyjson.com](https://dummyjson.com) for the API.

Allure report: https://maxoakov.github.io/qa-portfolio/

## What's tested

**UI (saucedemo.com)**
- Login: valid user, locked-out user, wrong/empty credentials, an SQL-injection string, opening a protected page without logging in
- Products: sorting by price and by name, adding and removing items, cart staying filled after a reload
- Checkout: full purchase with a check of the item total, required first name

**API (dummyjson.com)**
- Auth: login returns a token that works for `/auth/me`, wrong password, invalid token
- Products: response fields and types, pagination, 404 for missing ids, search, creating a product

## Tools

- Playwright for Python, for both the browser tests and the API requests
- pytest with fixtures, parametrize and markers (`ui`, `api`, `smoke`)
- Page Object Model
- Faker for checkout form data
- Allure for reports, with a screenshot attached when a UI test fails
- GitHub Actions: runs on every push and every Monday (in case the demo sites change), 4 workers with pytest-xdist

## Structure

```
pages/        page objects: login, inventory, cart + checkout (checkout_page.py)
api/          small client for the dummyjson endpoints
data/         users, expected error messages, Faker customer
tests/ui/     UI tests
tests/api/    API tests
conftest.py   fixtures and the screenshot-on-failure hook
```

## Running locally

Create and activate a virtual environment.

Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS / Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install and run:

```bash
pip install -r requirements.txt
playwright install chromium

pytest                  # everything
pytest -m smoke         # smoke tests only
pytest -m api           # API tests only
pytest -m ui --headed   # UI tests with the browser visible
pytest -n 4             # run in parallel

allure serve allure-results   # needs the Allure CLI
```
