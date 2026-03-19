# Usage Guide - Pattern Detection System

## 🎯 Objective

This system analyzes JSONs of Candy Crush Soda Saga levels, discovering patterns progressively through 4 increasingly detailed analysis passes.

## 📋 Step by Step

### Step 1: Preparation

```bash
cd patterns
pip install -r requirements.txt
```

### Step 2: Use the CLI (Recommended Option)

```bash
python3 cli.py
```

**Typical flow:**
1. Option **1**: Load levels (10 at a time to avoid issues)
2. Option **2**: Run analysis by pass
3. Option **3**: View progress in visual bars
4. Option **4**: Run all passes automatically

### Step 3 (Alternative): Use the API

```bash
# Terminal 1: Start server
python3 -m uvicorn api.main:app --host 0.0.0.0 --port 8000

# Terminal 2: Make requests
curl -X POST http://localhost:8000/analysis/load-levels?limit=50
curl -X POST http://localhost:8000/analysis/run-pass/1
curl http://localhost:8000/analysis/progress
```

## 📊 Results Interpretation

### Progress Bar (CLI)
```
Pass 1: [████████████████████] 100.0% (200/200)
Pass 2: [██████████░░░░░░░░░░] 50.0% (100/200)
Pass 3: [░░░░░░░░░░░░░░░░░░░░] 0.0% (0/200)
Pass 4: [░░░░░░░░░░░░░░░░░░░░] 0.0% (0/200)
```

- `████` = Completed
- `░░░░` = Pending
- Percentage = % of levels analyzed in that pass

### Average Passes
- **0.0**: Nothing analyzed
- **1.0-2.0**: First passes in progress
- **4.0-5.0**: System completely analyzed

## 🔍 What's Detected in Each Pass

### Pass 1: Structure
- Board size (7x7, 6x5, etc.)
- Mode type (Giant Bears, Soda, etc.)
- Number of moves
- Stars and scoring

### Pass 2: Gameplay
- Number of spawners
- Gravity types
- Available special candies

### Pass 3: Blockers
- Types: ice, chocolate, etc.
- Board density
- Obstacle complexity

### Pass 4: Advanced
- Multiple cameras
- Scrolling levels
- Portals and special mechanisms

## 💡 Tips

1. **Start small**: Load 10-50 levels first to test
2. **Monitor progress**: Use option 3 to see progress
3. **Pause if needed**: The system will resume where it left off
4. **For large amounts**: Use CLI, it's more stable

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| API closes | Use CLI instead of API for large loads |
| Slow levels | Reduce `limit` in load-levels to 20-30 |
| DB errors | Delete `patterns.db` and restart |

## 📈 Scale

System tested with:
- ✓ 100 levels
- ✓ 200 levels
- ✓ Incremental loading
- ✓ Complete analysis (4 passes)

---

**Ready! The system is working correctly.**
