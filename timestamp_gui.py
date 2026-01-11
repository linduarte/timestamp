import json
from pathlib import Path
from datetime import datetime
from nicegui import ui

# --- CONFIGURAÇÕES ---
BASE_DIR = Path(__file__).resolve().parent
FILE_PATH = BASE_DIR / "dev_history.json"

def load_data():
    if not FILE_PATH.exists():
        return []
    
    # Se o arquivo existir mas estiver vazio (0 bytes), json.load falha.
    if FILE_PATH.stat().st_size == 0:
        return []

    try:
        with FILE_PATH.open("r", encoding="utf-8") as file:
            data = json.load(file)
            # Garante que o que foi carregado é de fato uma lista
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, Exception) as e:
        print(f"Erro ao carregar JSON: {e}")
        return []

def save_data(data):
    with FILE_PATH.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# --- A CEREJA DO BOLO: ROTA RAIZ EXPLÍCITA ---
@ui.page('/')
def main_page():
    data = load_data()
    
    # Configuração de Cores e Dark Mode
    ui.colors(primary='#1e293b', secondary='#64748b', accent='#10b981')
    # Força o dark mode inicial se desejar, ou deixe o toggle
    # ui.dark_mode().enable()

    with ui.header().classes('items-center justify-between px-6 bg-primary shadow-md'):
        ui.label('TIMESTAMP PRO').classes('text-xl font-black tracking-tighter')
        with ui.row().classes('items-center gap-4'):
            ui.button(icon='dark_mode', on_click=lambda: ui.dark_mode().toggle()).props('flat color=white')
            ui.label(datetime.now().strftime("%H:%M")).classes('font-mono text-sm')

    with ui.tabs().classes('w-full') as tabs:
        editor_tab = ui.tab('EDITOR', icon='add_box')
        history_tab = ui.tab('HISTÓRICO', icon='format_list_bulleted')

    with ui.tab_panels(tabs, value=editor_tab).classes('w-full bg-transparent p-4'):
        
        # --- PAINEL EDITOR ---
        with ui.tab_panel(editor_tab):
            with ui.column().classes('w-full max-w-3xl mx-auto'):
                with ui.card().classes('w-full p-6 shadow-xl border-t-4 border-accent'):
                    ui.label('Nova Sessão').classes('text-2xl font-bold mb-4')
                    
                    project_input = ui.input('Projeto').classes('w-full')
                    status_input = ui.input('Status Principal').classes('w-full')
                    notes_input = ui.textarea('Notas Detalhadas').classes('w-full h-40').props('outlined')

                    def clear_form():
                        project_input.value = ''
                        status_input.value = ''
                        notes_input.value = ''
                        output_area.content = ''
                        ui.notify('Formulário limpo!')

                    recent_logs = list(reversed(data[-15:]))

                    ui.select(
                        options={i: f"{log['project']} | {log['status'][:30]}..." 
                                 for i, log in enumerate(recent_logs)},
                        label='Reciclar Log Recente',
                        on_change=lambda e: (
                            setattr(project_input, 'value', recent_logs[e.value]['project']),
                            setattr(status_input, 'value', recent_logs[e.value]['status']),
                            setattr(notes_input, 'value', recent_logs[e.value].get('notes', '')),
                            ui.notify('Contexto recuperado!')
                        ) if e.value is not None else None
                    ).classes('w-full mb-4').props('standout')

                    with ui.row().classes('w-full gap-2'):
                        def handle_save():
                            if not project_input.value or not status_input.value:
                                ui.notify('Preencha os campos obrigatórios!', type='warning')
                                return
                            
                            new_entry = {
                                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "project": project_input.value,
                                "status": status_input.value,
                                "notes": notes_input.value
                            }
                            data.append(new_entry)
                            save_data(data)
                            output_area.content = f"PROJECT: {new_entry['project']}\nSTATUS: {new_entry['status']}\nNOTES: {new_entry['notes']}"
                            ui.notify('Log salvo!', type='positive')
                            update_history_list()

                        ui.button('GERAR E SALVAR', icon='save', on_click=handle_save).classes('flex-grow bg-accent')
                        ui.button(icon='delete_sweep', on_click=clear_form).props('flat outline color=grey')

                with ui.card().classes('w-full mt-6 bg-slate-50 dark:bg-slate-900'):
                    output_area = ui.code('', language='markdown').classes('w-full h-32')
                    ui.button('COPIAR PARA O CHAT', icon='content_copy', 
                              on_click=lambda: ui.run_javascript(f'navigator.clipboard.writeText(`{output_area.content}`)')) \
                              .classes('w-full').props('flat')

        # --- PAINEL HISTÓRICO ---
        with ui.tab_panel(history_tab):
            with ui.column().classes('w-full max-w-3xl mx-auto'):
                search_box = ui.input(placeholder='Buscar...').classes('w-full mb-4').props('outlined rounded')
                history_list = ui.column().classes('w-full gap-3')

                def update_history_list():
                    history_list.clear()
                    term = search_box.value.lower()
                    for log in reversed(data):
                        if any(term in str(v).lower() for v in log.values()):
                            with history_list, ui.expansion(f"{log['timestamp']} | {log['project']}").classes('bg-white dark:bg-slate-800 border rounded-lg'):
                                ui.markdown(f"**Status:** {log['status']}\n\n**Notas:**\n{log.get('notes', '')}").classes('p-4')
                
                search_box.on('update:model-value', update_history_list)
                update_history_list()

# Inicia o app
ui.run(port=8080, reload=False, title="Timestamp Pro")