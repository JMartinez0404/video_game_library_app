from fastapi import FastAPI

from infrastructure.databases.models import Base
from infrastructure.databases.sessions import engine
from presentation.routes import router


app = FastAPI(title="Video Game Library API")

# Create tables automatically (for development only)
Base.metadata.create_all(bind=engine)

app.include_router(router)
