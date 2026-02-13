from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from config import get_config

config = get_config()

# Create database engine
engine = create_engine(
    config.DATABASE_URL,
    connect_args={'check_same_thread': False} if 'sqlite' in config.DATABASE_URL else {},
    echo=config.DEBUG
)

# Create session factory
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

# Base class for models
Base = declarative_base()

def init_db():
    """Initialize database - create all tables"""
    import models.user
    import models.companion
    import models.conversation
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully!")

def get_db():
    """Get database session"""
    db = Session()
    try:
        yield db
    finally:
        db.close()
