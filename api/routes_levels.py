from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.models import get_db, Level
from api.schemas import Level as LevelSchema, AnalysisResponse, SummaryResponse
from analyzer.level_analyzer import LevelAnalyzer

router = APIRouter(prefix="/levels", tags=["levels"])

@router.get("/", response_model=SummaryResponse)
def get_summary(db: Session = Depends(get_db)):
    """Get summary of all levels"""
    analyzer = LevelAnalyzer(db)
    return analyzer.get_levels_summary()

@router.get("/count")
def get_level_count(db: Session = Depends(get_db)):
    """Get total count of levels in database"""
    count = db.query(Level).count()
    return {"total_levels": count}

@router.get("/{level_id}", response_model=AnalysisResponse)
def get_level_patterns(level_id: int, db: Session = Depends(get_db)):
    """Get all patterns for a specific level"""
    analyzer = LevelAnalyzer(db)
    result = analyzer.get_level_patterns(level_id)
    
    if not result:
        raise HTTPException(status_code=404, detail="Level not found")
    
    return result

@router.get("/by-episode/{episode}")
def get_levels_by_episode(episode: int, db: Session = Depends(get_db)):
    """Get all levels from a specific episode"""
    levels = db.query(Level).filter(Level.episode == episode).all()
    return {"episode": episode, "levels": [{"id": l.id, "name": l.level_name} for l in levels]}
