import json
import sys
from pathlib import Path
from datetime import datetime

def generate_and_save_log():
    file_path = Path("dev_history.json")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = []

    # Carrega dados existentes
    if file_path.exists():
        try:
            with file_path.open("r", encoding="utf-8") as file:
                data = json.load(file)
        except (json.JSONDecodeError, ValueError):
            pass

    print("\n" + "="*50)
    print(f" LOG GENERATOR - {now} ")
    print("="*50)

    # Opção de Reuso
    reuse = input("Reuse a previous log? (y/N): ").lower().strip() == 'y'
    
    if reuse and data:
        # Mostra os últimos 5 logs para escolha rápida
        print("\nLast 5 logs:")
        last_logs = data[-5:][::-1] # Pega os últimos 5 e inverte a ordem
        for idx, log in enumerate(last_logs, 1):
            print(f"{idx}. [{log['project']}] {log['status'][:40]}...")
        
        try:
            choice = int(input("\nSelect log number to reuse: ")) - 1
            selected = last_logs[choice]
            project = selected['project']
            status = selected['status']
            notes = selected.get('notes', "")
            print(f"\n[Reusing Project: {project}]")
            print(f"[Reusing Status: {status}]")
        except (ValueError, IndexError):
            print("Invalid choice, starting new log.")
            reuse = False

    if not reuse:
        project = input("Project Name: ").strip() or "General"
        status = input(f"[{project}] - Main Status/Title: ") or "Ongoing progress"
        print("\n--- PASTE YOUR NOTES BELOW ---")
        print("(Press ENTER, then CTRL+Z and ENTER to save)")
        print("-" * 50)
        try:
            notes = sys.stdin.read().strip()
        except EOFError:
            notes = ""

    # Cria a nova entrada com o tempo ATUALIZADO
    new_entry = {
        "timestamp": now,
        "project": project,
        "status": status,
        "notes": notes
    }
    
    data.append(new_entry)
    
    with file_path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    
    # Saída formatada para o Chat
    log_output = (
        f"--- SESSION LOG ---\n"
        f"PROJECT: {project}\n"
        f"TIMESTAMP: {now} (UPDATED)\n"
        f"STATUS: {status}\n"
        f"NOTES:\n{notes}\n"
        f"-------------------"
    )
    
    print("\n" + "!"*30)
    print("LOG UPDATED AND SAVED!")
    print("COPY THE CONTENT BELOW:")
    print("!"*30 + "\n")
    print(log_output)

if __name__ == "__main__":
    generate_and_save_log()