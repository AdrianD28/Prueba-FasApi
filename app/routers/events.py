# app/routers/events.py
from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import List, Dict, Any
from app.services import add_event

router = APIRouter()

class EventProperties(BaseModel):
    distinct_id: str
    session_id: str
    journey_id: str
    current_url: str = Field(..., alias="$current_url")
    host: str = Field(..., alias="$host")
    pathname: str = Field(..., alias="$pathname")
    browser: str = Field(..., alias="$browser")
    device: str = Field(..., alias="$device")
    referrer: str = Field(..., alias="$referrer")
    referring_domain: str = Field(..., alias="$referring_domain")
    screen_height: int = Field(..., alias="$screen_height")
    screen_width: int = Field(..., alias="$screen_width")
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

class Event(BaseModel):
    event: str
    properties: EventProperties
    timestamp: str

class EventsRequest(BaseModel):
    events: List[Event]


@router.post("/")
async def receive_events(request: EventsRequest):
    for event in request.events:
        event_data = event.dict(by_alias=True)
        try:
            await add_event(event_data)  
        except Exception as e:
            return {"message": "Error al guardar el evento", "error": str(e)}
    return {"message": "Eventos recibidos y almacenados en la base de datos"}