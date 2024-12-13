from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import List, Dict, Any
from app.services import add_event, retrieve_events

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
    screen_height: int = Field(..., alias="$screen_height")
    screen_width: int = Field(..., alias="$screen_width")
    event_type: str = Field(..., alias="eventType")
    element_type: str = Field(..., alias="elementType")
    element_text: str = Field(..., alias="elementText")
    element_attributes: Dict[str, Any] = Field(..., alias="elementAttributes")
    timestamp: str
    x: int
    y: int
    mouse_button: int = Field(..., alias="mouseButton")
    ctrl_key: bool = Field(..., alias="ctrlKey")
    shift_key: bool = Field(..., alias="shiftKey")
    alt_key: bool = Field(..., alias="altKey")
    meta_key: bool = Field(..., alias="metaKey")

class Event(BaseModel):
    event: str
    properties: EventProperties
    timestamp: str

@router.post("/")
async def receive_events(events: List[Event]):
    for event in events:
        event_data = event.dict(by_alias=True)
        await add_event(event_data)
    return {"message": "Eventos recibidos y almacenados"}

@router.get("/")
async def get_events():
    return await retrieve_events()