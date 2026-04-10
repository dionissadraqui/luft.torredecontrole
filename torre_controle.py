import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np
import streamlit as st
import base64

#  >    executar  >   python -m streamlit run torre_controle.py  

# =====================================================
# CONFIGURAÇÕES DE CORES E ESTILOS - CENTRALIZADAS
# =====================================================

CORES_STATUS = {
    "MANUTENÇÃO": "#ff3c00",
    "DISPONÍVEIS NÃO TRIPULADO": "#4caf50",
    "CARREGADO": "#ff9800",
    "RETORNANDO DISPONÍVEIS": "#2196f3",
    "DISPONÍVEIS TRIPULADO": "#0aec0a",
    "APOIO FILIAL": '#ffffff',
    "INDISPONÍVEIS": "#94a3b8",
    "FORA DE OPERAÇÃO": "#64748b",
    "RETORNANDO INDISPONÍVEIS": "#cbd5e1"
}

CORES_KPI = {
    "TOTAL": {"border": "#29b6f6", "text": "#29b6f6", "shadow": "rgba(41, 182, 246, 0.75)"},
    "OPERACAO": {"border": "#ffb300", "text": "#ffb300", "shadow": "rgba(255, 179, 0, 0.75)"},
    "DISPONIVEIS": {"border": "#00e676", "text": "#00e676", "shadow": "rgba(0, 230, 118, 0.75)"},
    "MANUTENCAO": {"border": "#ff3d00", "text": "#ff3d00", "shadow": "rgba(255, 61, 0, 0.75)"}
}

CORES_TIPO_VEICULO = ['#00d4ff', '#ff6b00', '#00ff88', '#ffcc00', '#ff2d55', '#bf5fff']
CORES_POSICAO      = ['#00d4ff', '#ff6b00', '#ffcc00', '#00ff88', '#bf5fff', '#ff2d55',
                      '#00ffea', '#ff9500', '#b8ff3c', '#ff3caa']
CORES_UF           = ['#00ff88', '#00d4ff', '#ffcc00', '#ff6b00', '#bf5fff', '#ff2d55',
                      '#b8ff3c', '#00ffea']

CORES_HEADER = {
    "background": "#252525", "border": "#ffffff",
    "title": "#ffffff", "subtitle": "#888", "dot": "#4caf50"
}

CORES_SIRENE = {
    "base_top": "#666", "base_bottom": "#333",
    "light_top": "#ff5722", "light_bottom": "#d32f2f",
    "light_glow": "rgba(255, 87, 34, 0.8)",
    "light_top_alt": "#ff9800", "light_bottom_alt": "#ff5722",
    "light_glow_alt": "rgba(255, 152, 0, 1)",
    "beam": "rgba(255, 87, 34, 0.3)"
}

CORES_DISPONIBILIDADE = {
    "background_start": "#000000", "background_end": "#000000",
    "border": "#2e5a2e", "label": "#000000fa",
    "valor": "#000000", "subtitle": "#000000"
}

CORES_INTERFACE = {
    "fundo_gradiente_start": "#141414", "fundo_gradiente_end": "#0a0a0a",
    "painel_background": "#1a1a1a", "painel_border": "#484848",
    "sidebar_background": "#111111", "sidebar_border": "#484848",
    "texto_principal": "#f5f5f5", "texto_secundario": "#bbbbbb",
    "grid": "#3a3a3a", "botao_primary": "#2196f3", "botao_hover": "#1976d2",
    "tabela_header_bg": "#111111", "tabela_row_bg": "#1a1a1a",
    "tabela_row_hover": "#252525"
}

# =====================================================
# CONFIGURAÇÃO DA PÁGINA
# =====================================================
st.set_page_config(
    page_title="TORRE DE CONTROLE | FROTA AGRO",
    layout="wide",
    page_icon="🚛",
    initial_sidebar_state="expanded"
)

def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return None

def show_loading_screen(placeholder):
    img_base64 = get_base64_image("luft.png")
    if img_base64:
        loading_html = f"""
        <style>
        .loading-overlay {{
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            background-color: #1a1a1a; display: flex; flex-direction: column;
            justify-content: center; align-items: center; z-index: 9999;
        }}
        .loading-image {{
            max-width: 80vw; max-height: 80vh; object-fit: contain;
            animation: pulse 2s ease-in-out infinite;
        }}
        .loading-text {{
            color: #ffffff; font-size: 24px; font-weight: 700;
            margin-top: 30px; text-align: center;
            animation: blink 1.5s ease-in-out infinite;
        }}
        @keyframes pulse {{ 0%, 100% {{ opacity: 0.8; transform: scale(1); }} 50% {{ opacity: 1; transform: scale(1.05); }} }}
        @keyframes blink {{ 0%, 100% {{ opacity: 0.5; }} 50% {{ opacity: 1; }} }}
        </style>
        <div class="loading-overlay">
            <img src="data:image/png;base64,{img_base64}" class="loading-image" alt="Loading">
            <div class="loading-text">CARREGANDO DADOS...</div>
        </div>
        """
    else:
        loading_html = """
        <style>
        .loading-overlay {
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            background-color: #1a1a1a; display: flex; flex-direction: column;
            justify-content: center; align-items: center; z-index: 9999;
        }
        .loading-text {
            color: #ffffff; font-size: 32px; font-weight: 700;
            text-align: center; animation: blink 1.5s ease-in-out infinite;
        }
        @keyframes blink { 0%, 100% { opacity: 0.5; } 50% { opacity: 1; } }
        </style>
        <div class="loading-overlay"><div class="loading-text">🚛 CARREGANDO DADOS...</div></div>
        """
    placeholder.markdown(loading_html, unsafe_allow_html=True)

# =====================================================
# CSS CUSTOMIZADO
# =====================================================
def load_custom_css():
    st.markdown(f"""
    <style>
    * {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important; }}
    header[data-testid="stHeader"] {{ background-color: rgba(0,0,0,0) !important; backdrop-filter: none !important; }}
    header[data-testid="stHeader"] > div:first-child {{ background-color: transparent !important; }}
    button[kind="header"] {{ color: white !important; }}
    .main .block-container {{ padding-top: 2rem !important; }}
    .stApp {{ background: linear-gradient(135deg, {CORES_INTERFACE["fundo_gradiente_start"]} 0%, {CORES_INTERFACE["fundo_gradiente_end"]} 100%) !important; }}
    .block-container {{ padding-top: 1.5rem !important; padding-bottom: 1rem !important; padding-left: 2rem !important; padding-right: 2rem !important; }}
    div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlockBorderWrapper"] {{
        background-color: {CORES_INTERFACE["painel_background"]} !important;
        border: 1px solid {CORES_INTERFACE["painel_border"]} !important;
        border-radius: 10px !important; padding: 25px !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.6) !important;
    }}
    .card-title {{
        font-weight: 800; font-size: 1.25rem; color: {CORES_INTERFACE["texto_principal"]} !important;
        text-transform: uppercase; margin-bottom: 20px; letter-spacing: 1.5px;
        display: flex; align-items: center; gap: 10px;
        text-shadow: 0 0 10px rgba(255,255,255,0.12);
    }}
    .kpi-card {{
        background-color: {CORES_INTERFACE["painel_background"]}; border-radius: 12px;
        padding: 25px 15px 15px 15px; text-align: center; width: 100%; box-sizing: border-box;
    }}
    .kpi-card .kpi-label {{
        font-size: 1.15rem; font-weight: 800; text-transform: uppercase;
        letter-spacing: 1.8px; margin-bottom: 10px;
    }}
    .kpi-card .kpi-value {{
        font-size: 3.2rem; font-weight: 900; line-height: 1.1;
        margin-bottom: 12px; letter-spacing: -1px;
    }}
    .kpi-azul {{
        border: 2px solid {CORES_KPI["TOTAL"]["border"]};
        box-shadow: 0 0 22px {CORES_KPI["TOTAL"]["shadow"]}, 0 0 6px {CORES_KPI["TOTAL"]["border"]}, 0 4px 20px rgba(0,0,0,0.5);
    }}
    .kpi-azul .kpi-label {{ color: {CORES_KPI["TOTAL"]["text"]}; text-shadow: 0 0 10px {CORES_KPI["TOTAL"]["shadow"]}; }}
    .kpi-azul .kpi-value {{ color: {CORES_KPI["TOTAL"]["text"]}; text-shadow: 0 0 18px {CORES_KPI["TOTAL"]["shadow"]}; }}
    .kpi-laranja {{
        border: 2px solid {CORES_KPI["OPERACAO"]["border"]};
        box-shadow: 0 0 22px {CORES_KPI["OPERACAO"]["shadow"]}, 0 0 6px {CORES_KPI["OPERACAO"]["border"]}, 0 4px 20px rgba(0,0,0,0.5);
    }}
    .kpi-laranja .kpi-label {{ color: {CORES_KPI["OPERACAO"]["text"]}; text-shadow: 0 0 10px {CORES_KPI["OPERACAO"]["shadow"]}; }}
    .kpi-laranja .kpi-value {{ color: {CORES_KPI["OPERACAO"]["text"]}; text-shadow: 0 0 18px {CORES_KPI["OPERACAO"]["shadow"]}; }}
    .kpi-verde {{
        border: 2px solid {CORES_KPI["DISPONIVEIS"]["border"]};
        box-shadow: 0 0 22px {CORES_KPI["DISPONIVEIS"]["shadow"]}, 0 0 6px {CORES_KPI["DISPONIVEIS"]["border"]}, 0 4px 20px rgba(0,0,0,0.5);
    }}
    .kpi-verde .kpi-label {{ color: {CORES_KPI["DISPONIVEIS"]["text"]}; text-shadow: 0 0 10px {CORES_KPI["DISPONIVEIS"]["shadow"]}; }}
    .kpi-verde .kpi-value {{ color: {CORES_KPI["DISPONIVEIS"]["text"]}; text-shadow: 0 0 18px {CORES_KPI["DISPONIVEIS"]["shadow"]}; }}
    .kpi-vermelho {{
        border: 2px solid {CORES_KPI["MANUTENCAO"]["border"]};
        box-shadow: 0 0 22px {CORES_KPI["MANUTENCAO"]["shadow"]}, 0 0 6px {CORES_KPI["MANUTENCAO"]["border"]}, 0 4px 20px rgba(0,0,0,0.5);
    }}
    .kpi-vermelho .kpi-label {{ color: {CORES_KPI["MANUTENCAO"]["text"]}; text-shadow: 0 0 10px {CORES_KPI["MANUTENCAO"]["shadow"]}; }}
    .kpi-vermelho .kpi-value {{ color: {CORES_KPI["MANUTENCAO"]["text"]}; text-shadow: 0 0 18px {CORES_KPI["MANUTENCAO"]["shadow"]}; }}
    .kpi-btn-azul button {{
        background-color: transparent !important; color: {CORES_KPI["TOTAL"]["text"]} !important;
        border: 1px solid {CORES_KPI["TOTAL"]["border"]} !important; border-radius: 5px !important;
        font-size: 0.72rem !important; font-weight: 700 !important; padding: 4px 10px !important;
        letter-spacing: 0.8px !important; width: 100% !important; transition: all 0.2s !important;
    }}
    .kpi-btn-azul button:hover {{ background-color: #cc0000 !important; color: white !important; border: 1px solid #ffffff !important; box-shadow: 0 0 12px #ffffff, 0 0 24px rgba(255,0,0,0.8) !important; }}
    .kpi-btn-laranja button {{
        background-color: transparent !important; color: {CORES_KPI["OPERACAO"]["text"]} !important;
        border: 1px solid {CORES_KPI["OPERACAO"]["border"]} !important; border-radius: 5px !important;
        font-size: 0.72rem !important; font-weight: 700 !important; padding: 4px 10px !important;
        letter-spacing: 0.8px !important; width: 100% !important; transition: all 0.2s !important;
    }}
    .kpi-btn-laranja button:hover {{ background-color: #cc0000 !important; color: white !important; border: 1px solid #ffffff !important; box-shadow: 0 0 12px #ffffff, 0 0 24px rgba(255,0,0,0.8) !important; }}
    .kpi-btn-verde button {{
        background-color: transparent !important; color: {CORES_KPI["DISPONIVEIS"]["text"]} !important;
        border: 1px solid {CORES_KPI["DISPONIVEIS"]["border"]} !important; border-radius: 5px !important;
        font-size: 0.72rem !important; font-weight: 700 !important; padding: 4px 10px !important;
        letter-spacing: 0.8px !important; width: 100% !important; transition: all 0.2s !important;
    }}
    .kpi-btn-verde button:hover {{ background-color: #cc0000 !important; color: white !important; border: 1px solid #ffffff !important; box-shadow: 0 0 12px #ffffff, 0 0 24px rgba(255,0,0,0.8) !important; }}
    .kpi-btn-vermelho button {{
        background-color: transparent !important; color: {CORES_KPI["MANUTENCAO"]["text"]} !important;
        border: 1px solid {CORES_KPI["MANUTENCAO"]["border"]} !important; border-radius: 5px !important;
        font-size: 0.72rem !important; font-weight: 700 !important; padding: 4px 10px !important;
        letter-spacing: 0.8px !important; width: 100% !important; transition: all 0.2s !important;
    }}
    .kpi-btn-vermelho button:hover {{ background-color: #cc0000 !important; color: white !important; border: 1px solid #ffffff !important; box-shadow: 0 0 12px #ffffff, 0 0 24px rgba(255,0,0,0.8) !important; }}
    /* ====== DIALOG — estilos base ====== */
    div[role="dialog"] > div {{
        max-width: 92vw !important;
        width: 92vw !important;
        max-height: 90vh !important;
        padding: clamp(16px, 3vw, 36px) clamp(14px, 3vw, 40px) !important;
        border-radius: 14px !important;
        overflow-y: auto !important;
        box-sizing: border-box !important;
    }}

    [data-testid="stDialog"], [data-testid="stDialog"] > div, div[role="dialog"],
    div[role="dialog"] > div, div[role="dialog"] > div > div,
    div[role="dialog"] section, div[role="dialog"] [data-testid="stVerticalBlock"] {{
        background-color: #1e1e1e !important; color: #ffffff !important;
    }}
    div[role="dialog"] p, div[role="dialog"] span, div[role="dialog"] label,
    div[role="dialog"] div, div[role="dialog"] h1, div[role="dialog"] h2,
    div[role="dialog"] h3, div[role="dialog"] small {{ color: #ffffff !important; }}
    div[role="dialog"] input, div[role="dialog"] textarea, div[role="dialog"] select {{
        background-color: #2a2a2a !important; color: #ffffff !important; border-color: #444 !important;
    }}
    div[role="dialog"] [data-baseweb="select"] > div {{
        background-color: #2a2a2a !important; color: #ffffff !important; border-color: #444 !important;
    }}
    div[role="dialog"] [data-testid="stCaptionContainer"] * {{ color: #aaaaaa !important; font-size: 0.85rem !important; }}
    div[role="dialog"] ::-webkit-scrollbar {{ width: 6px; }}
    div[role="dialog"] ::-webkit-scrollbar-track {{ background: #1a1a1a; }}
    div[role="dialog"] ::-webkit-scrollbar-thumb {{ background: #555; border-radius: 3px; }}
    div[role="dialog"] hr {{ border-color: #444 !important; }}

    /* ====== BOTÃO X (fechar dialog) — vermelho visível ====== */
    div[role="dialog"] button[aria-label="Close"],
    div[role="dialog"] button[aria-label="Fechar"],
    div[role="dialog"] button[aria-label="close"],
    div[role="dialog"] button[aria-label="fechar"],
    div[role="dialog"] [data-testid="stBaseButton-headerNoPadding"],
    div[role="dialog"] button[data-testid="stBaseButton-headerNoPadding"] {{
        background: #c62828 !important;
        background-color: #c62828 !important;
        border-radius: 6px !important;
        border: 2px solid #ef5350 !important;
        box-shadow: 0 0 12px rgba(198,40,40,0.9) !important;
        opacity: 1 !important;
        width: 32px !important;
        height: 32px !important;
        min-width: 32px !important;
        padding: 0 !important;
        color: #ffffff !important;
    }}
    div[role="dialog"] button[aria-label="Close"]:hover,
    div[role="dialog"] button[aria-label="Fechar"]:hover,
    div[role="dialog"] button[aria-label="close"]:hover,
    div[role="dialog"] button[aria-label="fechar"]:hover,
    div[role="dialog"] [data-testid="stBaseButton-headerNoPadding"]:hover,
    div[role="dialog"] button[data-testid="stBaseButton-headerNoPadding"]:hover {{
        background: #c62828 !important;
        background-color: #c62828 !important;
        box-shadow: 0 0 30px rgba(239,83,80,1), 0 0 10px rgba(255,100,100,1) !important;
        opacity: 1 !important;
    }}
    div[role="dialog"] button[aria-label="Close"] svg,
    div[role="dialog"] button[aria-label="Fechar"] svg,
    div[role="dialog"] [data-testid="stBaseButton-headerNoPadding"] svg,
    div[role="dialog"] button[data-testid="stBaseButton-headerNoPadding"] svg {{
        color: #ffffff !important;
        fill: #ffffff !important;
        stroke: #ffffff !important;
    }}

    /* ====== MINI CARDS — responsivos por tamanho de tela ====== */
    .mini-card-veiculo {{
        border-radius: 10px;
        padding: clamp(8px, 1.5vw, 14px) clamp(8px, 1.5vw, 12px);
        margin-bottom: 0; box-sizing: border-box; width: 100%;
    }}
    .mini-card-placa {{
        font-size: clamp(0.85rem, 1.5vw, 1.1rem);
        font-weight: 900; letter-spacing: 2px; font-family: monospace;
        display: block; margin-bottom: 5px;
    }}
    .mini-card-status-badge {{
        font-size: clamp(0.5rem, 0.9vw, 0.62rem);
        font-weight: 800; text-transform: uppercase; letter-spacing: 0.8px;
        padding: 3px 8px; border-radius: 20px; display: inline-block;
        margin-bottom: 5px; line-height: 1.4;
    }}
    .mini-card-motorista {{
        font-size: clamp(0.62rem, 1vw, 0.78rem);
        font-weight: 600; color: #cccccc !important;
        white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
        display: block; margin-top: 2px;
    }}

    /* ====== MEDIA QUERIES — breakpoints responsivos ====== */
    /* Telas grandes (>1400px): 5 colunas */
    @media (min-width: 1400px) {{
        div[role="dialog"] > div {{
            padding: 36px 48px !important;
        }}
    }}
    /* Tablets (600–900px): 2 colunas */
    @media (max-width: 900px) {{
        [data-testid="stDialog"] > div,
        div[role="dialog"] > div {{
            max-width: 99vw !important;
            width: 99vw !important;
            padding: 16px 12px !important;
        }}
    }}
    /* Mobile (<600px): 1 coluna, fonte menor */
    @media (max-width: 600px) {{
        [data-testid="stDialog"] > div,
        div[role="dialog"] > div {{
            max-width: 100vw !important;
            width: 100vw !important;
            max-height: 100vh !important;
            border-radius: 0 !important;
            padding: 12px 8px !important;
        }}
        .mini-card-placa {{ font-size: 0.9rem !important; letter-spacing: 1px !important; }}
    }}
    .mini-card-expand-btn button {{
        background-color: transparent !important; color: #ffffff !important;
        border: 1px solid rgba(255,255,255,0.25) !important; border-radius: 5px !important;
        font-size: 0.65rem !important; font-weight: 700 !important; padding: 2px 8px !important;
        letter-spacing: 0.5px !important; width: 100% !important; transition: all 0.2s !important; margin-top: 0 !important;
    }}
    .mini-card-expand-btn button:hover {{ background-color: #cc0000 !important; border: 1px solid #ffffff !important; box-shadow: 0 0 12px #ffffff, 0 0 24px rgba(255,0,0,0.8) !important; color: white !important; }}
    .btn-voltar button {{
        background-color: #2a2a2a !important; color: #ffffff !important;
        border: 1px solid #555 !important; border-radius: 8px !important;
        font-size: 0.8rem !important; font-weight: 700 !important;
        letter-spacing: 0.5px !important; transition: all 0.2s !important;
    }}
    .btn-voltar button:hover {{ background-color: #cc0000 !important; border: 1px solid #ffffff !important; box-shadow: 0 0 12px #ffffff, 0 0 24px rgba(255,0,0,0.8) !important; color: white !important; }}
    .card-veiculo {{ border-radius: 12px; padding: 18px 16px; margin-bottom: 14px; box-sizing: border-box; width: 100%; }}
    .card-header {{ display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 10px; }}
    .card-placa-row {{ display: flex; flex-wrap: wrap; align-items: center; gap: 10px; min-width: 0; }}
    .card-placa {{ font-size: clamp(1.05rem, 3.5vw, 1.4rem); font-weight: 900; letter-spacing: 2px; font-family: monospace; white-space: nowrap; }}
    .card-tipo {{ font-size: 0.82rem; font-weight: 600; padding: 3px 10px; border-radius: 20px; white-space: nowrap; }}
    .card-badge {{ font-size: 0.68rem; font-weight: 800; text-transform: uppercase; letter-spacing: 1px; padding: 5px 12px; border-radius: 20px; white-space: nowrap; flex-shrink: 0; }}
    .card-divider {{ border: none; border-top: 1px solid; margin: 12px 0 10px 0; opacity: 0.4; }}
    .card-info-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(min(100%, 155px), 1fr)); gap: 8px; }}
    .card-info-item {{ display: flex; flex-direction: column; gap: 3px; padding: 8px 10px; border-radius: 7px; min-width: 0; word-break: break-word; }}
    .card-info-label {{ font-size: 0.6rem; text-transform: uppercase; letter-spacing: 0.9px; font-weight: 700; opacity: 0.85; }}
    .card-info-value {{ color: #ffffff !important; font-size: 0.9rem; font-weight: 600; line-height: 1.3; }}
    @media (max-width: 520px) {{
        .card-header {{ flex-direction: column; align-items: flex-start; }}
        .card-info-grid {{ grid-template-columns: 1fr 1fr; }}
        .card-placa {{ font-size: 1rem; letter-spacing: 1.5px; }}
    }}
    .main-header {{
        background-color: {CORES_HEADER["background"]}; padding: 25px 30px; border-radius: 10px;
        border: 3px solid {CORES_HEADER["border"]}; margin-bottom: 25px;
        box-shadow: 0 0 12px rgba(255, 255, 255, 0.4), 0 4px 15px rgba(0, 0, 0, 0.3);
        display: flex; align-items: center; gap: 20px;
    }}
    .main-header h1 {{ color: {CORES_HEADER["title"]}; font-size: 2rem; font-weight: 800; margin: 0; margin-bottom: 8px; letter-spacing: 0.5px; text-align: center; }}
    .main-header p {{ color: {CORES_HEADER["subtitle"]}; font-size: 0.9rem; margin: 0; }}
    .header-left {{ display: flex; align-items: center; padding-left: 15px; min-width: 220px; }}
    .header-center {{ flex: 1; display: flex; align-items: center; justify-content: center; }}
    .header-logo {{ max-height: 120px; max-width: 750px; width: 95%; height: auto; object-fit: contain; margin: 0; display: block; filter: drop-shadow(0 2px 8px rgba(255, 255, 255, 0.2)); transition: all 0.3s ease; }}
    .header-logo:hover {{ filter: drop-shadow(0 4px 12px rgba(255, 255, 255, 0.4)); transform: scale(1.02); }}
    .header-logo-placeholder {{ font-size: 1.8rem; font-weight: 800; color: {CORES_HEADER["title"]}; margin-bottom: 8px; letter-spacing: 1px; }}
    .mini-disponibilidade {{
        background: linear-gradient(135deg, {CORES_DISPONIBILIDADE["background_start"]} 0%, {CORES_DISPONIBILIDADE["background_end"]} 100%);
        border: 1px solid {CORES_DISPONIBILIDADE["border"]}; border-radius: 10px; padding: 18px 28px;
        text-align: center; flex-shrink: 0; min-width: 170px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255,255,255,0.05);
    }}
    .mini-disponibilidade .mini-label {{ font-size: 0.65rem; font-weight: 700; color: {CORES_DISPONIBILIDADE["label"]}; text-transform: uppercase; letter-spacing: 1.2px; margin-bottom: 6px; }}
    .mini-disponibilidade .mini-valor {{ font-size: 3rem; font-weight: 700; color: {CORES_DISPONIBILIDADE["valor"]}; line-height: 1.1; margin: 0; }}
    .mini-disponibilidade .mini-sub {{ font-size: 0.62rem; color: {CORES_DISPONIBILIDADE["subtitle"]}; text-transform: uppercase; letter-spacing: 0.8px; margin-top: 4px; }}
    .mini-disponibilidade .mini-icon {{ font-size: 0.8rem; margin-bottom: 2px; }}
    .sirene-container {{ position: relative; width: 60px; height: 60px; flex-shrink: 0; }}
    .sirene-base {{ position: absolute; bottom: 0; left: 50%; transform: translateX(-50%); width: 50px; height: 15px; background: linear-gradient(180deg, {CORES_SIRENE["base_top"]} 0%, {CORES_SIRENE["base_bottom"]} 100%); border-radius: 0 0 8px 8px; }}
    .sirene-light {{ position: absolute; top: 5px; left: 50%; transform: translateX(-50%); width: 40px; height: 35px; background: linear-gradient(180deg, {CORES_SIRENE["light_top"]} 0%, {CORES_SIRENE["light_bottom"]} 100%); border-radius: 50% 50% 20% 20%; box-shadow: 0 0 20px {CORES_SIRENE["light_glow"]}; animation: giroflex 1s infinite; }}
    .sirene-light::before {{ content: ''; position: absolute; top: 5px; left: 5px; width: 30px; height: 25px; background: linear-gradient(135deg, rgba(255, 255, 255, 0.3) 0%, transparent 100%); border-radius: 50% 50% 20% 20%; }}
    .sirene-beam {{ position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 0; height: 0; border-left: 60px solid transparent; border-right: 60px solid transparent; border-top: 40px solid {CORES_SIRENE["beam"]}; animation: beam-rotate 1s infinite; transform-origin: 50% 0%; }}
    @keyframes giroflex {{
        0%, 100% {{ background: linear-gradient(180deg, {CORES_SIRENE["light_top"]} 0%, {CORES_SIRENE["light_bottom"]} 100%); box-shadow: 0 0 20px {CORES_SIRENE["light_glow"]}; }}
        50% {{ background: linear-gradient(180deg, {CORES_SIRENE["light_top_alt"]} 0%, {CORES_SIRENE["light_bottom_alt"]} 100%); box-shadow: 0 0 40px {CORES_SIRENE["light_glow_alt"]}, 0 0 60px rgba(255, 87, 34, 0.6); }}
    }}
    @keyframes beam-rotate {{
        0% {{ transform: translate(-50%, -50%) rotate(0deg); opacity: 0.3; }}
        50% {{ opacity: 0.6; }}
        100% {{ transform: translate(-50%, -50%) rotate(360deg); opacity: 0.3; }}
    }}
    .status-dot {{ display: inline-block; width: 8px; height: 8px; background-color: {CORES_HEADER["dot"]}; border-radius: 50%; margin-right: 8px; animation: pulse 2s infinite; }}
    @keyframes pulse {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.5; }} }}
    .dataframe {{ font-size: 0.85rem !important; color: {CORES_INTERFACE["texto_principal"]} !important; }}
    .dataframe thead tr th {{ background-color: {CORES_INTERFACE["tabela_header_bg"]} !important; color: {CORES_INTERFACE["texto_secundario"]} !important; font-weight: 600 !important; text-transform: uppercase !important; font-size: 0.7rem !important; letter-spacing: 0.5px !important; border-bottom: 1px solid {CORES_INTERFACE["painel_border"]} !important; }}
    .dataframe tbody tr td {{ background-color: {CORES_INTERFACE["tabela_row_bg"]} !important; color: {CORES_INTERFACE["texto_principal"]} !important; border-bottom: 1px solid {CORES_INTERFACE["painel_border"]} !important; }}
    .dataframe tbody tr:hover td {{ background-color: {CORES_INTERFACE["tabela_row_hover"]} !important; }}
    .js-plotly-plot {{ background-color: transparent !important; }}
    /* ====== TOOLTIP — fundo escuro, texto branco ====== */
    div[data-testid="stTooltipContent"],
    div[data-testid="stTooltipContent"] p,
    [data-testid="stTooltipContent"] * {{
        background-color: #1a1a1a !important;
        color: #ffffff !important;
    }}
    [class^="stTooltipContent"],
    [class*=" stTooltipContent"] {{
        background-color: #1a1a1a !important;
        color: #ffffff !important;
        border: 1px solid #555 !important;
    }}
    section[data-testid="stSidebar"] {{ background-color: {CORES_INTERFACE["sidebar_background"]} !important; border-right: 1px solid {CORES_INTERFACE["sidebar_border"]} !important; }}
    section[data-testid="stSidebar"] * {{ color: {CORES_INTERFACE["texto_principal"]} !important; }}
    section[data-testid="stSidebar"] .stMarkdown, section[data-testid="stSidebar"] label, section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] span, section[data-testid="stSidebar"] div {{ color: {CORES_INTERFACE["texto_principal"]} !important; }}
    section[data-testid="stSidebar"] label[data-testid="stWidgetLabel"] {{ color: {CORES_INTERFACE["texto_principal"]} !important; font-weight: 600 !important; }}
    section[data-testid="stSidebar"] .stMarkdown small {{ color: #cccccc !important; }}
    section[data-testid="stSidebar"] [data-testid="stFileUploader"] p,
    section[data-testid="stSidebar"] [data-testid="stFileUploader"] span,
    section[data-testid="stSidebar"] [data-testid="stFileUploader"] small {{ color: #000000 !important; }}
    section[data-testid="stSidebar"] [data-testid="stFileUploadDropzone"],
    section[data-testid="stSidebar"] [class*="uploadDropzone"],
    section[data-testid="stSidebar"] [class*="fileUploader"],
    section[data-testid="stSidebar"] [class*="FileUploader"] {{ background-color: #ffffff !important; border: 3px solid #ffb300 !important; border-radius: 12px !important; box-shadow: none !important; outline: none !important; }}
    section[data-testid="stSidebar"] [data-testid="stFileUploadDropzone"] > *,
    section[data-testid="stSidebar"] [class*="uploadDropzone"] > *,
    section[data-testid="stSidebar"] [class*="fileUploader"] > *,
    section[data-testid="stSidebar"] [class*="FileUploader"] > * {{ border: none !important; box-shadow: none !important; }}
    section[data-testid="stSidebar"] [data-testid="stFileUploadDropzone"] *,
    section[data-testid="stSidebar"] [class*="uploadDropzone"] *,
    section[data-testid="stSidebar"] [class*="fileUploader"] *,
    section[data-testid="stSidebar"] [class*="FileUploader"] * {{ color: #000000 !important; }}
    section[data-testid="stSidebar"] [data-testid="stFileUploaderFile"],
    section[data-testid="stSidebar"] [class*="uploadedFile"],
    section[data-testid="stSidebar"] [class*="UploadedFile"] {{ border: 3px solid #ffffff !important; border-radius: 10px !important; box-shadow: none !important; }}
    .stButton button {{ background-color: {CORES_INTERFACE["botao_primary"]} !important; color: white !important; border: none !important; border-radius: 6px !important; font-weight: 600 !important; padding: 10px 20px !important; transition: all 0.3s !important; }}
    .stButton button:hover {{ background-color: #cc0000 !important; border: 1px solid #ffffff !important; box-shadow: 0 0 12px #ffffff, 0 0 24px rgba(255,0,0,0.8) !important; color: white !important; }}
    div[data-testid="stMetricDelta"] {{ display: none !important; }}
    .stMarkdown, .stMarkdown p, .stMarkdown span, .stMarkdown div {{ color: {CORES_INTERFACE["texto_principal"]} !important; }}
    h1, h2, h3, h4, h5, h6 {{ color: {CORES_INTERFACE["texto_principal"]} !important; }}
    p {{ color: {CORES_INTERFACE["texto_principal"]} !important; }}
    hr {{ border-color: {CORES_INTERFACE["painel_border"]} !important; }}
    .alert-box {{ background-color: {CORES_INTERFACE["sidebar_background"]}; padding: 15px; border-radius: 8px; margin: 10px 0; border-left: 4px solid #ff5722; }}
    .alert-success {{ border-left-color: {CORES_KPI["DISPONIVEIS"]["border"]}; }}
    .availability-display {{ background-color: {CORES_INTERFACE["sidebar_background"]}; padding: 30px; border-radius: 8px; text-align: center; }}
    .availability-display h2 {{ color: {CORES_KPI["DISPONIVEIS"]["text"]} !important; font-size: 3.5rem !important; font-weight: 700 !important; margin: 0 !important; }}
    .availability-display p {{ color: {CORES_INTERFACE["texto_secundario"]} !important; font-size: 0.9rem !important; text-transform: uppercase !important; margin-top: 10px !important; }}
    .btn-fullscreen button {{
        background-color: transparent !important;
        color: rgba(255,255,255,0.45) !important;
        border: 1px solid rgba(255,255,255,0.18) !important;
        border-radius: 6px !important;
        font-size: 1rem !important;
        font-weight: 400 !important;
        padding: 2px 8px !important;
        line-height: 1.2 !important;
        min-height: 0 !important;
        height: 28px !important;
        width: auto !important;
        transition: all 0.2s !important;
        box-shadow: none !important;
    }}
    .btn-fullscreen button:hover {{
        background-color: #cc0000 !important;
        border: 1px solid #ffffff !important;
        box-shadow: 0 0 12px #ffffff, 0 0 24px rgba(255,0,0,0.8) !important;
        color: white !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# =====================================================
# CONSTANTES
# =====================================================
STATUS_OFICIAIS = [
    "MANUTENÇÃO", "DISPONÍVEIS NÃO TRIPULADO", "CARREGADO",
    "RETORNANDO DISPONÍVEIS", "DISPONÍVEIS TRIPULADO", "APOIO FILIAL"
]
STATUS_ADICIONAIS = ["INDISPONÍVEIS", "FORA DE OPERAÇÃO", "RETORNANDO INDISPONÍVEIS"]
ORDEM_STATUS = STATUS_OFICIAIS + STATUS_ADICIONAIS

# =====================================================
# PROCESSAMENTO DE DADOS
# =====================================================
def renomear_colunas_duplicadas(df):
    cols = pd.Series(df.columns)
    for dup in cols[cols.duplicated()].unique():
        dup_indices = [i for i, x in enumerate(cols) if x == dup]
        # Trata tanto 'UF' quanto 'UF' já em uppercase
        if str(dup).strip().upper() == 'UF' and len(dup_indices) == 2:
            cols[dup_indices[0]] = 'UF_ORIGEM'
            cols[dup_indices[1]] = 'UF_DESTINO'
        else:
            for idx, position in enumerate(dup_indices):
                if idx > 0:
                    cols[position] = f"{dup}_{idx}"
    df.columns = cols
    return df

@st.cache_data
def load_data_from_file(file_source):
    try:
        # ── Lê a planilha sem assumir que a linha 0 é cabeçalho ──
        df = pd.read_excel(file_source, sheet_name="Frota Agro ", header=None)

        if df.empty:
            st.error("❌ A planilha está vazia!")
            return pd.DataFrame()

        # ── Detecta dinamicamente onde está a linha de cabeçalho ──
        # Procura a primeira linha que contenha "STATUS" (case-insensitive)
        header_row = None
        for i, row in df.iterrows():
            valores = [str(v).strip().upper() for v in row.values]
            if "STATUS" in valores:
                header_row = i
                break

        if header_row is None:
            # Fallback: assume linha 0 como cabeçalho
            header_row = 0

        df.columns = df.iloc[header_row]
        df = df[header_row + 1:].reset_index(drop=True)

        # ── Remove colunas completamente vazias ──
        df = df.dropna(axis=1, how='all')

        # ── Normaliza nomes de colunas (strip + upper) ──
        df.columns = [str(c).strip().upper() if pd.notna(c) else f"COL_{i}"
                      for i, c in enumerate(df.columns)]

        # ── Renomeia colunas duplicadas (ex: UF → UF_ORIGEM / UF_DESTINO) ──
        df = renomear_colunas_duplicadas(df)

        # ── Limpa colunas de texto ──
        # FIX: .str.replace(r'\s+', ' ', regex=True) normaliza espaços internos duplos/triplos
        # que causavam duplicação no gráfico de Posição Atual (ex: "LUFT  BARUERI" ≠ "LUFT BARUERI")
        colunas_texto = ["STATUS", "TIPO", "POSIÇÃO ATUAL", "PLACA",
                         "MOTORISTA", "OPERAÇÃO", "UF_ORIGEM", "UF_DESTINO", "DESTINO FINAL"]
        for col in colunas_texto:
            if col in df.columns:
                df[col] = (
                    df[col].astype(str)
                    .str.strip()
                    .str.upper()
                    .str.replace(r'\s+', ' ', regex=True)  # ← normaliza espaços internos
                )
                # Substitui strings vazias e 'nan'/'none' por NaN real
                df[col] = df[col].where(
                    ~df[col].isin(["NAN", "NONE", "NAT", ""]),
                    other=pd.NA
                )

        # ── Remove linhas sem STATUS válido ──
        if "STATUS" not in df.columns:
            st.error("❌ Coluna 'STATUS' não encontrada na planilha!")
            return pd.DataFrame()

        df = df[df["STATUS"].notna() & (df["STATUS"].str.strip() != "")]

        if df.empty:
            st.error("❌ Nenhum dado válido encontrado após o processamento!")
            return pd.DataFrame()

        return df

    except ValueError as e:
        # Aba não encontrada
        st.error(f"❌ Aba 'Frota Agro ' não encontrada. Verifique o nome da aba no Excel.")
        st.error(f"Detalhe: {str(e)}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"❌ Erro ao carregar dados: {str(e)}")
        import traceback
        st.error(f"Detalhes: {traceback.format_exc()}")
        return pd.DataFrame()

def aplicar_cor_status(row):
    status = row["STATUS"]
    # Mapa de status → (cor de fundo, cor do texto)
    estilos = {
        "MANUTENÇÃO":                  ("#3d1f1f", "#ff3c00"),
        "DISPONÍVEIS NÃO TRIPULADO":   ("#1a2e1a", "#4caf50"),
        "DISPONÍVEIS TRIPULADO":       ("#1a2e1a", "#0aec0a"),
        "CARREGADO":                   ("#2e2010", "#ff9800"),
        "RETORNANDO DISPONÍVEIS":      ("#101a2e", "#2196f3"),
        "APOIO FILIAL":                ("#2e2e2e", "#ffffff"),
        "INDISPONÍVEIS":               ("#1e2025", "#94a3b8"),
        "FORA DE OPERAÇÃO":            ("#1a1c1f", "#64748b"),
        "RETORNANDO INDISPONÍVEIS":    ("#1e2025", "#cbd5e1"),
    }
    bg, fg = estilos.get(status, ("#252525", "#ffffff"))
    return [f'background-color: {bg}; color: {fg}'] * len(row)

# =====================================================
# GRÁFICOS
# =====================================================
def criar_grafico_status(status_df):
    fig = go.Figure()
    for idx, row in status_df.iterrows():
        cor = CORES_STATUS.get(row["STATUS"], "#888888")
        fig.add_trace(go.Bar(
            y=[row["STATUS"]], x=[row["QUANTIDADE"]], orientation='h',
            marker=dict(color=cor, line=dict(color='rgba(255,255,255,0.2)', width=1)),
            text=row["QUANTIDADE"], textposition='outside',
            textfont=dict(color='#ffffff', size=20, family='Arial Black'),
            hovertemplate='<b>%{y}</b><br>Quantidade: %{x}<extra></extra>', showlegend=False
        ))
    fig.update_layout(
        hoverlabel=dict(bgcolor='#1e1e1e', bordercolor='#555', font=dict(size=18, color='#ffffff', family='Arial Black'), namelength=-1),
        height=320, showlegend=False, margin=dict(l=0, r=50, t=10, b=0),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#f5f5f5', size=16),
        xaxis=dict(showgrid=True, gridcolor=CORES_INTERFACE["grid"], showline=False, zeroline=False,
                   color=CORES_INTERFACE["texto_secundario"], tickfont=dict(size=16, color=CORES_INTERFACE["texto_secundario"])),
        yaxis=dict(showgrid=False, showline=False, color='#f5f5f5',
                   tickfont=dict(size=17, color='#f5f5f5', family='Arial Black'))
    )
    return fig

def criar_grafico_tipo(tipo_df):
    fig = go.Figure()
    for idx, row in tipo_df.iterrows():
        cor = CORES_TIPO_VEICULO[idx % len(CORES_TIPO_VEICULO)]
        fig.add_trace(go.Bar(
            x=[row["TIPO"]], y=[row["QUANTIDADE"]],
            marker=dict(color=cor, line=dict(color='rgba(255,255,255,0.2)', width=1)),
            text=row["QUANTIDADE"], textposition='outside',
            textfont=dict(color='#ffffff', size=20, family='Arial Black'),
            hovertemplate='<b>%{x}</b><br>Quantidade: %{y}<extra></extra>', showlegend=False
        ))
    valor_max = tipo_df["QUANTIDADE"].max() if not tipo_df.empty else 10
    altura_minima = max(320, valor_max * 4 + 80)
    fig.update_layout(
        hoverlabel=dict(bgcolor='#1e1e1e', bordercolor='#555', font=dict(size=18, color='#ffffff', family='Arial Black'), namelength=-1),
        height=altura_minima, showlegend=False, margin=dict(l=0, r=0, t=30, b=0),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#f5f5f5', size=16),
        xaxis=dict(showgrid=False, showline=False, color=CORES_INTERFACE["texto_secundario"],
                   tickangle=0, tickfont=dict(size=16, color=CORES_INTERFACE["texto_secundario"], family='Arial Black')),
        yaxis=dict(showgrid=True, gridcolor=CORES_INTERFACE["grid"], showline=False, zeroline=False,
                   color=CORES_INTERFACE["texto_secundario"], range=[0, valor_max * 1.18],
                   tickfont=dict(size=16, color=CORES_INTERFACE["texto_secundario"]))
    )
    return fig

def criar_grafico_posicao(posicao_df, fullscreen=False):
    df_plot = posicao_df if fullscreen else posicao_df.head(10)
    n = len(df_plot)
    cores = [CORES_POSICAO[i % len(CORES_POSICAO)] for i in range(n)]
    fig = go.Figure(data=[go.Pie(
        labels=df_plot["POSIÇÃO ATUAL"], values=df_plot["QUANTIDADE"],
        hole=0.62,
        marker=dict(colors=cores, line=dict(color='#0a0a0a', width=2)),
        textfont=dict(color='#ffffff', size=18, family='Arial Black'), textinfo='value',
        hovertemplate='<b>%{label}</b><br>Quantidade: %{value}<br>%{percent}<extra></extra>'
    )])
    if fullscreen:
        fig.update_layout(
            hoverlabel=dict(bgcolor='#1e1e1e', bordercolor='#555', font=dict(size=18, color='#ffffff', family='Arial Black'), namelength=-1),
            height=720, margin=dict(l=10, r=220, t=20, b=20),
            paper_bgcolor='#141414', plot_bgcolor='#141414',
            showlegend=True,
            legend=dict(
                orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.01,
                font=dict(color='#f5f5f5', size=16, family='Arial Black'),
                bgcolor='rgba(0,0,0,0)'
            )
        )
    else:
        fig.update_layout(
            hoverlabel=dict(bgcolor='#1e1e1e', bordercolor='#555', font=dict(size=18, color='#ffffff', family='Arial Black'), namelength=-1),
            height=320, margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            showlegend=True,
            legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.02,
                        font=dict(color='#f5f5f5', size=18, family='Arial Black'), bgcolor='rgba(0,0,0,0)')
        )
    return fig

def criar_grafico_uf_origem(uf_df):
    fig = go.Figure()
    for idx, row in uf_df.iterrows():
        cor = CORES_UF[idx % len(CORES_UF)]
        fig.add_trace(go.Bar(
            x=[row["UF_ORIGEM"]], y=[row["QUANTIDADE"]],
            marker=dict(color=cor, line=dict(color='rgba(255,255,255,0.2)', width=1)),
            text=row["QUANTIDADE"], textposition='outside',
            textfont=dict(color='#ffffff', size=20, family='Arial Black'),
            hovertemplate='<b>%{x}</b><br>Veículos: %{y}<extra></extra>', showlegend=False
        ))
    valor_max = uf_df["QUANTIDADE"].max() if not uf_df.empty else 10
    altura_minima = max(320, valor_max * 4 + 80)
    fig.update_layout(
        hoverlabel=dict(bgcolor='#1e1e1e', bordercolor='#555', font=dict(size=18, color='#ffffff', family='Arial Black'), namelength=-1),
        height=altura_minima, showlegend=False, margin=dict(l=0, r=0, t=30, b=0),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#f5f5f5', size=16),
        xaxis=dict(showgrid=False, showline=False, color=CORES_INTERFACE["texto_secundario"],
                   tickangle=0, tickfont=dict(size=17, color=CORES_INTERFACE["texto_secundario"], family='Arial Black')),
        yaxis=dict(showgrid=True, gridcolor=CORES_INTERFACE["grid"], showline=False, zeroline=False,
                   color=CORES_INTERFACE["texto_secundario"], range=[0, valor_max * 1.18],
                   tickfont=dict(size=16, color=CORES_INTERFACE["texto_secundario"]))
    )
    return fig

# =====================================================
# HELPERS DO DIALOG
# =====================================================
def _hex_to_rgba(hex_color, alpha=0.12):
    h = hex_color.lstrip('#')
    r, g, b = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    return f"rgba({r},{g},{b},{alpha})"

def _html_mini_card(veiculo):
    status    = str(veiculo.get("STATUS", "")).strip()
    placa     = str(veiculo.get("PLACA", "—")).strip()
    motorista = str(veiculo.get("MOTORISTA", "")).strip()
    if motorista.upper() in ("", "NAN", "NONE"):
        motorista = "—"
    cor_status = CORES_STATUS.get(status, "#888888")
    cor_fundo  = _hex_to_rgba(cor_status, 0.22)
    cor_borda  = _hex_to_rgba(cor_status, 0.70)
    return f"""
    <div class="mini-card-veiculo" style="background:{cor_fundo};border:2px solid {cor_borda};border-left:5px solid {cor_status};box-shadow: 0 0 10px {_hex_to_rgba(cor_status, 0.18)};">
        <span class="mini-card-placa" style="color:{cor_status};text-shadow:0 0 10px {_hex_to_rgba(cor_status, 0.5)};">🚛 {placa}</span>
        <span class="mini-card-status-badge" style="background:{_hex_to_rgba(cor_status, 0.30)};border:1px solid {cor_status};color:{cor_status};">{status}</span>
        <span class="mini-card-motorista">👤 {motorista}</span>
    </div>
    """

def _html_card_completo(veiculo):
    # Campos prioritários — aparecem primeiro no card
    campos_prioridade = ["POSIÇÃO ATUAL", "UF_ORIGEM", "UF_DESTINO",
                         "DESTINO FINAL", "MOTORISTA", "OPERAÇÃO"]
    # Campos que já ficam no cabeçalho — não repetir no corpo
    campos_cabecalho  = {"PLACA", "STATUS", "TIPO"}

    status     = str(veiculo.get("STATUS", "")).strip()
    placa      = str(veiculo.get("PLACA",  "—")).strip()
    tipo       = str(veiculo.get("TIPO",   "—")).strip()
    cor_status = CORES_STATUS.get(status, "#888888")
    cor_fundo  = _hex_to_rgba(cor_status, 0.28)
    cor_borda  = _hex_to_rgba(cor_status, 0.80)
    cor_ib     = _hex_to_rgba(cor_status, 0.12)
    cor_ib2    = _hex_to_rgba(cor_status, 0.35)

    # Monta ordem: prioritários primeiro, depois todos os demais
    todos_campos = list(veiculo.index)
    campos_extras = [c for c in todos_campos
                     if c not in campos_cabecalho and c not in campos_prioridade]
    ordem_final = campos_prioridade + campos_extras

    def _valor_valido(val):
        """Retorna True se o valor tem conteúdo útil para exibir"""
        if val is None:
            return False
        try:
            if pd.isna(val):
                return False
        except (TypeError, ValueError):
            pass
        s = str(val).strip().upper()
        return s not in ("", "NAN", "NONE", "NAT", "NaT".upper(), "UNNAMED")

    info_items = ""
    for campo in ordem_final:
        val = veiculo.get(campo)
        if not _valor_valido(val):
            continue
        # Formata valor: datas, números inteiros, floats
        val_str = str(val).strip()
        # Remove ".0" de floats que são inteiros (ex: "123.0" → "123")
        try:
            f = float(val_str)
            if f == int(f):
                val_str = str(int(f))
        except (ValueError, TypeError):
            pass

        label = str(campo).replace("_", " ").title()
        info_items += f"""
        <div style="display:flex; flex-direction:column; gap:6px; padding:16px 18px;
                    border-radius:10px; background:{cor_ib}; border:1px solid {cor_ib2};
                    min-width:0; word-break:break-word;">
            <span style="font-size:0.72rem; text-transform:uppercase; letter-spacing:1.1px;
                         font-weight:700; color:{cor_status}; opacity:0.9;">{label}</span>
            <span style="color:#ffffff; font-size:1.15rem; font-weight:600; line-height:1.3;">{val_str}</span>
        </div>"""

    divider  = f'<hr style="border:none; border-top:1px solid {cor_status}; margin:16px 0 14px 0; opacity:0.4;">' if info_items else ""
    info_blk = f'<div style="display:grid; grid-template-columns:repeat(auto-fill, minmax(clamp(140px, 18vw, 220px), 1fr)); gap:clamp(8px, 1.2vw, 14px);">{info_items}</div>' if info_items else ""

    return f"""
    <div style="border-radius:14px; padding:30px 28px; margin-bottom:14px; box-sizing:border-box; width:100%;
        background:{cor_fundo}; border:2px solid {cor_borda}; border-left:8px solid {cor_status};
        box-shadow:0 0 24px {_hex_to_rgba(cor_status, 0.30)}, 0 4px 20px rgba(0,0,0,0.5);">
        <div style="display:flex; flex-wrap:wrap; align-items:center; justify-content:space-between; gap:14px;">
            <div style="display:flex; flex-wrap:wrap; align-items:center; gap:14px; min-width:0;">
                <span style="font-size:clamp(1.6rem, 4vw, 2.2rem); font-weight:900; letter-spacing:4px;
                             font-family:monospace; white-space:nowrap; color:{cor_status};
                             text-shadow:0 0 20px {_hex_to_rgba(cor_status, 0.7)};">🚛 {placa}</span>
                <span style="font-size:1rem; font-weight:700; padding:6px 16px; border-radius:20px;
                             white-space:nowrap; color:#fff;
                             background:{_hex_to_rgba(cor_status, 0.25)};
                             border:1px solid {_hex_to_rgba(cor_status, 0.5)};">{tipo}</span>
            </div>
            <span style="font-size:0.85rem; font-weight:800; text-transform:uppercase; letter-spacing:1.4px;
                         padding:9px 20px; border-radius:20px; white-space:nowrap; flex-shrink:0;
                         background:{_hex_to_rgba(cor_status, 0.35)}; border:2px solid {cor_status};
                         color:{cor_status}; box-shadow:0 0 12px {_hex_to_rgba(cor_status, 0.5)};">{status}</span>
        </div>
        {divider}
        {info_blk}
    </div>"""

# =====================================================
# DIALOG - DETALHAMENTO DO KPI (DOIS NÍVEIS)
# BUG FIX: usa session_state para persistir qual dialog está aberto
# e qual veículo foi selecionado, evitando o fechamento ao st.rerun()
# =====================================================
def mostrar_detalhes_kpi(titulo, cor_hex, df_kpi):
    """
    Painel FULLSCREEN com DOIS NÍVEIS (renderizado na página, não como dialog).
    """
    # ── CSS fullscreen: esconde sidebar, expande o conteúdo ──
    st.markdown("""
    <style>
    section[data-testid="stSidebar"] { display: none !important; }
    .main .block-container {
        padding: 1rem 1.5rem !important;
        max-width: 100% !important;
    }
    </style>
    """, unsafe_allow_html=True)

    key_sel    = f"_kpi_sel_{titulo}"
    key_busca  = f"_kpi_busca_{titulo}"
    key_fsts   = f"_kpi_fsts_{titulo}"
    key_aberto = f"_kpi_aberto_{titulo}"   # controla se o dialog deve permanecer aberto

    # Inicializa as chaves se ainda não existem
    if key_sel not in st.session_state:
        st.session_state[key_sel] = None
    if key_aberto not in st.session_state:
        st.session_state[key_aberto] = True

    # ============================================================
    # NÍVEL 2 — Card expandido de um veículo específico
    # ============================================================
    if st.session_state[key_sel] is not None:
        placa_sel = st.session_state[key_sel]
        mask = df_kpi["PLACA"].astype(str).str.strip().str.upper() == placa_sel.upper()
        resultado = df_kpi[mask]

        cor_v = CORES_STATUS.get(
            str(resultado.iloc[0].get("STATUS", "")) if not resultado.empty else "",
            cor_hex
        )

        # Botão VOLTAR no canto superior direito — laranja vivo
        st.markdown("""
        <style>
        div[role="dialog"] button[kind="secondary"] {
            background: #e65100 !important;
            color: #ffffff !important;
            border: 2px solid #ff6d00 !important;
            border-radius: 8px !important;
            font-size: 1rem !important;
            font-weight: 900 !important;
            padding: 8px 24px !important;
            letter-spacing: 1.2px !important;
            box-shadow: 0 0 18px rgba(230,81,0,0.75), 0 2px 8px rgba(0,0,0,0.5) !important;
            min-width: 130px !important;
        }
        div[role="dialog"] button[kind="secondary"]:hover {
            background: #bf360c !important;
            box-shadow: 0 0 28px rgba(230,81,0,1) !important;
            transform: scale(1.04) !important;
        }
        </style>
        """, unsafe_allow_html=True)

        col_inicio_v, col_info_only, col_btn_v = st.columns([1, 4, 1])
        with col_inicio_v:
            if st.button("🏠 INÍCIO", key=f"btn_inicio_v_{titulo}", use_container_width=True):
                for k in [k for k in st.session_state if k.startswith("_kpi_aberto_") or k.startswith("_kpi_sel_")]:
                    st.session_state[k] = False if k.startswith("_kpi_aberto_") else None
                if "_grafico_fs" in st.session_state:
                    del st.session_state["_grafico_fs"]
                st.rerun()
        with col_btn_v:
            if st.button("← VOLTAR", key=f"btn_voltar_{titulo}", use_container_width=True, type="secondary"):
                st.session_state[key_sel]    = None
                st.session_state[key_aberto] = True
                st.rerun()
        with col_info_only:
            st.markdown(f"""
            <div style="border-left:4px solid {cor_v}; padding:8px 16px;
                background:{_hex_to_rgba(cor_v, 0.18)}; border-radius:0 8px 8px 0;">
                <span style="color:#aaa; font-size:0.68rem; letter-spacing:1px; text-transform:uppercase;">VEÍCULO SELECIONADO</span><br>
                <span style="color:{cor_v}; font-size:1.25rem; font-weight:900; font-family:monospace; letter-spacing:2px;">{placa_sel}</span>
            </div>""", unsafe_allow_html=True)

        st.divider()

        if resultado.empty:
            st.warning("Veículo não encontrado.")
        else:
            st.markdown(_html_card_completo(resultado.iloc[0]), unsafe_allow_html=True)

        return  # Encerra no nível 2

    # ============================================================
    # NÍVEL 1 — Grade de mini cards
    # ============================================================

    # ── Barra de topo com botão FECHAR no canto direito ──
    st.markdown(f"""
    <style>
    /* Botão FECHAR — vermelho vivo, canto superior direito do dialog */
    div[role="dialog"] [data-testid="stButton"]:has(button[kind="secondary"]) {{
        display: flex;
        justify-content: flex-end;
    }}
    div[role="dialog"] button[kind="secondary"] {{
        background: #c62828 !important;
        color: #ffffff !important;
        border: 2px solid #ef5350 !important;
        border-radius: 8px !important;
        font-size: 1rem !important;
        font-weight: 900 !important;
        padding: 8px 24px !important;
        letter-spacing: 1.2px !important;
        box-shadow: 0 0 18px rgba(198,40,40,0.75), 0 2px 8px rgba(0,0,0,0.5) !important;
        min-width: 130px !important;
    }}
    div[role="dialog"] button[kind="secondary"]:hover {{
        background: #b71c1c !important;
        box-shadow: 0 0 28px rgba(198,40,40,1) !important;
        transform: scale(1.04) !important;
    }}
    </style>
    """, unsafe_allow_html=True)

    col_inicio, col_espacador, col_fechar = st.columns([1, 5, 1])
    with col_inicio:
        if st.button("🏠 INÍCIO", key=f"btn_inicio_{titulo}", use_container_width=True):
            for k in [k for k in st.session_state if k.startswith("_kpi_aberto_") or k.startswith("_kpi_sel_")]:
                st.session_state[k] = False if k.startswith("_kpi_aberto_") else None
            if "_grafico_fs" in st.session_state:
                del st.session_state["_grafico_fs"]
            st.rerun()
    with col_fechar:
        if st.button("✕  FECHAR", key=f"btn_fechar_{titulo}", use_container_width=True, type="secondary"):
            st.session_state[key_aberto] = False
            st.session_state[key_sel]    = None
            # Limpa todas as chaves de KPI abertas
            for k in [k for k in st.session_state if k.startswith("_kpi_aberto_") or k.startswith("_kpi_sel_")]:
                st.session_state[k] = False if k.startswith("_kpi_aberto_") else None
            st.rerun()

    st.markdown(f"""
    <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:10px;
        border-left:6px solid {cor_hex}; padding:clamp(10px,2vw,18px) clamp(12px,2.5vw,24px);
        background:{_hex_to_rgba(cor_hex, 0.22)}; border-radius:0 10px 10px 0; margin-bottom:20px;">
        <div>
            <div style="color:{cor_hex}; font-size:clamp(0.65rem,1vw,0.82rem); font-weight:700; letter-spacing:1.4px; text-transform:uppercase;">CATEGORIA SELECIONADA</div>
            <div style="color:#fff; font-size:clamp(1.1rem,2.5vw,1.7rem); font-weight:800; margin-top:6px;">{titulo}</div>
        </div>
        <div style="background:{cor_hex}; color:#fff; font-size:clamp(1.4rem,3vw,2.4rem); font-weight:900;
            padding:clamp(6px,1vw,12px) clamp(14px,2vw,28px); border-radius:12px; min-width:60px; text-align:center;
            box-shadow: 0 0 18px {_hex_to_rgba(cor_hex, 0.6)};">{len(df_kpi)}</div>
    </div>
    """, unsafe_allow_html=True)

    if df_kpi.empty:
        st.info("Nenhum veículo encontrado nesta categoria.")
        return

    # Mini-resumo por status
    if "STATUS" in df_kpi.columns and df_kpi["STATUS"].nunique() > 1:
        resumo = df_kpi["STATUS"].value_counts().reset_index()
        resumo.columns = ["STATUS", "QTD"]
        cols_r = st.columns(min(len(resumo), 5))
        for i, (_, row) in enumerate(resumo.iterrows()):
            cor = CORES_STATUS.get(row["STATUS"], "#888")
            with cols_r[i % len(cols_r)]:
                st.markdown(f"""
                <div style="border:1px solid {cor}; border-radius:8px; padding:10px 12px; text-align:center;
                    background:{_hex_to_rgba(cor, 0.22)}; margin-bottom:10px;">
                    <div style="color:{cor}; font-size:1.5rem; font-weight:800;">{row['QTD']}</div>
                    <div style="color:#bbb; font-size:0.62rem; text-transform:uppercase; letter-spacing:0.5px; line-height:1.4; margin-top:2px;">{row['STATUS']}</div>
                </div>""", unsafe_allow_html=True)
        st.divider()

    col_busca, col_filtro_status = st.columns([3, 1])
    with col_busca:
        busca = st.text_input(
            "🔍 Busca rápida",
            placeholder="Placa, motorista, posição, destino...",
            key=key_busca, label_visibility="collapsed"
        )
    with col_filtro_status:
        status_unicos = sorted(df_kpi["STATUS"].dropna().unique()) if "STATUS" in df_kpi.columns else []
        filtro_status = st.selectbox(
            "Status", options=["TODOS"] + status_unicos,
            key=key_fsts, label_visibility="collapsed"
        )

    df_exibir = df_kpi.copy()
    if filtro_status != "TODOS":
        df_exibir = df_exibir[df_exibir["STATUS"] == filtro_status]
    if busca.strip():
        mask = df_exibir.apply(
            lambda col: col.astype(str).str.upper().str.contains(busca.strip().upper(), na=False)
        ).any(axis=1)
        df_exibir = df_exibir[mask]

    # BUG FIX: dropna(axis=1) removia colunas que tinham NaN em QUALQUER linha filtrada,
    # fazendo o card perder campos válidos. Agora mantém todas as colunas do DataFrame.
    df_exibir = df_exibir.reset_index(drop=True)
    total_exibindo = len(df_exibir)

    icone = '🔎' if busca.strip() or filtro_status != 'TODOS' else '📋'
    filtro_txt = (f" · filtro: *{busca.strip()}*" if busca.strip() else "")
    status_txt = (f" · status: *{filtro_status}*" if filtro_status != "TODOS" else "")
    st.markdown(f"""<span style="font-size:1rem; color:#aaaaaa;">
    {icone} Exibindo **{total_exibindo}** veículo(s){filtro_txt}{status_txt}  —  Clique em **▶ ABRIR** para ver os detalhes completos
    </span>""", unsafe_allow_html=True)

    if df_exibir.empty:
        st.warning("Nenhum veículo corresponde ao filtro.")
        return

    NUM_COLS = 4
    for row_start in range(0, total_exibindo, NUM_COLS):
        cols = st.columns(NUM_COLS)
        for col_idx in range(NUM_COLS):
            veiculo_idx = row_start + col_idx
            if veiculo_idx >= total_exibindo:
                break
            veiculo    = df_exibir.iloc[veiculo_idx]
            placa      = str(veiculo.get("PLACA", "—")).strip()
            cor_status = CORES_STATUS.get(str(veiculo.get("STATUS", "")), "#888")

            with cols[col_idx]:
                # Mini card HTML completo e fechado num único markdown
                st.markdown(_html_mini_card(veiculo), unsafe_allow_html=True)
                # Botão nativo do Streamlit (sem wrapper de div aberta/fechada)
                if st.button(
                    "▶ ABRIR",
                    key=f"expand_{titulo}_{veiculo_idx}_{placa}",
                    use_container_width=True
                ):
                    st.session_state[key_sel] = placa
                    st.rerun()


# =====================================================
# INTERFACE
# =====================================================
def criar_header(taxa_disponibilidade=0.0):
    logo_base64 = get_base64_image("logo_luft.png")
    if logo_base64:
        logo_html = f'<img src="data:image/png;base64,{logo_base64}" class="header-logo" alt="Logo Luft">'
    else:
        logo_html = '<div class="header-logo-placeholder">🚨 TORRE DE CONTROLE</div>'
    st.markdown(f"""
    <div class="main-header">
        <div class="sirene-container">
            <div class="sirene-beam"></div>
            <div class="sirene-light"></div>
            <div class="sirene-base"></div>
        </div>
        <div class="header-center">{logo_html}</div>
        <div class="mini-disponibilidade">
            <div class="mini-label">DISPONIBILIDADE</div>
            <div class="mini-valor">{taxa_disponibilidade:.1f}%</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def criar_kpis(df_filtrado):
    total          = len(df_filtrado)
    df_total       = df_filtrado.copy()
    df_operacao    = df_filtrado[df_filtrado["STATUS"].isin(["CARREGADO", "RETORNANDO DISPONÍVEIS"])].copy()
    df_disponiveis = df_filtrado[df_filtrado["STATUS"].isin(["DISPONÍVEIS TRIPULADO", "DISPONÍVEIS NÃO TRIPULADO"])].copy()
    df_manutencao  = df_filtrado[df_filtrado["STATUS"] == "MANUTENÇÃO"].copy()

    em_operacao = len(df_operacao)
    disponiveis = len(df_disponiveis)
    manutencao  = len(df_manutencao)

    # ── FIX: salvar os DataFrames dos KPIs no session_state ─────────────
    # para que o dialog possa ser reaberto com os dados corretos após rerun
    st.session_state["_kpi_df_TOTAL DE VEÍCULOS"]  = df_total
    st.session_state["_kpi_df_EM OPERAÇÃO"]        = df_operacao
    st.session_state["_kpi_df_DISPONÍVEIS"]        = df_disponiveis
    st.session_state["_kpi_df_MANUTENÇÃO"]         = df_manutencao
    # ────────────────────────────────────────────────────────────────────

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="kpi-card kpi-azul">
            <div class="kpi-label">TOTAL DE VEÍCULOS</div>
            <div class="kpi-value">{total}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔍 VER TODOS OS VEÍCULOS", key="btn_kpi_total", use_container_width=True):
            for k in [k for k in st.session_state if k.startswith("_kpi_aberto_") or k.startswith("_kpi_sel_")]:
                st.session_state[k] = False if k.startswith("_kpi_aberto_") else None
            st.session_state["_kpi_aberto_TOTAL DE VEÍCULOS"] = True
            st.session_state["_kpi_sel_TOTAL DE VEÍCULOS"]    = None
            st.rerun()

    with col2:
        st.markdown(f"""
        <div class="kpi-card kpi-laranja">
            <div class="kpi-label">EM OPERAÇÃO</div>
            <div class="kpi-value">{em_operacao}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔍 VER EM OPERAÇÃO", key="btn_kpi_operacao", use_container_width=True):
            for k in [k for k in st.session_state if k.startswith("_kpi_aberto_") or k.startswith("_kpi_sel_")]:
                st.session_state[k] = False if k.startswith("_kpi_aberto_") else None
            st.session_state["_kpi_aberto_EM OPERAÇÃO"] = True
            st.session_state["_kpi_sel_EM OPERAÇÃO"]    = None
            st.rerun()

    with col3:
        st.markdown(f"""
        <div class="kpi-card kpi-verde">
            <div class="kpi-label">DISPONÍVEIS</div>
            <div class="kpi-value">{disponiveis}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔍 VER DISPONÍVEIS", key="btn_kpi_disponiveis", use_container_width=True):
            for k in [k for k in st.session_state if k.startswith("_kpi_aberto_") or k.startswith("_kpi_sel_")]:
                st.session_state[k] = False if k.startswith("_kpi_aberto_") else None
            st.session_state["_kpi_aberto_DISPONÍVEIS"] = True
            st.session_state["_kpi_sel_DISPONÍVEIS"]    = None
            st.rerun()

    with col4:
        st.markdown(f"""
        <div class="kpi-card kpi-vermelho">
            <div class="kpi-label">MANUTENÇÃO</div>
            <div class="kpi-value">{manutencao}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔍 VER EM MANUTENÇÃO", key="btn_kpi_manutencao", use_container_width=True):
            for k in [k for k in st.session_state if k.startswith("_kpi_aberto_") or k.startswith("_kpi_sel_")]:
                st.session_state[k] = False if k.startswith("_kpi_aberto_") else None
            st.session_state["_kpi_aberto_MANUTENÇÃO"] = True
            st.session_state["_kpi_sel_MANUTENÇÃO"]    = None
            st.rerun()

    return em_operacao, disponiveis, manutencao


def criar_sidebar(main_loading_placeholder):
    with st.sidebar:
        st.header("🎛️ FILTROS OPERACIONAIS")
        st.divider()
        st.subheader("📁 CARREGAR ARQUIVO")

        uploaded_file = st.file_uploader(
            "Faça upload do arquivo Excel", type=['xlsx', 'xls'],
            help="Selecione o arquivo da planilha de frota"
        )

        df_base = pd.DataFrame()

        if uploaded_file is not None:
            show_loading_screen(main_loading_placeholder)
            df_base = load_data_from_file(uploaded_file)
            main_loading_placeholder.empty()
            if not df_base.empty:
                st.success("✅ Arquivo carregado com sucesso!")

        st.divider()

        if df_base.empty:
            st.info("⬆️ Faça upload de um arquivo Excel para visualizar os dados.")
            return pd.DataFrame(), [], [], [], []

        incluir_todos_status = st.checkbox("📋 Incluir TODOS os STATUS", value=False)
        STATUS_PARA_USAR = STATUS_OFICIAIS + STATUS_ADICIONAIS if incluir_todos_status else STATUS_OFICIAIS
        df_base_filtrado = df_base[df_base["STATUS"].isin(STATUS_PARA_USAR)].copy()

        status_disponiveis = sorted([s for s in df_base_filtrado["STATUS"].unique() if s in STATUS_PARA_USAR])
        status_sel = st.multiselect("📊 STATUS", status_disponiveis, default=status_disponiveis)

        tipos_disponiveis = sorted([t for t in df_base_filtrado["TIPO"].unique() if pd.notna(t) and t != ""])
        tipo_sel = st.multiselect("🚛 TIPO DE VEÍCULO", tipos_disponiveis, default=tipos_disponiveis)

        posicoes_disponiveis = sorted([p for p in df_base_filtrado["POSIÇÃO ATUAL"].unique() if pd.notna(p) and p != ""])
        pos_sel = st.multiselect("📍 POSIÇÃO ATUAL", posicoes_disponiveis, default=posicoes_disponiveis)

        if "UF_ORIGEM" in df_base_filtrado.columns:
            ufs_disponiveis = sorted([u for u in df_base_filtrado["UF_ORIGEM"].unique() if pd.notna(u) and u != ""])
            uf_sel = st.multiselect("🗺️ UF DE ORIGEM", ufs_disponiveis, default=ufs_disponiveis)
        else:
            uf_sel = []

        if st.button("🔄 ATUALIZAR DADOS AGORA", use_container_width=True):
            st.cache_data.clear()
            st.rerun()

        return df_base_filtrado, status_sel, tipo_sel, pos_sel, uf_sel


def criar_painel_status(status_df):
    with st.container(border=True):
        col_t, col_b = st.columns([11, 1])
        with col_t:
            st.markdown('<div class="card-title">📊 STATUS DA FROTA</div>', unsafe_allow_html=True)
        with col_b:
            st.markdown('<div class="btn-fullscreen">', unsafe_allow_html=True)
            if st.button("⛶", key="fs_btn_status"):
                st.session_state["_grafico_fs"] = "status"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        st.plotly_chart(criar_grafico_status(status_df), use_container_width=True, config={'displayModeBar': False})

def criar_painel_uf(uf_df):
    with st.container(border=True):
        col_t, col_b = st.columns([11, 1])
        with col_t:
            st.markdown('<div class="card-title">🗺️ DISTRIBUIÇÃO POR UF (ORIGEM)</div>', unsafe_allow_html=True)
        with col_b:
            st.markdown('<div class="btn-fullscreen">', unsafe_allow_html=True)
            if st.button("⛶", key="fs_btn_uf"):
                st.session_state["_grafico_fs"] = "uf"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        st.plotly_chart(criar_grafico_uf_origem(uf_df), use_container_width=True, config={'displayModeBar': False})

def criar_painel_tipo(tipo_df):
    with st.container(border=True):
        col_t, col_b = st.columns([11, 1])
        with col_t:
            st.markdown('<div class="card-title">🚛 TIPO DE VEÍCULO</div>', unsafe_allow_html=True)
        with col_b:
            st.markdown('<div class="btn-fullscreen">', unsafe_allow_html=True)
            if st.button("⛶", key="fs_btn_tipo"):
                st.session_state["_grafico_fs"] = "tipo"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        st.plotly_chart(criar_grafico_tipo(tipo_df), use_container_width=True, config={'displayModeBar': False})

def criar_painel_posicao(posicao_df):
    with st.container(border=True):
        col_t, col_b = st.columns([11, 1])
        with col_t:
            st.markdown('<div class="card-title">📍 POSIÇÃO ATUAL</div>', unsafe_allow_html=True)
        with col_b:
            st.markdown('<div class="btn-fullscreen">', unsafe_allow_html=True)
            if st.button("⛶", key="fs_btn_posicao"):
                st.session_state["_grafico_fs"] = "posicao"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        st.plotly_chart(criar_grafico_posicao(posicao_df), use_container_width=True, config={'displayModeBar': False})


def mostrar_grafico_fullscreen(grafico_id, status_df, tipo_df, posicao_df, uf_origem_df):
    """Renderiza o gráfico escolhido em modo tela cheia com botão fechar."""
    titulos = {
        "status":  "📊 STATUS DA FROTA",
        "posicao": "📍 POSIÇÃO ATUAL",
        "tipo":    "🚛 TIPO DE VEÍCULO",
        "uf":      "🗺️ DISTRIBUIÇÃO POR UF (ORIGEM)",
    }
    titulo = titulos.get(grafico_id, "")

    st.markdown(f"""
    <style>
    section[data-testid="stSidebar"] {{ display: none !important; }}
    .stApp {{ background: #141414 !important; }}
    .main .block-container {{ padding: 1rem 1.5rem !important; max-width: 100% !important; background: #141414 !important; }}
    </style>
    """, unsafe_allow_html=True)

    col_titulo, col_fechar = st.columns([10, 2])
    with col_titulo:
        st.markdown(f'<div class="card-title" style="font-size:1.3rem;">{titulo}</div>', unsafe_allow_html=True)
    with col_fechar:
        if st.button("✕  Fechar", key="fs_fechar", use_container_width=True):
            del st.session_state["_grafico_fs"]
            st.rerun()

    st.markdown("<hr style='border-color:#484848;margin:0 0 12px 0;'>", unsafe_allow_html=True)

    if grafico_id == "status":
        fig = criar_grafico_status(status_df)
        fig.update_layout(height=680, margin=dict(l=10, r=10, t=20, b=10), paper_bgcolor='#141414', plot_bgcolor='#141414')
    elif grafico_id == "posicao":
        fig = criar_grafico_posicao(posicao_df, fullscreen=True)
    elif grafico_id == "tipo":
        fig = criar_grafico_tipo(tipo_df)
        fig.update_layout(height=680, margin=dict(l=10, r=10, t=20, b=10), paper_bgcolor='#141414', plot_bgcolor='#141414')
    elif grafico_id == "uf":
        fig = criar_grafico_uf_origem(uf_origem_df)
        fig.update_layout(height=680, margin=dict(l=10, r=10, t=20, b=10), paper_bgcolor='#141414', plot_bgcolor='#141414')
    else:
        st.stop()

    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': True})

def criar_tabela_detalhada(df_filtrado):
    with st.container(border=True):
        st.markdown('<div class="card-title">📋 DETALHAMENTO COMPLETO DA FROTA</div>', unsafe_allow_html=True)
        colunas_exibir = ["PLACA", "STATUS", "TIPO", "POSIÇÃO ATUAL"]
        if "UF_ORIGEM" in df_filtrado.columns:
            colunas_exibir.append("UF_ORIGEM")
        if "DESTINO FINAL" in df_filtrado.columns:
            colunas_exibir.append("DESTINO FINAL")
        if "UF_DESTINO" in df_filtrado.columns:
            colunas_exibir.append("UF_DESTINO")
        colunas_exibir.append("MOTORISTA")
        df_display = df_filtrado[colunas_exibir].copy()
        st.dataframe(
            df_display.style.apply(aplicar_cor_status, axis=1),
            hide_index=True, use_container_width=True, height=400
        )


# =====================================================
# FUNÇÃO PRINCIPAL
# =====================================================

def main():
    load_custom_css()
    # Fix tooltip color via JS (Streamlit gera classes dinâmicas)
    st.markdown("""<script>
    (function(){
        var style = document.createElement('style');
        style.textContent = '[class*="TooltipContent"],[class*="tooltip"]{background:#1a1a1a!important;color:#fff!important;border:1px solid #555!important;}[class*="TooltipContent"] *{color:#fff!important;}';
        document.head.appendChild(style);
    })();
    </script>""", unsafe_allow_html=True)
    loading_placeholder = st.empty()

    df_base_filtrado, status_sel, tipo_sel, pos_sel, uf_sel = criar_sidebar(loading_placeholder)

    if df_base_filtrado.empty:
        st.markdown("""
        <style>
        .centered-warning { display: flex; justify-content: center; align-items: center; min-height: 60vh; text-align: center; }
        .warning-box { background-color: #1e1e1e; border: 2px solid #ff9800; border-radius: 15px; padding: 40px 60px; box-shadow: 0 0 20px rgba(255, 152, 0, 0.3); }
        .warning-icon { font-size: 4rem; margin-bottom: 20px; }
        .warning-text { font-size: 1.3rem; color: #ffffff; font-weight: 600; line-height: 1.6; }
        </style>
        <div class="centered-warning">
            <div class="warning-box">
                <div class="warning-icon">⚠️</div>
                <div class="warning-text">Por favor, carregue um arquivo Excel<br>na barra lateral para visualizar os dados.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.stop()

    filtro_aplicado = (
        (df_base_filtrado["STATUS"].isin(status_sel)) &
        (df_base_filtrado["TIPO"].isin(tipo_sel)) &
        (df_base_filtrado["POSIÇÃO ATUAL"].isin(pos_sel))
    )
    if "UF_ORIGEM" in df_base_filtrado.columns and uf_sel:
        filtro_aplicado = filtro_aplicado & (df_base_filtrado["UF_ORIGEM"].isin(uf_sel))

    df_filtrado = df_base_filtrado[filtro_aplicado].copy()

    manutencao_count = len(df_filtrado[df_filtrado["STATUS"] == "MANUTENÇÃO"])
    taxa_disponibilidade = ((len(df_filtrado) - manutencao_count) / len(df_filtrado) * 100) if len(df_filtrado) > 0 else 0.0

    criar_header(taxa_disponibilidade)

    em_operacao, disponiveis, manutencao = criar_kpis(df_filtrado)
    st.markdown("<br>", unsafe_allow_html=True)

    # ── Modo fullscreen KPI ──────────────────────────────────────────────
    kpis_config = [
        ("TOTAL DE VEÍCULOS",  CORES_KPI["TOTAL"]["border"]),
        ("EM OPERAÇÃO",        CORES_KPI["OPERACAO"]["border"]),
        ("DISPONÍVEIS",        CORES_KPI["DISPONIVEIS"]["border"]),
        ("MANUTENÇÃO",         CORES_KPI["MANUTENCAO"]["border"]),
    ]
    for titulo_kpi, cor_kpi in kpis_config:
        key_sel    = f"_kpi_sel_{titulo_kpi}"
        key_aberto = f"_kpi_aberto_{titulo_kpi}"
        key_df     = f"_kpi_df_{titulo_kpi}"
        if (st.session_state.get(key_sel) or st.session_state.get(key_aberto)) and key_df in st.session_state:
            mostrar_detalhes_kpi(titulo_kpi, cor_kpi, st.session_state[key_df])
            st.stop()  # não renderiza o resto da página
    # ─────────────────────────────────────────────────────────────────────

    status_counts = df_filtrado["STATUS"].value_counts()
    status_df = pd.DataFrame({
        "STATUS": [s for s in ORDEM_STATUS if s in status_counts.index],
        "QUANTIDADE": [status_counts.get(s, 0) for s in ORDEM_STATUS if s in status_counts.index]
    })
    status_df = status_df[status_df["QUANTIDADE"] > 0]

    tipo_df    = df_filtrado["TIPO"].value_counts().reset_index().rename(columns={"count": "QUANTIDADE"})
    posicao_df = df_filtrado["POSIÇÃO ATUAL"].value_counts().reset_index().rename(columns={"count": "QUANTIDADE"})

    if "UF_ORIGEM" in df_filtrado.columns:
        uf_origem_df = df_filtrado["UF_ORIGEM"].value_counts().reset_index().rename(columns={"count": "QUANTIDADE"})
    else:
        uf_origem_df = pd.DataFrame()

    # ── Modo tela cheia de gráfico ──────────────────────────────────────
    if st.session_state.get("_grafico_fs"):
        mostrar_grafico_fullscreen(
            st.session_state["_grafico_fs"],
            status_df, tipo_df, posicao_df, uf_origem_df
        )
        st.stop()
    # ────────────────────────────────────────────────────────────────────

    col_graf1, col_graf2 = st.columns(2)
    with col_graf1:
        criar_painel_status(status_df)
    with col_graf2:
        criar_painel_posicao(posicao_df)

    st.markdown("<br>", unsafe_allow_html=True)
    col_graf4, col_graf5 = st.columns(2)
    with col_graf4:
        criar_painel_tipo(tipo_df)
    with col_graf5:
        if not uf_origem_df.empty:
            criar_painel_uf(uf_origem_df)

    st.markdown("<br>", unsafe_allow_html=True)
    criar_tabela_detalhada(df_filtrado)


if __name__ == "__main__":
    main()
