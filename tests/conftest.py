import pytest
from httpx import AsyncClient, ASGITransport
from src.config import settings
from src.database import Base, engine_null_pool
from src.main import app
from src.models import *
from tests.data_for_tests import data_iterator
from tests.data_for_tests_1 import data_iterator_1


@pytest.fixture(scope="session", autouse=True)
async def async_main():
    print("Я ФИКСТУРА")
    assert settings.MODE == "TEST"
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


# @pytest.fixture(scope="session", autouse=True)
# async def test_root():
#     async with AsyncClient(
#         transport=ASGITransport(app=app),
#         base_url="http://test",
#     ) as ac:
#         await ac.post(
#             "/auth/register",
#             json={
#                 "email": "kot@pes.com",
#                 "password": "1234",
#             },
#         )


@pytest.fixture(scope="session", autouse=True)
async def test_root():
    base_url = "http://test"

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url=base_url,
    ) as ac:
        for data in data_iterator():
            endpoint = data["endpoint"]
            json_data = data["json_data"]

            # Отправка POST-запроса с данными по выбранному адресу
            await ac.post(
                endpoint,
                json=json_data,
            )


# @pytest.fixture(scope="session", autouse=True)
# async def test_root():
#     async with AsyncClient(
#         transport=ASGITransport(app=app),
#         base_url="http://test",
#     ) as ac:
#         await ac.post(
#             "/hotels",
#             json=[
#                 {
#                     "title": "Cosmos Collection Altay Resort",
#                     "location": "Республика Алтай, Майминский район, село Урлу-Аспак, Лесхозная улица, 20",
#                 },
#                 {
#                     "title": "Skala",
#                     "location": "Республика Алтай, Майминский район, поселок Барангол, Чуйская улица 40а",
#                 },
#                 {
#                     "title": "Bridge Resort",
#                     "location": "посёлок городского типа Сириус, Фигурная улица, 45",
#                 },
#             ],
#         )
