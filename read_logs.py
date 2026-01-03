import json
from pathlib import Path

def read_logs():
    file_path = Path("dev_history.json")
    
    if not file_path.exists():
        print("\n[!] No history file found.")
        return

    with file_path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    print("\n" + "="*60)
    print("      DEVELOPMENT HISTORY & NOTES")
    print("="*60)
    
    keyword = input("Search by keyword (or press Enter for all): ").lower()
    
    found = False
    for log in data:
        # Busca tanto no status quanto nas notas
        if keyword in log['status'].lower() or keyword in log.get('notes', '').lower() or keyword in log['project'].lower():
            print(f"\n>> [{log['timestamp']}] | PROJECT: {log['project']}")
            print(f"   STATUS: {log['status']}")
            print(f"   NOTES:  {log.get('notes', 'N/A')}")
            print("-" * 40)
            found = True
            
    if not found:
        print("No entries found.")

if __name__ == "__main__":
    read_logs()