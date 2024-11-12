from src.schemas.facilities import FacilitiesAdd


# async def test_facilities_crud(db):
#     # Create facilities
#     # facilities_data = FacilitiesAdd(title="WiFi")
#     facilities_data = [
#         {"title": "WiFi"},
#         {"title": "Air conditioning"},
#     ]
#     facilities = [
#         FacilitiesAdd.model_validate(facility) for facility in facilities_data
#     ]
#     await db.facilities.add_bulk(facilities)
#     await db.commit()

# # Get facilities
# facilities_response = await db.facilities.get_all()
#
# # Assert facilities
# assert len(facilities_response) == len(facilities)
# for facility in facilities_response:
#     assert facility in facilities
#
# # Update facilities
# updated_facilities_data = [
#     {"id": facility.id, "summary": "Updated WiFi", "value": {"title": "Updated WiFi"}},
#     {"id": facility.id, "summary": "Updated Air conditioning", "value": {"title": "Updated Air conditioning"}},
# ]
