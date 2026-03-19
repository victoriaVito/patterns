import json
import os
from pathlib import Path
from typing import Dict, List, Any, Iterator
from config import settings

class JSONLoader:
    """Load and validate Candy Crush level JSONs with lazy loading"""
    
    def __init__(self, input_path: str = None):
        self.input_path = Path(input_path or settings.json_input_path)
    
    def load_all_levels(self) -> Iterator[Dict[str, Any]]:
        """Lazily load JSON files from the input directory"""
        if not self.input_path.exists():
            raise FileNotFoundError(f"Input path not found: {self.input_path}")
        
        json_files = sorted(self.input_path.glob("*.json"))
        
        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    yield {
                        'file_name': json_file.name,
                        'data': data
                    }
            except json.JSONDecodeError as e:
                print(f"Error parsing {json_file.name}: {e}")
            except Exception as e:
                print(f"Error loading {json_file.name}: {e}")
    
    def load_single_level(self, file_path: str) -> Dict[str, Any]:
        """Load a single JSON file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def get_level_count(self) -> int:
        """Get total number of JSON files"""
        if not self.input_path.exists():
            return 0
        return len(list(self.input_path.glob("*.json")))


def extract_level_info(raw_data: Dict) -> Dict[str, Any]:
    """Extract basic level information from raw JSON"""
    level_data = raw_data.get('level', {})
    
    return {
        'id': raw_data.get('levelId'),
        'level_id': raw_data.get('levelId'),
        'name': f"Level {raw_data.get('levelId')}",
        'episode': raw_data.get('id'),
        'raw_json': raw_data
    }
