from typing import Dict, List, Any
from collections import defaultdict
from pymongo.errors import PyMongoError
from pydantic import BaseModel, ValidationError
from app.database import event_collection 

class EventProperties(BaseModel):
    distinct_id: str
    session_id: str
    journey_id: str
    current_url: str
    host: str
    pathname: str
    browser: str
    device: str
    referrer: str
    referring_domain: str
    screen_height: int
    screen_width: int
    eventType: str
    elementType: str
    elementText: str
    elementAttributes: Dict[str, Any]
    timestamp: str
    x: int
    y: int
    mouseButton: int
    ctrlKey: bool
    shiftKey: bool
    altKey: bool
    metaKey: bool

async def add_event(event_data: Dict) -> None:
    try:
        # Validar el evento
        event = EventProperties(**event_data['properties'])
        await event_collection.insert_one(event_data)
    except ValidationError as e:
        print(f"Error de validación: {e}")
    except PyMongoError as e:
        print(f"Error al agregar evento: {e}")

async def retrieve_events(limit: int = 100, skip: int = 0) -> List[Dict]:
    events = []
    async for event in event_collection.find().skip(skip).limit(limit):
        events.append(event)
    return events

async def get_user_stories(session_id: str = None) -> List[Dict]:
    events = await retrieve_events()
    user_stories = []
    
    # Agrupar eventos por session_id o journey_id
    grouped_events = defaultdict(list)
    for event in events:
        key = event['properties']['session_id'] if session_id is None else session_id
        grouped_events[key].append(event)

    # Crear historias de usuario a partir de los eventos agrupados
    for key, events in grouped_events.items():
        user_stories.append({
            "session_id": key,
            "events": events
        })
    
    return user_stories