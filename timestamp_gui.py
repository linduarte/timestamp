import json
# import asyncio
from pathlib import Path
from datetime import datetime
from nicegui import ui

# --- CONFIGURAÇÕES ---
BASE_DIR = Path(__file__).resolve().parent
FILE_PATH = BASE_DIR / "dev_history.json"

def load_data():
    if not FILE_PATH.exists() or FILE_PATH.stat().st_size == 0:
        return []
    try:
        with FILE_PATH.open("r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, Exception) as e:
        print(f"Erro ao carregar JSON: {e}")
        return []

def save_data(data):
    with FILE_PATH.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# --- INTERFACE ---
@ui.page('/')
def main_page():
    data = load_data()
    
    # Configuração de Cores (Paleta Profissional)
    ui.colors(primary='#1e293b', secondary='#64748b', accent='#10b981')

    # Header com Relógio em Tempo Real
    with ui.header().classes('items-center justify-between px-6 bg-primary shadow-md'):
        ui.label('TIMESTAMP PRO').classes('text-xl font-black tracking-tighter text-white')
        with ui.row().classes('items-center gap-4'):
            ui.button(icon='dark_mode', on_click=lambda: ui.dark_mode().toggle()).props('flat color=white')
            # Relógio que mostra data e hora no topo
            clock_label = ui.label().classes('font-mono text-sm text-white')
            ui.timer(1.0, lambda: clock_label.set_text(datetime.now().strftime("%d/%m/%Y %H:%M:%S")))

    with ui.tabs().classes('w-full') as tabs:
        editor_tab = ui.tab('EDITOR', icon='add_box')
        history_tab = ui.tab('HISTÓRICO', icon='format_list_bulleted')

    with ui.tab_panels(tabs, value=editor_tab).classes('w-full bg-transparent p-4'):
        
        # --- PAINEL EDITOR ---
        with ui.tab_panel(editor_tab):
            with ui.column().classes('w-full max-w-3xl mx-auto'):
                with ui.card().classes('w-full p-6 shadow-xl border-t-4 border-accent'):
                    ui.label('Nova Sessão de Trabalho').classes('text-2xl font-bold mb-4')
                    
                    project_input = ui.input('Projeto / Cliente').classes('w-full')
                    status_input = ui.input('O que vamos fazer? (Status)').classes('w-full')
                    notes_input = ui.textarea('Notas e Detalhes Técnicos').classes('w-full h-40').props('outlined')

                    # Função para carregar contexto antigo
                    recent_logs = list(reversed(data[-15:]))
                    ui.select(
                        options={i: f"{log['project']} | {log['status'][:30]}..." for i, log in enumerate(recent_logs)},
                        label='Recuperar Contexto Recente',
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
                                ui.notify('Campos obrigatórios vazios!', type='warning')
                                return
                            
                            # Gerando o carimbo de tempo formatado
                            now = datetime.now()
                            ts_display = now.strftime("%d/%m/%Y %H:%M:%S")
                            
                            new_entry = {
                                "timestamp": ts_display,
                                "project": project_input.value.upper(),
                                "status": status_input.value,
                                "notes": notes_input.value
                            }
                            
                            data.append(new_entry)
                            save_data(data)
                            
                            # Atualizando a área de saída com DATA e HORA inclusas
                            output_area.content = (
                                f"🕒 **REGISTRO:** {ts_display}\n"
                                f"📁 **PROJETO:** {new_entry['project']}\n"
                                f"✅ **STATUS:** {new_entry['status']}\n"
                                f"📝 **NOTAS:** {new_entry['notes']}"
                            )
                            ui.notify('Sessão registrada!', type='positive')
                            update_history_list()

                        ui.button('GERAR E SALVAR', icon='save', on_click=handle_save).classes('flex-grow bg-accent shadow-lg')
                        ui.button(icon='delete_sweep', on_click=lambda: [setattr(project_input, 'value', ''), setattr(status_input, 'value', ''), setattr(notes_input, 'value', ''), ui.notify('Limpo!')]).props('flat color=grey')

                # Área de Visualização e Cópia
                with ui.card().classes('w-full mt-6 bg-slate-50 dark:bg-slate-900 border-dashed border-2'):
                    output_area = ui.code('Os dados formatados aparecerão aqui...', language='markdown').classes('w-full h-auto min-h-[100px]')
                    ui.button('COPIAR PARA O CHAT', icon='content_copy', 
                              on_click=lambda: ui.run_javascript(f'navigator.clipboard.writeText(`{output_area.content}`)')) \
                              .classes('w-full py-4').props('elevated color=primary')

        # --- PAINEL HISTÓRICO ---
        with ui.tab_panel(history_tab):
            with ui.column().classes('w-full max-w-3xl mx-auto'):
                search_box = ui.input(placeholder='Filtrar histórico...').classes('w-full mb-4').props('outlined rounded icon=search')
                history_list = ui.column().classes('w-full gap-3')

                def update_history_list():
                    history_list.clear()
                    term = search_box.value.lower()
                    # Mostra os logs mais recentes primeiro
                    for log in reversed(data):
                        if any(term in str(v).lower() for v in log.values()):
                            with history_list, ui.expansion(f"{log['timestamp']} | {log['project']}").classes('bg-white dark:bg-slate-800 border rounded-lg shadow-sm'):
                                with ui.column().classes('p-4 w-full'):
                                    ui.markdown(f"**Status:** {log['status']}")
                                    if log.get('notes'):
                                        ui.separator().classes('my-2')
                                        ui.markdown(f"**Notas:**\n{log['notes']}")
                
                search_box.on('update:model-value', update_history_list)
                update_history_list()

# Inicia o app
ui.run(port=8080, reload=False, title="Timestamp Pro")