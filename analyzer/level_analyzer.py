from typing import Dict, Any, List
from sqlalchemy.orm import Session
from db.models import Level, LevelRawData, LevelAnalysis, Pattern, PatternInstance, GlobalStatistics
from analyzer.json_loader import JSONLoader, extract_level_info
from analyzer.pattern_detector import PatternDetector
import json

class LevelAnalyzer:
    """Multi-pass analysis engine for Candy Crush levels"""
    
    def __init__(self, db: Session):
        self.db = db
        self.loader = JSONLoader()
    
    def load_and_store_levels(self, batch_size: int = 100, limit: int = None):
        """Load all JSONs and store in database with batching"""
        levels = self.loader.load_all_levels()
        stored_count = 0
        batch = []
        
        for idx, level_data in enumerate(levels):
            if limit and idx >= limit:
                break
            
            try:
                level_info = extract_level_info(level_data['data'])
                
                # Check if already stored
                existing = self.db.query(Level).filter(
                    Level.level_id == level_info['level_id']
                ).first()
                
                if not existing:
                    # Store metadata
                    db_level = Level(
                        level_id=level_info['level_id'],
                        level_name=level_info['name'],
                        episode=level_info['episode']
                    )
                    batch.append((db_level, level_info['raw_json']))
                    
                    # Batch commit
                    if len(batch) >= batch_size:
                        levels_to_add = [item[0] for item in batch]
                        self.db.add_all(levels_to_add)
                        self.db.flush()  # Flush to get IDs
                        
                        # Store raw data
                        for db_level, raw_json in batch:
                            raw_data = LevelRawData(
                                level_id=db_level.level_id,
                                raw_json=json.dumps(raw_json).encode('utf-8')
                            )
                            self.db.add(raw_data)
                        
                        self.db.commit()
                        stored_count += len(batch)
                        batch = []
                        
            except Exception as e:
                print(f"Error storing level: {e}")
        
        # Final batch
        if batch:
            levels_to_add = [item[0] for item in batch]
            self.db.add_all(levels_to_add)
            self.db.flush()
            
            for db_level, raw_json in batch:
                raw_data = LevelRawData(
                    level_id=db_level.level_id,
                    raw_json=json.dumps(raw_json).encode('utf-8')
                )
                self.db.add(raw_data)
            
            self.db.commit()
            stored_count += len(batch)
        
        return stored_count
    
    def analyze_level(self, level_id: int) -> Dict[str, Any]:
        """Analyze a single level with all 4 passes"""
        db_level = self.db.query(Level).filter(
            Level.level_id == level_id
        ).first()
        
        if not db_level:
            return None
        
        # Get raw data
        raw_data_obj = self.db.query(LevelRawData).filter(
            LevelRawData.level_id == level_id
        ).first()
        
        if not raw_data_obj:
            return None
        
        raw_data = json.loads(raw_data_obj.raw_json.decode('utf-8'))
        analysis_results = PatternDetector.analyze_full_level(raw_data)
        
        return analysis_results
    
    def store_analysis(self, db_level_id: int, pass_number: int, analysis: Dict):
        """Store analysis results in database"""
        db_analysis = LevelAnalysis(
            level_id=db_level_id,
            pass_number=pass_number,
            patterns_found=json.dumps(analysis),
            analysis_data=json.dumps(analysis)
        )
        self.db.add(db_analysis)
        self.db.commit()
    
    def run_full_analysis_pass(self, pass_number: int = 1):
        """Run a full pass on all levels - Only un-analyzed levels"""
        levels = self.db.query(Level).all()
        updated_count = 0
        
        for db_level in levels:
            try:
                # Check if this pass already done for this level
                existing = self.db.query(LevelAnalysis).filter(
                    LevelAnalysis.level_id == db_level.id,
                    LevelAnalysis.pass_number == pass_number
                ).first()
                
                if existing:
                    continue  # Skip already analyzed
                
                # Run analysis
                analysis = self.analyze_level(db_level.level_id)
                
                if analysis:
                    # Extract specific pass data
                    pass_key = f'pass_{pass_number}'
                    pass_data = analysis.get(pass_key, {})
                    
                    self.store_analysis(db_level.id, pass_number, pass_data)
                    
                    # Update passes completed
                    passes_set = set(map(int, db_level.passes_completed.split(',') if db_level.passes_completed else []))
                    passes_set.add(pass_number)
                    db_level.passes_completed = ','.join(map(str, sorted(passes_set)))
                    db_level.total_passes = len(passes_set)
                    self.db.commit()
                    
                    updated_count += 1
                    
            except Exception as e:
                print(f"Error analyzing level {db_level.level_id} pass {pass_number}: {e}")
        
        # Update global stats
        self.update_global_stats(pass_number, updated_count)
        
        return updated_count
    
    def update_global_stats(self, pass_number: int, levels_processed: int):
        """Update global analysis statistics"""
        stats = self.db.query(GlobalStatistics).first()
        
        if not stats:
            stats = GlobalStatistics(
                total_levels_analyzed=levels_processed,
                current_pass=pass_number
            )
            self.db.add(stats)
        else:
            stats.current_pass = pass_number
            stats.total_levels_analyzed = self.db.query(Level).count()
        
        self.db.commit()
    
    def get_levels_summary(self) -> Dict[str, Any]:
        """Get summary of all levels"""
        total_levels = self.db.query(Level).count()
        total_analyses = self.db.query(LevelAnalysis).count()
        
        return {
            'total_levels': total_levels,
            'total_analyses': total_analyses,
            'average_analyses_per_level': total_analyses / total_levels if total_levels > 0 else 0
        }
    
    def get_level_patterns(self, level_id: int) -> Dict[str, Any]:
        """Get all patterns for a specific level"""
        db_level = self.db.query(Level).filter(
            Level.level_id == level_id
        ).first()
        
        if not db_level:
            return None
        
        analyses = self.db.query(LevelAnalysis).filter(
            LevelAnalysis.level_id == db_level.id
        ).order_by(LevelAnalysis.pass_number).all()
        
        return {
            'level_id': level_id,
            'analyses': [
                {
                    'pass_number': a.pass_number,
                    'patterns': json.loads(a.patterns_found)
                }
                for a in analyses
            ]
        }
    
    def correlate_patterns(self) -> Dict[str, Any]:
        """PASS 5: Find correlations between patterns (requires all levels analyzed)"""
        analyses = self.db.query(LevelAnalysis).filter(
            LevelAnalysis.pass_number == 1
        ).all()
        
        if not analyses:
            return {'error': 'No level 1 analyses found'}
        
        # Extract metrics for correlation
        board_sizes = []
        game_modes = []
        
        for analysis in analyses:
            data = json.loads(analysis.analysis_data)
            board_dims = data.get('board_dimensions', {})
            mode = data.get('game_mode', {})
            
            board_sizes.append({
                'level_id': analysis.level_id,
                'size': board_dims.get('total_tiles', 0)
            })
            game_modes.append({
                'level_id': analysis.level_id,
                'mode': mode.get('mode_type', 'Unknown')
            })
        
        return {
            'correlations_found': {
                'board_size_range': {
                    'min': min([b['size'] for b in board_sizes]) if board_sizes else 0,
                    'max': max([b['size'] for b in board_sizes]) if board_sizes else 0,
                    'avg': sum(b['size'] for b in board_sizes) / len(board_sizes) if board_sizes else 0
                },
                'game_modes_distribution': self._count_distribution([m['mode'] for m in game_modes])
            },
            'pass_number': 5,
            'pass_name': 'Correlation Analysis'
        }
    
    @staticmethod
    def _count_distribution(items: List) -> Dict:
        """Helper to count item distribution"""
        counts = {}
        for item in items:
            counts[item] = counts.get(item, 0) + 1
        return counts
