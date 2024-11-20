import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("lol@gmail.com", "no2ta", 200),
        ("pets@gmail.com", "bb03g", 200),
        ("slot@gmail.com", "11111111", 200),
        (66666666, "test", 422),
        ("test1@gmail.com", "test1", 200),
        ("test2@gmail.com", 23232, 422),
        ("test3@gmail.com", "test3", 200),
        ("test4@gmail.com", "test4", 200),
    ],
)
async def test_auth(
    email: str,
    password: str,
    status_code: int,
    ac: AsyncClient,
):
    res_register = await ac.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
        },
    )
    assert res_register.status_code == status_code

    res_login = await ac.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )
    assert res_login.status_code == status_code
    if res_login.status_code == 200:
        assert res_login.json()["access_token"]

        res_me = await ac.get(
            "/auth/me",
            headers={"Authorization": f"Bearer {res_login.json()['access_token']}"},
        )
        assert res_me.status_code == 200
        # print(res_me.json()["user"]["email"])
        assert res_me.json()["user"]["email"] == email
        assert ac.cookies["access_token"]

        res_logout = await ac.post(
            "/auth/logout",
            headers={"Authorization": f"Bearer {res_login.json()['access_token']}"},
        )
        assert res_logout.status_code == 200
        assert "access_token" not in ac.cookies
