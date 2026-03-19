from typing import Dict, Any, List
from collections import defaultdict

class PatternDetector:
    """Detect patterns in Candy Crush levels - Multi-Pass System"""
    
    # PASADA 1: BOARD DIMENSIONS & LAYOUTS
    @staticmethod
    def detect_board_dimensions(level_data: Dict) -> Dict[str, Any]:
        """Extract board dimensions from tileMap"""
        tile_map = level_data.get('level', {}).get('tileMap', [])
        
        if not tile_map:
            return {}
        
        height = len(tile_map)
        width = len(tile_map[0]) if tile_map else 0
        
        return {
            'width': width,
            'height': height,
            'total_tiles': width * height,
            'aspect_ratio': f"{width}x{height}"
        }
    
    @staticmethod
    def detect_board_layout(level_data: Dict) -> Dict[str, Any]:
        """Detect board shape and special layouts"""
        tile_map = level_data.get('level', {}).get('tileMap', [])
        
        if not tile_map:
            return {'type': 'unknown'}
        
        # Count different tile types
        tile_counts = defaultdict(int)
        total_tiles = 0
        
        for row in tile_map:
            for tile in row:
                total_tiles += 1
                if isinstance(tile, list) and len(tile) > 0:
                    tile_counts[tile[0]] += 1
        
        # Check for special layouts
        is_regular = all(len(row) == len(tile_map[0]) for row in tile_map)
        
        return {
            'is_regular_grid': is_regular,
            'tile_variety': len(tile_counts),
            'tile_distribution': dict(tile_counts),
            'layout_type': 'regular' if is_regular else 'irregular'
        }
    
    @staticmethod
    def detect_game_mode(level_data: Dict) -> Dict[str, Any]:
        """Detect game mode type"""
        level = level_data.get('level', {})
        
        game_mode_name = level.get('gameModeName', 'Unknown')
        moves_limit = level.get('movesLimit', 0)
        
        # Determine mode type
        if 'Bears' in game_mode_name or 'Bear' in game_mode_name:
            mode_type = 'Giant Bears'
        elif 'Soda' in game_mode_name:
            mode_type = 'Soda'
        elif 'Timed' in game_mode_name or 'Time' in game_mode_name:
            mode_type = 'Timed'
        else:
            mode_type = game_mode_name
        
        return {
            'mode_name': game_mode_name,
            'mode_type': mode_type,
            'moves_limit': moves_limit
        }
    
    @staticmethod
    def detect_score_mechanics(level_data: Dict) -> Dict[str, Any]:
        """Detect score thresholds and mechanics"""
        level = level_data.get('level', {})
        
        star_level = level.get('starlevel', [])
        score_targets = level.get('scoreTargets', [])
        
        return {
            'star_thresholds': star_level,
            'score_targets': score_targets,
            'max_score': max(score_targets) if score_targets else 0,
            'num_stars': len(star_level)
        }
    
    @staticmethod
    def pass_1_general_patterns(level_data: Dict) -> Dict[str, Any]:
        """PASS 1: Detect board dimensions, layouts, modes, scores"""
        return {
            'board_dimensions': PatternDetector.detect_board_dimensions(level_data),
            'board_layout': PatternDetector.detect_board_layout(level_data),
            'game_mode': PatternDetector.detect_game_mode(level_data),
            'score_mechanics': PatternDetector.detect_score_mechanics(level_data),
            'pass_number': 1,
            'pass_name': 'General Structure (Board, Layout, Mode, Score)'
        }
    
    # PASADA 2: GAMEPLAY MECHANICS
    @staticmethod
    def detect_gameplay_patterns(level_data: Dict) -> Dict[str, Any]:
        """Detect gameplay patterns, spawners, gravity"""
        level = level_data.get('level', {})
        
        # Candy cannons = spawners
        candy_cannons = level.get('candyCannons', [])
        
        # Acceleration map = gravity
        acceleration_map = level.get('accelerationMap', [])
        
        gravity_types = set()
        if acceleration_map:
            for row in acceleration_map:
                for tile in row:
                    if isinstance(tile, (list, tuple)) and len(tile) >= 1:
                        gravity_types.add(f"gravity_{tile[0]}")
        
        # Liquorice mechanics
        liquorice_spawn_rate = level.get('liquoriceSpawnRate', 0)
        
        return {
            'spawners': {
                'count': len(candy_cannons),
                'positions': [cc.get('coordinate', []) for cc in candy_cannons],
                'types': [cc.get('normalType', 'unknown') for cc in candy_cannons]
            },
            'gravity': {
                'has_acceleration': bool(acceleration_map),
                'gravity_types': list(gravity_types),
                'is_standard_gravity': len(gravity_types) <= 1
            },
            'liquorice': {
                'spawn_rate': liquorice_spawn_rate,
                'has_liquorice': liquorice_spawn_rate > 0
            }
        }
    
    @staticmethod
    def detect_special_candies(level_data: Dict) -> Dict[str, Any]:
        """Detect special candies/power-ups"""
        level = level_data.get('level', {})
        
        special_candies = level.get('specialCandiesAmmunitionData', [])
        
        candy_types = {}
        for candy in special_candies:
            ammo_type = candy.get('ammunitionType', 'unknown')
            candy_types[ammo_type] = {
                'spawn_amount': candy.get('amountPerSpawn', 0),
                'spawn_interval': candy.get('spawnInterval', 0),
                'available': candy.get('amountPerSpawn', 0) > 0
            }
        
        return {
            'special_candies_available': sum(1 for c in candy_types.values() if c['available']),
            'candy_types': candy_types
        }
    
    @staticmethod
    def pass_2_gameplay(level_data: Dict) -> Dict[str, Any]:
        """PASS 2: Detect gameplay mechanics, spawners, gravity"""
        return {
            'gameplay_patterns': PatternDetector.detect_gameplay_patterns(level_data),
            'special_candies': PatternDetector.detect_special_candies(level_data),
            'pass_number': 2,
            'pass_name': 'Gameplay Mechanics (Spawners, Gravity, Special Candies)'
        }
    
    # PASADA 3: BLOCKERS & OBSTACLES
    @staticmethod
    def detect_blockers(level_data: Dict) -> Dict[str, Any]:
        """Detect blocker types and distribution"""
        level = level_data.get('level', {})
        
        # Blocker ammunition data
        blocker_ammo = level.get('blockerTypeAmmunitionData', [])
        
        blocker_types = {}
        for blocker in blocker_ammo:
            ammo_type = blocker.get('ammunitionType', 'unknown')
            blocker_types[ammo_type] = {
                'spawn_amount': blocker.get('amountPerSpawn', 0),
                'spawn_interval': blocker.get('spawnInterval', 0),
                'min_on_screen': blocker.get('minimumOnScreen', 0),
                'max_on_screen': blocker.get('maximumOnScreen', 0),
                'active': blocker.get('amountPerSpawn', 0) > 0 or blocker.get('minimumOnScreen', 0) > 0
            }
        
        # Analyze tile map for blocker density
        tile_map = level.get('tileMap', [])
        blocker_tile_count = 0
        total_tiles = 0
        
        for row in tile_map:
            for tile in row:
                total_tiles += 1
                if isinstance(tile, list) and len(tile) > 0:
                    # Tiles with multiple layers often have blockers
                    if len(tile) > 1:
                        blocker_tile_count += 1
        
        blocker_density = (blocker_tile_count / total_tiles * 100) if total_tiles > 0 else 0
        
        return {
            'blocker_types_active': sum(1 for b in blocker_types.values() if b['active']),
            'blocker_types': blocker_types,
            'blocker_density_percent': round(blocker_density, 2),
            'has_complex_blockers': blocker_density > 20
        }
    
    @staticmethod
    def pass_3_blockers(level_data: Dict) -> Dict[str, Any]:
        """PASS 3: Detect blockers and obstacles"""
        return {
            'blockers': PatternDetector.detect_blockers(level_data),
            'pass_number': 3,
            'pass_name': 'Blockers & Obstacles (Ice, Chocolate, Frosting, etc.)'
        }
    
    # PASADA 4: ADVANCED MECHANICS
    @staticmethod
    def detect_camera_mechanics(level_data: Dict) -> Dict[str, Any]:
        """Detect camera and scrolling mechanics"""
        level = level_data.get('level', {})
        
        camera_targets = level.get('cameraTargets', [])
        portals = level.get('portals', [])
        portal_tubes = level.get('portalTubes', [])
        
        has_scrolling = len(camera_targets) > 1
        has_multiple_areas = bool(portals) or bool(portal_tubes)
        
        return {
            'camera_targets': camera_targets,
            'num_camera_zones': len(camera_targets),
            'has_scrolling_levels': has_scrolling,
            'has_portals': bool(portals),
            'has_portal_tubes': bool(portal_tubes),
            'has_multiple_play_areas': has_multiple_areas,
            'complexity_level': 'complex' if has_scrolling or has_multiple_areas else 'simple'
        }
    
    @staticmethod
    def pass_4_advanced(level_data: Dict) -> Dict[str, Any]:
        """PASS 4: Detect advanced mechanics (cameras, scrolling, portals)"""
        return {
            'camera_mechanics': PatternDetector.detect_camera_mechanics(level_data),
            'pass_number': 4,
            'pass_name': 'Advanced Mechanics (Cameras, Scrolling, Portals)'
        }
    
    # PASADA 5: CORRELATIONAL ANALYSIS
    @staticmethod
    def pass_5_correlation(level_data: Dict, all_previous_passes: List[Dict]) -> Dict[str, Any]:
        """PASS 5: Correlational analysis, clustering, anomalies"""
        return {
            'correlations': {},  # Populated when analyzing multiple levels
            'pass_number': 5,
            'pass_name': 'Correlation & Anomaly Detection'
        }
    
    @staticmethod
    def analyze_full_level(level_data: Dict) -> Dict[str, Any]:
        """Run all 4 passes (5th requires multiple levels)"""
        return {
            'pass_1': PatternDetector.pass_1_general_patterns(level_data),
            'pass_2': PatternDetector.pass_2_gameplay(level_data),
            'pass_3': PatternDetector.pass_3_blockers(level_data),
            'pass_4': PatternDetector.pass_4_advanced(level_data)
        }
