# Bugster API

## Descripción
Esta API captura eventos de interacción de usuario en aplicaciones web y los transforma en pruebas E2E.

## Instalación

1. Clona el repositorio.
2. Crea un entorno virtual:
   ```bash
   python -m venv venv
   ```
3. Activa el entorno virtual:
   - En Windows:
     ```bash
     venv\Scripts\activate
     ```
   - En macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
4. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Ejecución

Para ejecutar la aplicación, usa el siguiente comando:
bash
uvicorn app.main:app --reload