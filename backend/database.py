import os
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

# Setup DB path
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
os.makedirs(DATA_DIR, exist_ok=True)
DB_PATH = os.path.join(DATA_DIR, "pdr.db")

engine = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class ConversationLog(Base):
    __tablename__ = "conversation_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    user_message = Column(Text, nullable=False)
    ai_response = Column(Text, nullable=False)

class DocumentMetadata(Base):
    __tablename__ = "document_metadata"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    file_type = Column(String)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    summary = Column(Text, nullable=True)

# Create tables
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
