from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from infrastructure.databases.models import Base
from infrastructure.databases.sessions import engine
from presentation.routes import router


origins = [
    "http://localhost:3000",  # Next.js dev server
]

app = FastAPI(title="Video Game Library API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables automatically (for development only)
Base.metadata.create_all(bind=engine)

app.include_router(router)
