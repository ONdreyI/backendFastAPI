from src.schemas.facilities import FacilitiesAdd


async def test_facilities_crud(db):
    # Create facilities
    # facilities_data = FacilitiesAdd(title="WiFi")
    facilities_data = [
        {"title": "WiFi"},
        {"title": "Air conditioning"},
    ]
    facilities = [
        FacilitiesAdd.model_validate(facility) for facility in facilities_data
    ]
    await db.facilities.add_bulk(facilities)
    await db.commit()


async def test_get_facilities(ac):
    response = await ac.get(
        "/facilities",
    )
    print(f"{response.json()=}")
    assert response.status_code == 200
