from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import inspect, text

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

def ensure_rawg_slug_column() -> None:
    inspector = inspect(engine)
    if "video_games" not in inspector.get_table_names():
        return
    columns = {column["name"] for column in inspector.get_columns("video_games")}
    if "rawg_slug" in columns:
        return
    with engine.begin() as connection:
        connection.execute(text("ALTER TABLE video_games ADD COLUMN rawg_slug VARCHAR"))

ensure_rawg_slug_column()

def ensure_rawg_platforms_column() -> None:
    inspector = inspect(engine)
    if "video_games" not in inspector.get_table_names():
        return
    columns = {column["name"] for column in inspector.get_columns("video_games")}
    if "rawg_platforms" in columns:
        return
    with engine.begin() as connection:
        connection.execute(text("ALTER TABLE video_games ADD COLUMN rawg_platforms VARCHAR"))

ensure_rawg_platforms_column()

def ensure_metadata_columns() -> None:
    inspector = inspect(engine)
    if "video_games" not in inspector.get_table_names():
        return
    columns = {column["name"] for column in inspector.get_columns("video_games")}
    statements = []
    if "notes" not in columns:
        statements.append("ALTER TABLE video_games ADD COLUMN notes VARCHAR")
    if "tags" not in columns:
        statements.append("ALTER TABLE video_games ADD COLUMN tags VARCHAR")
    if "progress" not in columns:
        statements.append("ALTER TABLE video_games ADD COLUMN progress FLOAT")
    if "favorite" not in columns:
        statements.append("ALTER TABLE video_games ADD COLUMN favorite BOOLEAN")
    if "added_at" not in columns:
        statements.append("ALTER TABLE video_games ADD COLUMN added_at VARCHAR")
    if "last_updated" not in columns:
        statements.append("ALTER TABLE video_games ADD COLUMN last_updated VARCHAR")
    if not statements:
        return
    with engine.begin() as connection:
        for statement in statements:
            connection.execute(text(statement))

ensure_metadata_columns()

app.include_router(router)
