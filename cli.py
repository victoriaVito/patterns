#!/usr/bin/env python3
"""
Standalone script to load and analyze Candy Crush levels in batches
without depending on HTTP API timeouts
"""
import sys
from db.models import SessionLocal, init_db, Level
from analyzer.level_analyzer import LevelAnalyzer

def main():
    # Initialize database
    init_db()
    db = SessionLocal()
    
    # Create analyzer
    analyzer = LevelAnalyzer(db)
    
    print("\n" + "="*60)
    print("CANDY CRUSH PATTERN DETECTION SYSTEM")
    print("="*60 + "\n")
    
    while True:
        print("\nOptions:")
        print("1. Load levels (10 at a time)")
        print("2. Run analysis pass")
        print("3. Check progress")
        print("4. Run all passes")
        print("5. Exit")
        
        choice = input("\nSelect option (1-5): ").strip()
        
        if choice == "1":
            current_count = db.query(Level).count()
            
            print(f"\nCurrent levels in DB: {current_count}")
            load_count = input("How many levels to load? (default 10): ").strip()
            load_count = int(load_count) if load_count else 10
            
            print(f"Loading {load_count} levels in batches of 10...")
            loaded = analyzer.load_and_store_levels(batch_size=10, limit=load_count)
            
            new_count = db.query(Level).count()
            print(f"✓ Loaded {loaded} new levels")
            print(f"Total in DB: {new_count}")
        
        elif choice == "2":
            pass_num = input("Which pass? (1-4): ").strip()
            if pass_num not in ["1", "2", "3", "4"]:
                print("Invalid pass number")
                continue
            
            pass_num = int(pass_num)
            print(f"\nRunning Pass {pass_num}...")
            analyzed = analyzer.run_full_analysis_pass(pass_num)
            
            total = db.query(Level).count()
            completed = db.query(Level).filter(
                Level.passes_completed.like(f'%{pass_num}%')
            ).count()
            
            print(f"✓ Analyzed {analyzed} levels in this pass")
            print(f"Progress: {completed}/{total} ({round(completed/total*100, 1)}%)")
        
        elif choice == "3":
            total = db.query(Level).count()
            
            if total == 0:
                print("\nNo levels in database yet")
                continue
            
            print(f"\n{'='*50}")
            print(f"Total levels: {total}")
            print(f"{'='*50}\n")
            
            for pass_num in range(1, 5):
                count = db.query(Level).filter(
                    Level.passes_completed.like(f'%{pass_num}%')
                ).count()
                pct = round(count / total * 100, 1)
                bar = "█" * int(pct / 5) + "░" * (20 - int(pct / 5))
                print(f"Pass {pass_num}: [{bar}] {pct}% ({count}/{total})")
            
            avg_passes = db.query(Level).with_entities(
                Level.total_passes
            ).all()
            avg = sum([p[0] for p in avg_passes]) / len(avg_passes) if avg_passes else 0
            print(f"\nAverage passes per level: {round(avg, 2)}")
        
        elif choice == "4":
            print("\nRunning all 4 passes...")
            
            for pass_num in range(1, 5):
                print(f"\n--- Pass {pass_num} ---")
                analyzed = analyzer.run_full_analysis_pass(pass_num)
                total = db.query(Level).count()
                completed = db.query(Level).filter(
                    Level.passes_completed.like(f'%{pass_num}%')
                ).count()
                print(f"Analyzed {analyzed} levels in this pass")
                print(f"Total progress: {completed}/{total} ({round(completed/total*100, 1)}%)")
            
            print("\n✓ All passes completed!")
        
        elif choice == "5":
            print("\nGoodbye!")
            db.close()
            sys.exit(0)
        
        else:
            print("Invalid option")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
