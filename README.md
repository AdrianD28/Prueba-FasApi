## Uso

La API de Bugster permite capturar y gestionar eventos de interacción de usuario. A continuación se detallan los endpoints disponibles y ejemplos de cómo utilizarlos.

### Endpoints

#### 1. Obtener todos los eventos

- **Método**: `GET`
- **URL**: `/api/stories`
- **Descripción**: Recupera una lista de todos los eventos registrados.

**Ejemplo de solicitud**:
```bash
curl -X GET http://localhost:8000/api/stories
```

**Ejemplo de respuesta**:
```json
 {
        "session_id": "fcc95c16-28ae-4bc5-bead-cf052ab87cef",
        "events": [
            {
                "_id": "67603fae4b1c8aae709ea26b",
                "event": "$click",
                "properties": {
                    "distinct_id": "56676925-6e55-4072-98db-ca544bd3dbb5",
                    "session_id": "fcc95c16-28ae-4bc5-bead-cf052ab87cef",
                    "journey_id": "98eb984a-542f-4064-8e48-73ee04632a03",
                    "current_url": "https://www.bugster.app/dashboard",
                    "host": "www.bugster.app",
                    "pathname": "/dashboard",
                    "browser": "Chrome",
                    "device": "Desktop",
                    "referrer": "https://www.bugster.app/testCases?testCaseId=",
                    "referring_domain": "www.bugster.app",
                    "screen_height": 1117,
                    "screen_width": 1728,
                    "eventType": "click",
                    "elementType": "div",
                    "elementText": "71.43% Pass Rate 21 Tests",
                    "elementAttributes": {
                        "class": "flex items-center justify-between"
                    },
                    "timestamp": "2024-10-10T22:53:05.563Z",
                    "x": 539,
                    "y": 445,
                    "mouseButton": 0,
                    "ctrlKey": false,
                    "shiftKey": false,
                    "altKey": false,
                    "metaKey": false
                },
                "timestamp": "2024-10-10T22:53:05.563Z"
            },
            {
                "_id": "676042480a7d8e7d93c383d8",
                "event": "$input",
                "properties": {
                    "distinct_id": "56676925-6e55-4072-98db-ca544bd3dbb5",
                    "session_id": "fcc95c16-28ae-4bc5-bead-cf052ab87cef",
                    "journey_id": "98eb984a-542f-4064-8e48-73ee04632a03",
                    "current_url": "https://www.bugster.app/login",
                    "host": "www.bugster.app",
                    "pathname": "/login",
                    "browser": "Chrome",
                    "device": "Desktop",
                    "referrer": "https://www.bugster.app/dashboard",
                    "referring_domain": "www.bugster.app",
                    "screen_height": 1117,
                    "screen_width": 1728,
                    "eventType": "input",
                    "elementType": "input",
                    "elementText": "Username",
                    "elementAttributes": {
                        "class": "input-field"
                    },
                    "timestamp": "2024-10-10T22:53:10.563Z",
                    "x": 300,
                    "y": 200,
                    "mouseButton": 0,
                    "ctrlKey": false,
                    "shiftKey": false,
                    "altKey": false,
                    "metaKey": false
                },
                "timestamp": "2024-10-10T22:53:10.563Z"
            }
```

#### 2. Registrar un nuevo evento

- **Método**: `POST`
- **URL**: `/api/events`
- **Descripción**: Registra un nuevo evento de interacción.

**Cuerpo de la solicitud**:
```json
{
   {
    "events": [
        {
            "event": "$input",
            "properties": {
                "distinct_id": "56676925-6e55-4072-98db-ca544bd3dbb5",
                "session_id": "fcc95c16-28ae-4bc5-bead-cf052ab87cef",
                "journey_id": "98eb984a-542f-4064-8e48-73ee04632a03",
                "current_url": "https://www.bugster.app/login",
                "host": "www.bugster.app",
                "pathname": "/login",
                "browser": "Chrome",
                "device": "Desktop",
                "referrer": "https://www.bugster.app/dashboard",
                "referring_domain": "www.bugster.app",
                "screen_height": 1117,
                "screen_width": 1728,
                "eventType": "input",
                "elementType": "input",
                "elementText": "Username",
                "elementAttributes": {
                    "class": "input-field"
                },
                "timestamp": "2024-10-10T22:53:10.563Z",
                "x": 300,
                "y": 200,
                "mouseButton": 0,
                "ctrlKey": false,
                "shiftKey": false,
                "altKey": false,
                "metaKey": false
            },
            "timestamp": "2024-10-10T22:53:10.563Z"
        }
    ]
}
}
```

**Ejemplo de solicitud**:
```bash
curl -X POST http://localhost:8000/api/events -H "Content-Type: application/json" -d '{
    "tipo": "clic",
    "elemento": "botón",
    "timestamp": "2023-10-01T12:00:00Z"
}'
```

**Ejemplo de respuesta**:
```json

{
    "message": "Eventos recibidos y almacenados en la base de datos"
}

```


#### 3. Test

- **Método**: `GET`
- **URL**: `/api/test/?story_id="session_id"`
- **Descripción**: Realiza un test.

**Ejemplo de solicitud**:
```bash
curl -X GET http://localhost:8000/api/v1/tests/?story_id
```

**Ejemplo de respuesta**:
```json
{
    "test_script": "from playwright.sync_api import sync_playwright\n\ndef test_generated_fcc95c16-28ae-4bc5-bead-cf052ab87cef():\n    with sync_playwright() as p:\n        browser = p.chromium.launch()\n        page = browser.new_page()\n        page.click('71.43% Pass Rate 21 Tests')  # Click on 71.43% Pass Rate 21 Tests\n        page.fill('Username', '')  # Fill input with \n        page.fill('Username', '')  # Fill input with \n        browser.close()\n"
}
```

### Notas

- Asegúrate de que la API esté en ejecución antes de realizar las solicitudes.
- Puedes utilizar herramientas como Postman o Insomnia para probar los endpoints de manera más interactiva.
