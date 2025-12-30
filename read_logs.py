import json
from pathlib import Path

def read_logs():
    # Define o caminho do arquivo usando Path
    file_path = Path("dev_history.json")
    
    # Verifica existência de forma elegante
    if not file_path.exists():
        print(f"\n[!] File not found at: {file_path.absolute()}")
        print("Please run 'generate_log.py' first.")
        return

    try:
        # Abre e lê o arquivo usando o método do objeto Path
        with file_path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except (json.JSONDecodeError, ValueError):
        print("\n[!] Error: The log file is empty or contains invalid JSON.")
        return

    # Extrai projetos únicos para o menu
    projects = sorted(list(set(log['project'] for log in data)))
    
    print("\n" + "="*60)
    print(f"      LOG VIEWER | Source: {file_path.name}")
    print("="*60)
    print("1. View All Logs")
    print("2. Filter by Project")
    print("3. Search by Keyword")
    
    choice = input("\nChoose an option: ")
    
    # Cabeçalho da tabela
    print("\n" + "-"*85)
    print(f"{'TIMESTAMP':<20} | {'PROJECT':<18} | {'STATUS'}")
    print("-" * 85)

    results = []
    
    if choice == "2":
        print("\nAvailable Projects:")
        for idx, p in enumerate(projects, 1):
            print(f"{idx}. {p}")
        
        try:
            p_idx = int(input("\nSelect project number: ")) - 1
            if 0 <= p_idx < len(projects):
                target = projects[p_idx]
                results = [log for log in data if log['project'] == target]
            else:
                print("Invalid selection.")
                return
        except ValueError:
            return

    elif choice == "3":
        keyword = input("Enter keyword (e.g. 'bug', 'fix'): ").lower()
        results = [log for log in data if keyword in log['status'].lower() or keyword in log['project'].lower()]
    
    else:
        results = data

    # Exibição dos resultados
    for log in results:
        # Limita o tamanho do nome do projeto para não quebrar a tabela
        proj_display = (log['project'][:15] + '..') if len(log['project']) > 15 else log['project']
        print(f"{log['timestamp']:<20} | {proj_display:<18} | {log['status']}")
            
    if not results:
        print("No matching entries found.")
        
    print("-" * 85)
    print(f"Total entries: {len(results)} | Location: {file_path.absolute()}")

if __name__ == "__main__":
    read_logs()