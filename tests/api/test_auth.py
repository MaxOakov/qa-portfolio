import allure
import pytest

from data.test_data import ApiUsers

pytestmark = [pytest.mark.api, allure.feature("API: Auth")]


@pytest.mark.smoke
@allure.title("Login returns a token that grants access to /auth/me")
def test_login_and_get_profile(api):
    resp = api.login(**ApiUsers.VALID)
    assert resp.status == 200
    body = resp.json()
    assert body["username"] == ApiUsers.VALID["username"]
    assert body["accessToken"]

    me = api.me(body["accessToken"])
    assert me.status == 200
    assert me.json()["id"] == body["id"]


@allure.title("Invalid credentials return 400")
def test_login_invalid_password(api):
    resp = api.login(ApiUsers.VALID["username"], "wrong-password")
    assert resp.status == 400
    assert resp.json()["message"] == "Invalid credentials"


@allure.title("/auth/me without a valid token is rejected")
def test_me_with_invalid_token(api):
    resp = api.me("not-a-real-token")
    assert resp.status == 401
    assert resp.json()["message"] == "Invalid/Expired Token!"
