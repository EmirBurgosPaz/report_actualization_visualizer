import os

# ── Persistencia ──────────────────────────────────────────────────────────────

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "documentos_data.json")


C = {
    "bg":        "#1A1A1E",
    "sidebar":   "#141417",
    "panel":     "#22222A",
    "border":    "#2E2E38",
    "grid": "#1F1F26",
    "text":      "#E8E8EC",
    "muted":     "#7A7A8A",
    "accent":    "#7C6FE0",
    "accent_dk": "#5A4FBA",
    "accent_hover" : "#5599ff" ,
    "hover":     "#2A2A36",
    "row_alt":   "#1F1F26",
    "dlg_bg":    "#1E1E26",
    "dlg_input": "#2A2A36",
    "dlg_border":"#3A3A4A",
    "info_bg":   "#142336",
    "info_fg":   "#60A5FA",
    "disabled_fg": "#4D4D5C",
    "tag_teal":  "#2DD4BF",
    "tag_pink":  "#F472B6",
    "white" : "#FFFFFF",
    "splash_bg" : "#1F1F26",
    "tree_bg":   "#181825",   # fondo principal de la tabla
"tree_alt":  "#1e1e2e",   # fila alternada
"header_bg": "#313244",   # encabezados de columna
"select_bg": "#45475a",   # fila seleccionada
"entry_bg":  "#313244",   # fondo del campo de búsqueda
"fg_dim":    "#6c7086",  
"outdated": "#4a1c1c"  # rojo oscuro
}

KEYBOARD_KEYS = {
    "enter": "<Return>", 
    "escape": "<Escape>", 
    "space": "<space>", # ignorar
    "tab" : "<KeyPress-Tab>", # Ignorar 
}