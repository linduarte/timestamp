import json
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
    
    print("\nDetailed Notes (Briefly describe topics to work on):")
    notes = input("> ") or "No additional notes."
    
    log_entry = {
        "timestamp": now,
        "project": project,
        "status": status,
        "notes": notes
    }
    
    # Carregamento e salvamento com Pathlib
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
    
    # Saída formatada para o Chat de IA
    log_output = (
        f"--- SESSION LOG ---\n"
        f"PROJECT: {project}\n"
        f"TIMESTAMP: {now}\n"
        f"STATUS: {status}\n"
        f"NOTES/TOPICS: {notes}\n"
        f"-------------------"
    )
    
    print("\n--- COPY THE TEXT BELOW TO YOUR AI CHAT ---")
    print(log_output)

if __name__ == "__main__":
    generate_and_save_log()