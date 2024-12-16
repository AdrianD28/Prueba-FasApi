from typing import Dict, List, Any
from collections import defaultdict
from pymongo.errors import PyMongoError
from pydantic import BaseModel, ValidationError
from bson import ObjectId
from app.database import event_collection
import re
from playwright.sync_api import sync_playwright

# Modelo para validar las propiedades del evento
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


# Constantes para tipos de eventos
EVENT_CLICK = "$click"
EVENT_INPUT = "$input"
EVENT_NAVIGATE = "$navigate"

import re
from playwright.sync_api import sync_playwright, Page, expect

def generate_tests(story_id: str) -> str:
    # Recuperar los eventos de la historia (esto lo obtienes de tu base de datos o cualquier fuente)
    # Aquí estamos simulando los eventos de la historia de usuario
    events = [
        {"event": "$click", "properties": {"elementText": "Get started"}},
        {"event": "$input", "properties": {"elementText": "email", "value": "test@example.com"}}
    ]
    
    # Generar el código de test basado en los eventos
    test_code = f"""
def test_user_story_{story_id}(page: Page):
    page.goto("https://playwright.dev/")
    """
    
    for event in events:
        if event['event'] == "$click":
            element_text = event['properties']['elementText']
            test_code += f"""
    page.get_by_role("link", name="{element_text}").click()
            """
        elif event['event'] == "$input":
            element_text = event['properties']['elementText']
            value = event['properties']['value']
            test_code += f"""
    page.fill('text={element_text}', '{value}')
            """

    test_code += """
    # Aserciones adicionales
    expect(page).to_have_title(re.compile("Playwright"))
    """
    
    return test_code

def test_generated_code_sync(story_id: str) -> str:
    # Generar el código de prueba
    test_code = generate_tests(story_id)

    # Usar Playwright en modo sincrónico
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Ejecutar el código generado (de forma sincrónica)
        exec(test_code)  # Ejecuta el código generado dinámicamente
        
        # Aserción adicional
        assert page.title() == "Playwright"
        
        browser.close()

    return "Test executed successfully"

# Agregar un evento a la base de datos
async def add_event(event_data: Dict) -> None:
    try:
        # Validar el evento
        event = EventProperties(**event_data['properties'])
        await event_collection.insert_one(event_data)
    except ValidationError as e:
        # Registrar errores de validación
        print(f"Error de validación: {e}")
    except PyMongoError as e:
        # Registrar errores de base de datos
        print(f"Error al agregar evento: {e}")


# Recuperar eventos de la base de datos
async def retrieve_events(limit: int = 100, skip: int = 0) -> List[Dict]:
    events = []
    async for event in event_collection.find().skip(skip).limit(limit):
        events.append(event)
    return events

def convert_objectid_to_str(data):
    """Convierte ObjectId a string en un diccionario o lista."""
    if isinstance(data, list):
        return [convert_objectid_to_str(item) for item in data]
    elif isinstance(data, dict):
        return {key: convert_objectid_to_str(value) for key, value in data.items()}
    elif isinstance(data, ObjectId):
        return str(data)
    return data

# Obtener historias de usuario basadas en eventos
async def get_user_stories(session_id: str = None) -> List[Dict]:
    events = await retrieve_events()  # Supongo que esto devuelve eventos con datos MongoDB
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
            "events": convert_objectid_to_str(events),
            "_id": str(events[0]['_id']) if events else None  # Convertir ObjectId a string
        })
    
    return user_stories
