from app.database import event_collection

async def add_event(event_data: dict) -> dict:
    event = await event_collection.insert_one(event_data)
    new_event = await event_collection.find_one({"_id": event.inserted_id})
    return new_event

async def retrieve_events():
    events = []
    async for event in event_collection.find():
        events.append(event)
    return events