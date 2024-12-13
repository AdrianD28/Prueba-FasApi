from motor.motor_asyncio import AsyncIOMotorClient

# Configura la URL de conexión a MongoDB
MONGO_DETAILS = "mongodb://localhost:27017"

client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.bugster
event_collection = database.get_collection("events")