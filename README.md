# Candy Crush Pattern Detection System

An intelligent analysis and pattern detection system for **Candy Crush Soda Saga** levels using a **multi-pass approach** to progressively discover patterns, from high-level to granular details.

## 🎯 Features

### 5-Pass Analysis System
The system analyzes each level iteratively, improving detail with each pass:

1. **Pass 1: General Structure**
   - Board dimensions
   - Layout and arrangements
   - Game modes
   - Scoring mechanics

2. **Pass 2: Gameplay Mechanics**
   - Gameplay patterns
   - Spawners and positions
   - Gravity and physics
   - Special candies

3. **Pass 3: Blockers and Obstacles**
   - Blocker types
   - Obstacle density
   - Pattern distribution
   - Interaction rules

4. **Pass 4: Advanced Mechanics**
   - Multiple cameras
   - Scrolling levels
   - Portals and mechanisms
   - Control complexity

5. **Pass 5: Correlation Analysis**
   - Correlations between features
   - Level clustering
   - Anomaly detection
   - Difficulty recommendations

### Analysis Tracking
- Each level tracks which passes have been completed
- Real-time progress visualization
- Statistics per pass
- Average passes completed

## 📂 Project Structure

```
patterns/
├── api/                      # FastAPI REST API
│   ├── main.py              # Main application
│   ├── routes_levels.py     # Level endpoints
│   ├── routes_analysis.py   # Analysis endpoints
│   └── schemas.py           # Pydantic schemas
├── analyzer/                # Analysis engine
│   ├── json_loader.py       # JSON loader
│   ├── pattern_detector.py  # Pattern detector (5 passes)
│   └── level_analyzer.py    # Analysis orchestrator
├── db/                      # Database
│   └── models.py            # SQLAlchemy models
├── cli.py                   # Interactive CLI
├── config.py                # Configuration
├── requirements.txt         # Python dependencies
└── patterns.db              # SQLite database (auto-created)
```

## 🚀 Quick Start

### 1. Installation

```bash
cd patterns
pip install -r requirements.txt
```

### 2. Interactive CLI (Recommended)

```bash
python3 cli.py
```

Interactive menu with options:
- **1**: Load levels (10 at a time)
- **2**: Run specific pass
- **3**: View analysis progress
- **4**: Run all 4 passes
- **5**: Exit

**Example:**
```
Select option (1-5): 1
Current levels in DB: 0
How many levels to load? (default 10): 100
Loading 100 levels in batches of 10...
✓ Loaded 100 new levels
Total in DB: 100

Select option (1-5): 4
Running all 4 passes...
--- Pass 1 ---
Analyzed 100 levels
Total progress: 100/100 (100.0%)
...
✓ All passes completed!
```

### 3. REST API

Start server:
```bash
python3 -m uvicorn api.main:app --host 0.0.0.0 --port 8000
```

Access:
- Interactive docs: http://localhost:8000/docs
- OpenAPI spec: http://localhost:8000/openapi.json

**Main endpoints:**

```bash
# Load levels
POST /analysis/load-levels?limit=50

# Run analysis
POST /analysis/run-pass/1           # Pass 1
POST /analysis/run-pass/2           # Pass 2
POST /analysis/run-all-passes       # All passes

# View progress
GET /analysis/progress

# Statistics
GET /analysis/stats

# Get patterns for a level
GET /levels/1?level_id=199850
```

## 📊 Output Example

### Analysis Progress
```
Total levels: 200
==================================================

Pass 1: [████████████████████] 100.0% (200/200)
Pass 2: [████████████████████] 100.0% (200/200)
Pass 3: [████████████████████] 100.0% (200/200)
Pass 4: [████████████████████] 100.0% (200/200)

Average passes per level: 4.0
```

### API Statistics
```json
{
  "summary": {
    "total_levels": 200,
    "total_analyses": 800,
    "average_analyses_per_level": 4.0
  },
  "progress": {
    "total_levels": 200,
    "average_passes_per_level": 4.0,
    "pass_statistics": {
      "pass_1": { "completed": 200, "percent": 100.0 },
      "pass_2": { "completed": 200, "percent": 100.0 },
      "pass_3": { "completed": 200, "percent": 100.0 },
      "pass_4": { "completed": 200, "percent": 100.0 }
    }
  },
  "correlations": {
    "board_size_range": {
      "min": 49,
      "max": 589,
      "avg": 104.1
    }
  }
}
```

## 🗄️ Database

SQLite with tables:

- **levels**: Level metadata with pass tracking
- **level_raw_data**: Raw JSON data (efficient storage)
- **level_analyses**: Results for each analysis pass
- **patterns**: Pattern definitions
- **pattern_instances**: Level↔pattern mappings
- **global_statistics**: System-wide statistics

## 🔧 Configuration

File `.env`:
```env
DATABASE_URL=sqlite:///./patterns.db
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=true
JSON_INPUT_PATH=/path/to/level/json
```

## 📈 Performance

- **Loading**: ~10 levels per second
- **Analysis (Pass 1)**: ~30 levels per second
- **Analysis (Pass 2-4)**: ~20 levels per second
- **Batching**: 10 at a time to avoid timeouts
- **DB**: SQLite optimized with indexes

## 🎮 Detected Patterns

### Board Dimensions
- 6x5, 7x6, 8x5, etc.
- Regular and irregular layouts

### Mechanics
- Giant Bears, Soda, Timed modes
- Spawners and cameras
- Gravity types

### Blockers
- Ice, Chocolate, Licorice
- Density and distribution
- Complexity

### Advanced
- Scroll levels
- Multiple play areas
- Portals and tubes

## 📝 Notes

- The system is completely autonomous and resumable
- Each pass is independent and can run separately
- Already analyzed levels are not reprocessed
- Compatible with Candy Crush Soda Saga LIVE JSON files
- No external dependencies (uses native SQLite)

## 🚀 Future Improvements

- [ ] Export results (CSV, JSON)
- [ ] Web dashboard with visualization
- [ ] Machine learning for automatic clustering
- [ ] Difficulty recommendations
- [ ] Predictive analysis

---

**Advanced level analysis system for Candy Crush Soda Saga**
