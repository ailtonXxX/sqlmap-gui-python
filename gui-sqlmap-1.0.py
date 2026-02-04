import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import subprocess
import threading
import webbrowser

# ======================================================
# VARIÁVEIS GLOBAIS
# ======================================================
processo = None
tema_escuro = True
idioma_atual = "pt_br"

# ======================================================
# IDIOMAS
# ======================================================
idiomas = {
    "pt_br": {
        "nome": "Português (Brasil)",
        "titulo": "SQLMap GUI – Open Source",
        "url": "URL Alvo",
        "identificacao": "Identificação do Banco",
        "database": "Database",
        "tabela": "Tabela",
        "coluna": "Coluna",
        "enumeracao": "Enumeração",
        "extracao": "Extração de Dados",
        "avancado": "Configurações Avançadas",
        "executar": "Executar",
        "parar": "Parar",
        "sobre": "Sobre",
        "erro_url": "Informe a URL alvo.",
        "uso": "Projeto open source para fins educacionais e testes autorizados."
    },
    "en": {
        "nome": "English",
        "titulo": "SQLMap GUI – Open Source",
        "url": "Target URL",
        "identificacao": "Database Identification",
        "database": "Database",
        "tabela": "Table",
        "coluna": "Column",
        "enumeracao": "Enumeration",
        "extracao": "Data Extraction",
        "avancado": "Advanced Settings",
        "executar": "Run",
        "parar": "Stop",
        "sobre": "About",
        "erro_url": "Target URL is required.",
        "uso": "Open source project for educational and authorized testing."
    },
    "ru": {
        "nome": "Русский",
        "titulo": "SQLMap GUI – Открытый код",
        "url": "Целевой URL",
        "identificacao": "Идентификация БД",
        "database": "База данных",
        "tabela": "Таблица",
        "coluna": "Колонка",
        "enumeracao": "Перечисление",
        "extracao": "Извлечение данных",
        "avancado": "Дополнительные настройки",
        "executar": "Запустить",
        "parar": "Остановить",
        "sobre": "О системе",
        "erro_url": "Целевой URL обязателен.",
        "uso": "Проект с открытым исходным кодом для обучения."
    },
    "zh": {
        "nome": "中文",
        "titulo": "SQLMap GUI – 开源界面",
        "url": "目标 URL",
        "identificacao": "数据库识别",
        "database": "数据库",
        "tabela": "表",
        "coluna": "列",
        "enumeracao": "枚举",
        "extracao": "数据提取",
        "avancado": "高级设置",
        "executar": "运行",
        "parar": "停止",
        "sobre": "关于",
        "erro_url": "目标 URL 是必填项。",
        "uso": "用于学习和授权测试的开源项目。"
    },
    "vi": {
        "nome": "Tiếng Việt",
        "titulo": "SQLMap GUI – Giao diện mã nguồn mở",
        "url": "URL Mục tiêu",
        "identificacao": "Xác định cơ sở dữ liệu",
        "database": "Cơ sở dữ liệu",
        "tabela": "Bảng",
        "coluna": "Cột",
        "enumeracao": "Liệt kê",
        "extracao": "Trích xuất dữ liệu",
        "avancado": "Cài đặt nâng cao",
        "executar": "Chạy",
        "parar": "Dừng",
        "sobre": "Giới thiệu",
        "erro_url": "URL mục tiêu là bắt buộc.",
        "uso": "Dự án mã nguồn mở cho mục đích học tập."
    },
    "uk": {
        "nome": "Українська",
        "titulo": "SQLMap GUI – Відкритий код",
        "url": "Цільовий URL",
        "identificacao": "Ідентифікація БД",
        "database": "База даних",
        "tabela": "Таблиця",
        "coluna": "Стовпець",
        "enumeracao": "Перелік",
        "extracao": "Отримання даних",
        "avancado": "Розширені налаштування",
        "executar": "Запустити",
        "parar": "Зупинити",
        "sobre": "Про систему",
        "erro_url": "Цільовий URL є обовʼязковим.",
        "uso": "Проєкт з відкритим кодом."
    },
    "pt_pt": {
        "nome": "Português (Portugal)",
        "titulo": "SQLMap GUI – Open Source",
        "url": "URL Alvo",
        "identificacao": "Identificação da Base",
        "database": "Base de Dados",
        "tabela": "Tabela",
        "coluna": "Coluna",
        "enumeracao": "Enumeração",
        "extracao": "Extração de Dados",
        "avancado": "Configurações Avançadas",
        "executar": "Executar",
        "parar": "Parar",
        "sobre": "Sobre",
        "erro_url": "O URL alvo é obrigatório.",
        "uso": "Projeto open source."
    },
    "de": {
        "nome": "Deutsch",
        "titulo": "SQLMap GUI – Open-Source",
        "url": "Ziel-URL",
        "identificacao": "Datenbankidentifikation",
        "database": "Datenbank",
        "tabela": "Tabelle",
        "coluna": "Spalte",
        "enumeracao": "Aufzählung",
        "extracao": "Datenextraktion",
        "avancado": "Erweiterte Einstellungen",
        "executar": "Starten",
        "parar": "Stoppen",
        "sobre": "Über",
        "erro_url": "Ziel-URL ist erforderlich.",
        "uso": "Open-Source-Projekt."
    },
    "fr": {
        "nome": "Français",
        "titulo": "SQLMap GUI – Open Source",
        "url": "URL Cible",
        "identificacao": "Identification DB",
        "database": "Base de données",
        "tabela": "Table",
        "coluna": "Colonne",
        "enumeracao": "Énumération",
        "extracao": "Extraction de données",
        "avancado": "Paramètres Avancés",
        "executar": "Exécuter",
        "parar": "Arrêter",
        "sobre": "À propos",
        "erro_url": "L’URL cible est obligatoire.",
        "uso": "Projet open source."
    }
}

# ======================================================
# FUNÇÕES TEMA
# ======================================================
def aplicar_tema():
    style = ttk.Style(janela)
    style.theme_use("clam")
    if tema_escuro:
        bg, fg = "#1e1e1e", "#e6e6e6"
        entry_bg, out_bg, out_fg = "#2b2b2b", "#121212", "#00ff90"
    else:
        bg, fg = "#f2f2f2", "#000000"
        entry_bg, out_bg, out_fg = "#ffffff", "#ffffff", "#000000"

    janela.configure(bg=bg)
    style.configure(".", background=bg, foreground=fg, fieldbackground=entry_bg)
    style.configure("TLabel", background=bg, foreground=fg)
    style.configure("TButton", background=entry_bg, foreground=fg)
    style.configure("TEntry", fieldbackground=entry_bg)
    style.configure("TCheckbutton", background=bg, foreground=fg)
    style.configure("TLabelframe", background=bg, foreground=fg)
    style.configure("TLabelframe.Label", background=bg, foreground=fg)
    output.configure(bg=out_bg, fg=out_fg, insertbackground=fg)

def alternar_tema():
    global tema_escuro
    tema_escuro = not tema_escuro
    aplicar_tema()

# ======================================================
# FUNÇÕES IDIOMA
# ======================================================
def atualizar_textos():
    t = idiomas[idioma_atual]
    janela.title(t["titulo"])
    lbl_url.config(text=t["url"])
    frame_id.config(text=t["identificacao"])
    lbl_db.config(text=t["database"])
    lbl_tb.config(text=t["tabela"])
    lbl_col.config(text=t["coluna"])
    frame_enum.config(text=t["enumeracao"])
    frame_dump.config(text=t["extracao"])
    frame_adv.config(text=t["avancado"])
    btn_exec.config(text=t["executar"])
    btn_stop.config(text=t["parar"])
    btn_about.config(text=t["sobre"])

def mudar_idioma(event=None):
    global idioma_atual
    idioma_atual = idioma_map[combo_idioma.get()]
    atualizar_textos()

# ======================================================
# FUNÇÕES SQLMAP
# ======================================================
def executar_sqlmap():
    global processo
    url = entry_url.get().strip()
    if not url:
        messagebox.showerror("Erro", idiomas[idioma_atual]["erro_url"])
        return

    cmd = ["sqlmap", "-u", url, "--batch"]

    # Opções avançadas
    if var_dbs.get(): cmd.append("--dbs")
    if var_tables.get(): cmd.append("--tables")
    if var_columns.get(): cmd.append("--columns")
    if var_dump.get(): cmd.append("--dump")
    if var_dump_all.get(): cmd.append("--dump-all")
    if var_current_user.get(): cmd.append("--current-user")
    if var_current_db.get(): cmd.append("--current-db")
    if var_random_agent.get(): cmd.append("--random-agent")

    # Database / Table / Column
    if entry_db.get(): cmd += ["-D", entry_db.get()]
    if entry_table.get(): cmd += ["-T", entry_table.get()]
    if entry_column.get(): cmd += ["-C", entry_column.get()]

    # Risk / Level / Threads
    cmd += ["--risk", risk_var.get(), "--level", level_var.get(), "--threads", threads_var.get()]

    output.insert(tk.END, "\n▶ " + " ".join(cmd) + "\n\n")
    btn_exec.config(state="disabled")

    def run():
        global processo
        processo = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in processo.stdout:
            janela.after(0, lambda l=line: output.insert(tk.END, l))
        janela.after(0, lambda: btn_exec.config(state="normal"))

    threading.Thread(target=run, daemon=True).start()

def parar_sqlmap():
    global processo
    if processo:
        processo.kill()
        output.insert(tk.END, "\n⛔ Execução interrompida pelo usuário.\n")
        btn_exec.config(state="normal")

# ======================================================
# FUNÇÃO SOBRE
# ======================================================
def mostrar_sobre():
    w = tk.Toplevel(janela)
    w.title("Sobre")
    w.geometry("420x260")
    ttk.Label(w, text="SQLMap GUI", font=("Segoe UI", 16, "bold")).pack(pady=10)
    ttk.Label(w, text=idiomas[idioma_atual]["uso"], wraplength=400, justify="center").pack(pady=5)
    ttk.Separator(w).pack(fill="x", pady=10)
    ttk.Label(w, text="Open Source Project").pack(pady=3)
    ttk.Button(w, text="GitHub", command=lambda: webbrowser.open("https://github.com/")).pack(pady=3)
    ttk.Button(w, text="E-mail", command=lambda: webbrowser.open("ailton.martins.031227@gmail.com")).pack(pady=3)

# ======================================================
# INTERFACE
# ======================================================
janela = tk.Tk()
janela.geometry("1000x720")

# --- TOPO: Sobre, Tema, Idioma ---
frame_top = ttk.Frame(janela)
frame_top.pack(fill="x", padx=10, pady=5)

btn_about = ttk.Button(frame_top, command=mostrar_sobre)
btn_about.pack(side="right", padx=5)

ttk.Button(frame_top, text="🌙 / 🌞", command=alternar_tema).pack(side="right", padx=5)

idioma_map = {idiomas[k]["nome"]: k for k in idiomas}
combo_idioma = ttk.Combobox(frame_top, values=list(idioma_map.keys()), state="readonly", width=28)
combo_idioma.set(idiomas["pt_br"]["nome"])
combo_idioma.pack(side="right", padx=5)
combo_idioma.bind("<<ComboboxSelected>>", mudar_idioma)

# --- URL ---
lbl_url = ttk.Label(janela)
lbl_url.pack(anchor="w", padx=10)
entry_url = ttk.Entry(janela, width=120)
entry_url.pack(padx=10, pady=5)

# --- IDENTIFICAÇÃO ---
frame_id = ttk.LabelFrame(janela)
frame_id.pack(fill="x", padx=10)

lbl_db = ttk.Label(frame_id)
lbl_tb = ttk.Label(frame_id)
lbl_col = ttk.Label(frame_id)

entry_db = ttk.Entry(frame_id, width=25)
entry_table = ttk.Entry(frame_id, width=25)
entry_column = ttk.Entry(frame_id, width=25)

lbl_db.grid(row=0, column=0)
entry_db.grid(row=0, column=1, padx=5)
lbl_tb.grid(row=0, column=2)
entry_table.grid(row=0, column=3, padx=5)
lbl_col.grid(row=0, column=4)
entry_column.grid(row=0, column=5, padx=5)

# --- ENUMERAÇÃO ---
frame_enum = ttk.LabelFrame(janela)
frame_enum.pack(fill="x", padx=10, pady=5)

var_dbs = tk.BooleanVar()
var_tables = tk.BooleanVar()
var_columns = tk.BooleanVar()
var_current_user = tk.BooleanVar()
var_current_db = tk.BooleanVar()

ttk.Checkbutton(frame_enum, text="Databases", variable=var_dbs).grid(row=0, column=0, sticky="w")
ttk.Checkbutton(frame_enum, text="Tables", variable=var_tables).grid(row=0, column=1, sticky="w")
ttk.Checkbutton(frame_enum, text="Columns", variable=var_columns).grid(row=0, column=2, sticky="w")
ttk.Checkbutton(frame_enum, text="Current User", variable=var_current_user).grid(row=1, column=0, sticky="w")
ttk.Checkbutton(frame_enum, text="Current DB", variable=var_current_db).grid(row=1, column=1, sticky="w")

# --- EXTRAÇÃO ---
frame_dump = ttk.LabelFrame(janela)
frame_dump.pack(fill="x", padx=10, pady=5)

var_dump = tk.BooleanVar()
var_dump_all = tk.BooleanVar()

ttk.Checkbutton(frame_dump, text="Dump", variable=var_dump).pack(anchor="w")
ttk.Checkbutton(frame_dump, text="Dump All", variable=var_dump_all).pack(anchor="w")

# --- AVANÇADO ---
frame_adv = ttk.LabelFrame(janela)
frame_adv.pack(fill="x", padx=10, pady=5)

risk_var = tk.StringVar(value="1")
level_var = tk.StringVar(value="1")
threads_var = tk.StringVar(value="1")
var_random_agent = tk.BooleanVar()

ttk.Label(frame_adv, text="Risk").grid(row=0, column=0)
ttk.Entry(frame_adv, textvariable=risk_var, width=5).grid(row=0, column=1)
ttk.Label(frame_adv, text="Level").grid(row=0, column=2)
ttk.Entry(frame_adv, textvariable=level_var, width=5).grid(row=0, column=3)
ttk.Label(frame_adv, text="Threads").grid(row=0, column=4)
ttk.Entry(frame_adv, textvariable=threads_var, width=5).grid(row=0, column=5)
ttk.Checkbutton(frame_adv, text="Random Agent", variable=var_random_agent).grid(row=1, column=0, sticky="w")

# --- BOTÕES ---
frame_btn = ttk.Frame(janela)
frame_btn.pack(pady=10)

btn_exec = ttk.Button(frame_btn, command=executar_sqlmap)
btn_stop = ttk.Button(frame_btn, command=parar_sqlmap)

btn_exec.grid(row=0, column=0, padx=5)
btn_stop.grid(row=0, column=1, padx=5)

# --- OUTPUT ---
output = scrolledtext.ScrolledText(janela, height=18)
output.pack(fill="both", padx=10, pady=5)

# --- APLICAR TEMA E IDIOMA ---
aplicar_tema()
atualizar_textos()

janela.mainloop()
