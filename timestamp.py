import json
from pathlib import Path
from datetime import datetime

def generate_and_save_log():
    # Define o caminho usando pathlib
    file_path = Path("dev_history.json")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print("\n" + "="*40)
    print(f" LOG GENERATOR - {now} ")
    print("="*40)
    
    project = input("Project Name: ").strip() or "General"
    note = input(f"[{project}] - Current task/issue: ") or "Ongoing progress"
    
    log_entry = {
        "timestamp": now,
        "project": project,
        "status": note
    }
    
    # Gerenciamento de arquivo com pathlib
    data = []
    if file_path.exists():
        try:
            # Lê o conteúdo de forma mais limpa
            with file_path.open("r", encoding="utf-8") as file:
                data = json.load(file)
        except (json.JSONDecodeError, ValueError):
            data = []
    
    data.append(log_entry)
    
    # Escrita simplificada
    with file_path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    
    log_output = f"--- PROJECT: {project} | TIMESTAMP: {now} ---\nSTATUS: {note}\n"
    
    print("\n" + "-"*30)
    print("COPY THE TEXT BELOW TO YOUR AI CHAT:")
    print("-" * 30)
    print(log_output)
    print(f"Saved locally to: {file_path.absolute()}")

if __name__ == "__main__":
    generate_and_save_log()