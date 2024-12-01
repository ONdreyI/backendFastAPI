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
    # Register user
    res_register = await ac.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
        },
    )
    assert res_register.status_code == status_code

    # Login user
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
    else:
        return

        # /me
        resp_me = await ac.get("/auth/me")
        assert resp_me.status_code == 200
        user = resp_me.json()
        assert user["email"] == email
        assert "id" in user
        assert "password" not in user
        assert "hashed_password" not in user

    # Logout user
    res_logout = await ac.post(
        "/auth/logout",
        headers={"Authorization": f"Bearer {res_login.json()['access_token']}"},
    )
    assert res_logout.status_code == 200
    assert "access_token" not in ac.cookies
