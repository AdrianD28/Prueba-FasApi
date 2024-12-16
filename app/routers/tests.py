from fastapi import APIRouter, HTTPException
from app.database import event_collection
import logging

router = APIRouter()
logger = logging.getLogger(__name__)



async def load_events_from_db():
    events = []
    async for event in event_collection.find():  
        events.append(event)
    return events
events_storage = []
stories_storage = []

def group_events_into_stories(events):
    stories = []
    # Example grouping logic: Group by session_id or other relevant pattern
    grouped_by_session = {}
    for event in events:
        session_id = event.properties["session_id"]
        if session_id not in grouped_by_session:
            grouped_by_session[session_id] = []
        grouped_by_session[session_id].append(event)
    
    # Convert grouped events into user stories
    for session, events in grouped_by_session.items():
        stories.append({"session_id": session, "events": events})
    
    return stories

def generate_playwright_test(story):
    # Inicialización del script de Playwright
    test_script = f"from playwright.sync_api import sync_playwright\n\n"
    
    # Inicio de la función de prueba
    test_script += f"def test_generated_{story['session_id']}():\n"
    
    # Abriendo Playwright y el navegador
    test_script += f"    with sync_playwright() as p:\n"
    test_script += f"        browser = p.chromium.launch()\n"
    test_script += f"        page = browser.new_page()\n"
    
    # Generación de acciones para cada evento
    for event in story["events"]:
        if event['event'] == "$click":  # Si el evento es un click
            test_script += f"        page.click('{event['properties']['elementText']}')  # Click on {event['properties']['elementText']}\n"
        elif event['event'] == "$input":  # Si el evento es un input
            # Verificar si 'value' existe en las propiedades antes de acceder a ella
            value = event['properties'].get('value', '')
            test_script += f"        page.fill('{event['properties']['elementText']}', '{value}')  # Fill input with {value}\n"
        # Agregar más eventos si es necesario

    # Cierre del navegador
    test_script += f"        browser.close()\n"
    
    return test_script



def group_events_into_stories(events):
    stories = {}
    
    for event in events:
        session_id = event["properties"]["session_id"]
        
        if session_id not in stories:
            stories[session_id] = {
                "_id": session_id,
                "session_id": session_id,
                "events": []
            }
        
        stories[session_id]["events"].append(event)
    
    return list(stories.values())  # Devuelve una lista de historias

@router.get("/")
async def generate_tests(story_id: str = None):
    global stories_storage
    global events_storage
    
    # Cargar eventos desde la base de datos si no están ya cargados
    if not events_storage:
        events_storage = await load_events_from_db()
    
    print(f"Events storage: {events_storage}")  # Log para verificar los eventos cargados
    
    if not stories_storage:
        stories_storage = group_events_into_stories(events_storage)
    
    print(f"Stories in storage: {stories_storage}")  # Log para verificar las historias
    
    if story_id:
        # Buscar en base al session_id, no al _id
        story = next((story for story in stories_storage if story["session_id"] == story_id), None)
        
        if not story:
            raise HTTPException(status_code=404, detail="Story not found")
        
        test_script = generate_playwright_test(story)
        return {"test_script": test_script}
    
    tests = []
    for story in stories_storage:
        tests.append({"session_id": story["session_id"], "test_script": generate_playwright_test(story)})
    
    return tests
