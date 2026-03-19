from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from db.models import get_db, Level
from api.schemas import CorrelationResponse
from analyzer.level_analyzer import LevelAnalyzer
import asyncio

router = APIRouter(prefix="/analysis", tags=["analysis"])

@router.post("/load-levels")
def load_levels(limit: int = 100, db: Session = Depends(get_db)):
    """Load levels from JSON folder into database in batches"""
    analyzer = LevelAnalyzer(db)
    count = analyzer.load_and_store_levels(batch_size=10, limit=limit)
    
    total = db.query(Level).count()
    return {
        "status": "success",
        "levels_loaded_this_time": count,
        "total_levels_in_db": total,
        "message": f"Loaded {count} new levels (Total: {total})"
    }

@router.post("/run-pass/{pass_number}")
def run_analysis_pass(pass_number: int, db: Session = Depends(get_db)):
    """Run a specific analysis pass on all un-analyzed levels"""
    
    if pass_number < 1 or pass_number > 5:
        return {"error": "Pass number must be between 1 and 5"}
    
    analyzer = LevelAnalyzer(db)
    count = analyzer.run_full_analysis_pass(pass_number)
    
    total_levels = db.query(Level).count()
    analyzed = db.query(Level).filter(
        Level.passes_completed.like(f'%{pass_number}%')
    ).count()
    
    return {
        "status": "completed",
        "pass_number": pass_number,
        "levels_analyzed_in_pass": count,
        "total_levels_analyzed_for_pass": analyzed,
        "total_levels": total_levels,
        "progress_percent": round((analyzed / total_levels * 100), 2) if total_levels > 0 else 0
    }

@router.get("/progress")
def get_progress(db: Session = Depends(get_db)):
    """Get current analysis progress across all levels"""
    total = db.query(Level).count()
    
    if total == 0:
        return {
            "total_levels": 0,
            "message": "No levels loaded yet"
        }
    
    # Count levels by passes completed
    pass_stats = {}
    for pass_num in range(1, 6):
        count = db.query(Level).filter(
            Level.passes_completed.like(f'%{pass_num}%')
        ).count()
        pass_stats[f"pass_{pass_num}"] = {
            "completed": count,
            "percent": round((count / total * 100), 2)
        }
    
    # Get average passes per level
    avg_passes = db.query(Level).with_entities(
        Level.total_passes
    ).all()
    avg = sum([p[0] for p in avg_passes]) / len(avg_passes) if avg_passes else 0
    
    return {
        "total_levels": total,
        "average_passes_per_level": round(avg, 2),
        "pass_statistics": pass_stats,
        "message": f"Database contains {total} levels with analysis progress tracked"
    }

@router.post("/run-all-passes")
def run_all_passes(db: Session = Depends(get_db)):
    """Run all analysis passes sequentially"""
    analyzer = LevelAnalyzer(db)
    results = {}
    
    for pass_num in range(1, 5):
        count = analyzer.run_full_analysis_pass(pass_num)
        results[f"pass_{pass_num}"] = count
    
    progress = get_progress(db)
    
    return {
        "status": "completed",
        "passes_results": results,
        "final_progress": progress
    }

@router.get("/correlations", response_model=CorrelationResponse)
def get_correlations(db: Session = Depends(get_db)):
    """Get correlation analysis (Pass 5)"""
    analyzer = LevelAnalyzer(db)
    return analyzer.correlate_patterns()

@router.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    """Get global analysis statistics"""
    analyzer = LevelAnalyzer(db)
    summary = analyzer.get_levels_summary()
    correlations = analyzer.correlate_patterns()
    progress = get_progress(db)
    
    return {
        "summary": summary,
        "progress": progress,
        "correlations": correlations
    }
