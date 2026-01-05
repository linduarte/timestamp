import json
import sys
from pathlib import Path
from datetime import datetime

def generate_and_save_log():
    file_path = Path("dev_history.json")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print("\n" + "="*50)
    print(f" LOG GENERATOR - {now} ")
    print("="*50)
    
    project = input("Project Name: ").strip() or "General"
    status = input(f"[{project}] - Main Status/Title: ") or "Ongoing progress"
    
    print("\n--- PASTE YOUR NOTES BELOW ---")
    print("(When finished, press ENTER and then CTRL+Z and ENTER to save)")
    print("-" * 50)
    
    # sys.stdin.read() lê todo o bloco colado de uma vez sem executar no terminal
    try:
        notes_data = sys.stdin.read().strip()
    except EOFError:
        notes_data = ""
            
    notes = notes_data if notes_data else "No additional notes."
    
    log_entry = {
        "timestamp": now,
        "project": project,
        "status": status,
        "notes": notes
    }
    
    # Persistência com Pathlib
    data = []
    if file_path.exists():
        try:
            with file_path.open("r", encoding="utf-8") as file:
                data = json.load(file)
        except (json.JSONDecodeError, ValueError):
            data = []
    
    data.append(log_entry)
    
    with file_path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    
    # Saída formatada para o Chat
    log_output = (
        f"--- SESSION LOG ---\n"
        f"PROJECT: {project}\n"
        f"TIMESTAMP: {now}\n"
        f"STATUS: {status}\n"
        f"NOTES:\n{notes}\n"
        f"-------------------"
    )
    
    print("\n" + "!"*30)
    print("SUCCESSFULLY RECORDED!")
    print("COPY THE CONTENT BELOW TO YOUR AI:")
    print("!"*30 + "\n")
    print(log_output)

if __name__ == "__main__":
    generate_and_save_log()