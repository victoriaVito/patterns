from sqlalchemy import create_engine, Column, Integer, String, LargeBinary, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from config import settings

# Create engine
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Database Models
class LevelRawData(Base):
    """Stores raw JSON separately to avoid bloat"""
    __tablename__ = "level_raw_data"
    
    id = Column(Integer, primary_key=True, index=True)
    level_id = Column(Integer, unique=True, index=True)
    raw_json = Column(LargeBinary)  # Store JSON as binary
    created_at = Column(DateTime, default=datetime.utcnow)


class Level(Base):
    """Stores Candy Crush level metadata"""
    __tablename__ = "levels"
    
    id = Column(Integer, primary_key=True, index=True)
    level_id = Column(Integer, unique=True, index=True)
    level_name = Column(String)
    episode = Column(Integer)
    passes_completed = Column(String, default="0")  # "0,1,2,3,4" format - which passes done
    total_passes = Column(Integer, default=0)  # How many passes completed
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class LevelAnalysis(Base):
    """Stores analysis results for each pass"""
    __tablename__ = "level_analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    level_id = Column(Integer, ForeignKey("levels.id"), index=True)
    pass_number = Column(Integer)  # Which pass (1-5)
    patterns_found = Column(Text)  # Patterns detected in this pass (as JSON string)
    analysis_data = Column(Text)  # Full analysis data (as JSON string)
    created_at = Column(DateTime, default=datetime.utcnow)


class Pattern(Base):
    """Stores pattern definitions"""
    __tablename__ = "patterns"
    
    id = Column(Integer, primary_key=True, index=True)
    pattern_name = Column(String, unique=True, index=True)
    pass_number = Column(Integer)  # Which pass detects it
    category = Column(String)  # blockers, gameplay, gravity, spawners, etc.
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


class PatternInstance(Base):
    """Maps patterns to levels"""
    __tablename__ = "pattern_instances"
    
    id = Column(Integer, primary_key=True, index=True)
    pattern_id = Column(Integer, ForeignKey("patterns.id"), index=True)
    level_id = Column(Integer, ForeignKey("levels.id"), index=True)
    value = Column(Text)  # Value or metadata for this instance (as JSON string)
    created_at = Column(DateTime, default=datetime.utcnow)


class GlobalStatistics(Base):
    """Global analysis statistics"""
    __tablename__ = "global_statistics"
    
    id = Column(Integer, primary_key=True)
    total_levels_analyzed = Column(Integer, default=0)
    current_pass = Column(Integer, default=1)
    total_patterns_found = Column(Integer, default=0)
    last_analysis_time = Column(DateTime)
    analysis_metadata = Column(Text)


# Create tables
def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
