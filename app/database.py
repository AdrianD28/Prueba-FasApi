from motor.motor_asyncio import AsyncIOMotorClient
import os

# Configura la URL de conexión a MongoDB
MONGO_DETAILS = os.getenv("MONGOLOCAL")

client = AsyncIOMotorClient(MONGO_DETAILS)
database = client["bugster"]
event_collection = database.get_collection("events")