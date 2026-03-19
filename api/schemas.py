from pydantic import BaseModel
from typing import List, Dict, Any, Optional

# Level Schemas
class LevelBase(BaseModel):
    level_id: int
    level_name: str

class LevelCreate(LevelBase):
    raw_json: Dict[str, Any]

class Level(LevelBase):
    id: int
    
    class Config:
        from_attributes = True

# Analysis Schemas
class AnalysisBase(BaseModel):
    pass_number: int
    patterns_found: Dict[str, Any]

class AnalysisCreate(AnalysisBase):
    level_id: int

class Analysis(AnalysisBase):
    id: int
    level_id: int
    
    class Config:
        from_attributes = True

# Pattern Schemas
class PatternBase(BaseModel):
    pattern_name: str
    category: str
    description: Optional[str] = None

class PatternCreate(PatternBase):
    pass_number: int

class Pattern(PatternBase):
    id: int
    pass_number: int
    
    class Config:
        from_attributes = True

# Response Schemas
class AnalysisResponse(BaseModel):
    level_id: int
    analyses: List[Dict[str, Any]]

class SummaryResponse(BaseModel):
    total_levels: int
    total_analyses: int
    average_analyses_per_level: float

class CorrelationResponse(BaseModel):
    correlations_found: Dict[str, Any]
    pass_number: int
    pass_name: str
