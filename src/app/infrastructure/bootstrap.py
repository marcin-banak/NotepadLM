from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    "sqlite:///notepadlm.db",
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine)

from app.infrastructure.database.models import Base

Base.metadata.create_all(engine)