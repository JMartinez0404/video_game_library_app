from sqlalchemy import desc
from sqlalchemy.orm import Session

from domain.entities import ActivityEntry
from domain.repositories import ActivityRepository
from infrastructure.databases.models import ActivityModel


class SQLAlchemyActivityRepository(ActivityRepository):

    def __init__(self, db: Session):
        self.db = db

    def add(self, entry: ActivityEntry) -> ActivityEntry:
        db_entry = ActivityModel(
            game_id=entry.game_id,
            title=entry.title,
            type=entry.type,
            details=entry.details,
            timestamp=entry.timestamp,
        )
        self.db.add(db_entry)
        self.db.commit()
        self.db.refresh(db_entry)

        return ActivityEntry(
            id=db_entry.id,
            game_id=db_entry.game_id,
            title=db_entry.title,
            type=db_entry.type,
            details=db_entry.details,
            timestamp=db_entry.timestamp,
        )

    def list(self, limit: int = 10) -> list[ActivityEntry]:
        entries = (
            self.db.query(ActivityModel)
            .order_by(desc(ActivityModel.timestamp))
            .limit(limit)
            .all()
        )
        return [
            ActivityEntry(
                id=entry.id,
                game_id=entry.game_id,
                title=entry.title,
                type=entry.type,
                details=entry.details,
                timestamp=entry.timestamp,
            )
            for entry in entries
        ]

    def list_imports(self, limit: int = 10) -> list[ActivityEntry]:
        entries = (
            self.db.query(ActivityModel)
            .filter(ActivityModel.type == "import")
            .order_by(desc(ActivityModel.timestamp))
            .limit(limit)
            .all()
        )
        return [
            ActivityEntry(
                id=entry.id,
                game_id=entry.game_id,
                title=entry.title,
                type=entry.type,
                details=entry.details,
                timestamp=entry.timestamp,
            )
            for entry in entries
        ]
