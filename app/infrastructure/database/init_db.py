from app.infrastructure.database import mongo_connection
from app.infrastructure.database.models import all_models
from beanie import init_beanie

async def init_db():
    db = mongo_connection.connect()
    await init_beanie(database=db, document_models=all_models)
