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
# Paleta de cores padronizada para toda a aplicação
# =====================================================

# Cores dos Status - Define cores para cada status de veículo
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

# Cores dos KPIs - Bordas, textos e sombras dos cartões de métricas
CORES_KPI = {
    "TOTAL": {
        "border": "#2196f3",
        "text": "#2196f3",
        "shadow": "rgba(33, 150, 243, 0.5)"
    },
    "OPERACAO": {
        "border": "#ff9800",
        "text": "#ff9800",
        "shadow": "rgba(255, 152, 0, 0.5)"
    },
    "DISPONIVEIS": {
        "border": "#4caf50",
        "text": "#4caf50",
        "shadow": "rgba(76, 175, 80, 0.5)"
    },
    "MANUTENCAO": {
        "border": "#ff3c00",
        "text": "#ff3c00",
        "shadow": "rgba(255, 60, 0, 0.5)"
    }
}

# Cores dos Gráficos - Paletas para visualizações
CORES_TIPO_VEICULO = ['#03a9f4', "#033966", '#4caf50', '#ff9800', '#ff5722', '#9c27b0']
CORES_POSICAO = ["#0e9ef1", '#ff5722', "#fc9700", "#033864", '#9c27b0', "#43eb10", "#325509", '#ff5252', "#fdd660", '#795548']
CORES_UF = ['#4caf50', '#2196f3', '#ff9800', "#fd3d02", '#9c27b0', "#03405c", '#8bc34a', '#ff5252']

# Cores do Header - Cabeçalho principal
CORES_HEADER = {
    "background": "#252525",
    "border": "#ffffff",
    "title": "#ffffff",
    "subtitle": "#888",
    "dot": "#4caf50"
}

# Cores da Sirene - Animação giroflex no header
CORES_SIRENE = {
    "base_top": "#666",
    "base_bottom": "#333",
    "light_top": "#ff5722",
    "light_bottom": "#d32f2f",
    "light_glow": "rgba(255, 87, 34, 0.8)",
    "light_top_alt": "#ff9800",
    "light_bottom_alt": "#ff5722",
    "light_glow_alt": "rgba(255, 152, 0, 1)",
    "beam": "rgba(255, 87, 34, 0.3)"
}

# Cores do Mini Painel de Disponibilidade - Widget no header
CORES_DISPONIBILIDADE = {
    "background_start": "#000000",
    "background_end": "#000000",
    "border": "#2e5a2e",
    "label": "#000000fa",
    "valor": "#000000",
    "subtitle": "#000000"
}

# Cores Gerais da Interface - Elementos comuns
CORES_INTERFACE = {
    "fundo_gradiente_start": "#2d2d2d",
    "fundo_gradiente_end": "#1a1a1a",
    "painel_background": "#252525",
    "painel_border": "#333",
    "sidebar_background": "#1e1e1e",
    "sidebar_border": "#333",
    "texto_principal": "#ffffff",
    "texto_secundario": "#888",
    "grid": "#333",
    "botao_primary": "#2196f3",
    "botao_hover": "#1976d2",
    "tabela_header_bg": "#1e1e1e",
    "tabela_row_bg": "#252525",
    "tabela_row_hover": "#2a2a2a"
}

# =====================================================
# CONFIGURAÇÃO DA PÁGINA
# Setup inicial do Streamlit
# =====================================================
st.set_page_config(
    page_title="TORRE DE CONTROLE | FROTA AGRO",
    layout="wide",
    page_icon="🚛",
    initial_sidebar_state="expanded"
)

# =====================================================
# FUNÇÃO PARA CODIFICAR IMAGEM EM BASE64
# Converte imagem para string base64 para embed no HTML
# =====================================================
def get_base64_image(image_path):
    """Converte imagem para base64 para uso no HTML"""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return None

# =====================================================
# FUNÇÃO PARA MOSTRAR TELA DE LOADING
# Exibe animação de carregamento em tela cheia
# =====================================================
def show_loading_screen(placeholder):
    """Exibe tela de loading em tela cheia com a imagem"""
    img_base64 = get_base64_image("luft.png")
    
    if img_base64:
        loading_html = f"""
        <style>
        .loading-overlay {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background-color: #1a1a1a;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            z-index: 9999;
        }}
        .loading-image {{
            max-width: 80vw;
            max-height: 80vh;
            object-fit: contain;
            animation: pulse 2s ease-in-out infinite;
        }}
        .loading-text {{
            color: #ffffff;
            font-size: 24px;
            font-weight: 700;
            margin-top: 30px;
            text-align: center;
            animation: blink 1.5s ease-in-out infinite;
        }}
        @keyframes pulse {{
            0%, 100% {{ opacity: 0.8; transform: scale(1); }}
            50% {{ opacity: 1; transform: scale(1.05); }}
        }}
        @keyframes blink {{
            0%, 100% {{ opacity: 0.5; }}
            50% {{ opacity: 1; }}
        }}
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
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background-color: #1a1a1a;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            z-index: 9999;
        }
        .loading-text {
            color: #ffffff;
            font-size: 32px;
            font-weight: 700;
            text-align: center;
            animation: blink 1.5s ease-in-out infinite;
        }
        @keyframes blink {
            0%, 100% { opacity: 0.5; }
            50% { opacity: 1; }
        }
        </style>
        <div class="loading-overlay">
            <div class="loading-text">🚛 CARREGANDO DADOS...</div>
        </div>
        """
    
    placeholder.markdown(loading_html, unsafe_allow_html=True)

# =====================================================
# CSS CUSTOMIZADO
# Estilos personalizados para toda a interface
# =====================================================
def load_custom_css():
    st.markdown(f"""
    <style>
    /* ====== FORÇAR SOBREPOSIÇÃO COMPLETA DO STREAMLIT ====== */
    /* Fonte padrão para toda aplicação */
    * {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
    }}
    
    /* ====== REMOVER HEADER PADRÃO STREAMLIT ====== */
    /* Esconde header nativo do Streamlit */
    header[data-testid="stHeader"] {{
        background-color: rgba(0,0,0,0) !important;
        backdrop-filter: none !important;
    }}
    
    header[data-testid="stHeader"] > div:first-child {{
        background-color: transparent !important;
    }}
    
    button[kind="header"] {{
        color: white !important;
    }}
    
    .main .block-container {{
        padding-top: 2rem !important;
    }}
    
    /* ====== FUNDO GERAL ====== */
    /* Gradiente de fundo da aplicação */
    .stApp {{
        background: linear-gradient(135deg, {CORES_INTERFACE["fundo_gradiente_start"]} 0%, {CORES_INTERFACE["fundo_gradiente_end"]} 100%) !important;
    }}
    
    .block-container {{
        padding-top: 1.5rem !important;
        padding-bottom: 1rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }}
    
    /* ====== PAINÉIS/CONTAINERS ====== */
    /* Estilo dos cartões/painéis */
    div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlockBorderWrapper"] {{
        background-color: {CORES_INTERFACE["painel_background"]} !important;
        border: 1px solid {CORES_INTERFACE["painel_border"]} !important;
        border-radius: 10px !important;
        padding: 25px !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3) !important;
    }}
    
    /* ====== TÍTULOS DOS PAINÉIS ====== */
    /* Cabeçalhos dos cartões */
    .card-title {{
        font-weight: 700;
        font-size: 0.95rem;
        color: {CORES_INTERFACE["texto_principal"]} !important;
        text-transform: uppercase;
        margin-bottom: 20px;
        letter-spacing: 0.5px;
        display: flex;
        align-items: center;
        gap: 10px;
    }}
    
    /* ====== KPI CARDS CUSTOM ====== */
    /* Cartões de métricas principais */
    .kpi-card {{
        background-color: {CORES_INTERFACE["painel_background"]};
        border-radius: 10px;
        padding: 25px 15px;
        text-align: center;
        width: 100%;
        box-sizing: border-box;
    }}
    .kpi-card .kpi-label {{
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 10px;
    }}
    .kpi-card .kpi-value {{
        font-size: 3rem;
        font-weight: 700;
        line-height: 1.1;
    }}

    /* AZUL - TOTAL */
    /* KPI de total de veículos */
    .kpi-azul {{
        border: 2px solid {CORES_KPI["TOTAL"]["border"]};
        box-shadow: 0 0 15px {CORES_KPI["TOTAL"]["shadow"]}, 0 4px 15px rgba(0,0,0,0.3);
    }}
    .kpi-azul .kpi-label {{ color: {CORES_KPI["TOTAL"]["text"]}; }}
    .kpi-azul .kpi-value {{ color: {CORES_KPI["TOTAL"]["text"]}; }}

    /* LARANJA - EM OPERAÇÃO */
    /* KPI de veículos em operação */
    .kpi-laranja {{
        border: 2px solid {CORES_KPI["OPERACAO"]["border"]};
        box-shadow: 0 0 15px {CORES_KPI["OPERACAO"]["shadow"]}, 0 4px 15px rgba(0,0,0,0.3);
    }}
    .kpi-laranja .kpi-label {{ color: {CORES_KPI["OPERACAO"]["text"]}; }}
    .kpi-laranja .kpi-value {{ color: {CORES_KPI["OPERACAO"]["text"]}; }}

    /* VERDE - DISPONÍVEIS */
    /* KPI de veículos disponíveis */
    .kpi-verde {{
        border: 2px solid {CORES_KPI["DISPONIVEIS"]["border"]};
        box-shadow: 0 0 15px {CORES_KPI["DISPONIVEIS"]["shadow"]}, 0 4px 15px rgba(0,0,0,0.3);
    }}
    .kpi-verde .kpi-label {{ color: {CORES_KPI["DISPONIVEIS"]["text"]}; }}
    .kpi-verde .kpi-value {{ color: {CORES_KPI["DISPONIVEIS"]["text"]}; }}

    /* VERMELHO - MANUTENÇÃO */
    /* KPI de veículos em manutenção */
    .kpi-vermelho {{
        border: 2px solid {CORES_KPI["MANUTENCAO"]["border"]};
        box-shadow: 0 0 15px {CORES_KPI["MANUTENCAO"]["shadow"]}, 0 4px 15px rgba(0,0,0,0.3);
    }}
    .kpi-vermelho .kpi-label {{ color: {CORES_KPI["MANUTENCAO"]["text"]}; }}
    .kpi-vermelho .kpi-value {{ color: {CORES_KPI["MANUTENCAO"]["text"]}; }}

    /* ====== HEADER PRINCIPAL ====== */
    /* Cabeçalho da página */
    .main-header {{
        background-color: {CORES_HEADER["background"]};
        padding: 25px 30px;
        border-radius: 10px;
        border: 3px solid {CORES_HEADER["border"]};
        margin-bottom: 25px;
        box-shadow: 0 0 12px rgba(255, 255, 255, 0.4), 0 4px 15px rgba(0, 0, 0, 0.3);
        display: flex;
        align-items: center;
        gap: 20px;
    }}
    
    .main-header h1 {{
        color: {CORES_HEADER["title"]};
        font-size: 2rem;
        font-weight: 800;
        margin: 0;
        margin-bottom: 8px;
        letter-spacing: 0.5px;
        text-align: center;
    }}
    
    .main-header p {{
        color: {CORES_HEADER["subtitle"]};
        font-size: 0.9rem;
        margin: 0;
    }}

    .header-left {{
        display: flex;
        align-items: center;
        padding-left: 15px;
        min-width: 220px;
    }}

    .header-center {{
        flex: 1;
        display: flex;
        align-items: center;
        justify-content: center;
        padding-right: 200px;
    }}

    /* ====== LOGO NO HEADER ====== */
    /* Estilo da logo centralizada */
    .header-logo {{
        max-height: 120px;
        max-width: 750px;
        width: 95%;
        height: auto;
        object-fit: contain;
        margin: 0;
        display: block;
        filter: drop-shadow(0 2px 8px rgba(255, 255, 255, 0.2));
        transition: all 0.3s ease;
    }}
    
    .header-logo:hover {{
        filter: drop-shadow(0 4px 12px rgba(255, 255, 255, 0.4));
        transform: scale(1.02);
    }}
    
    .header-logo-placeholder {{
        font-size: 1.8rem;
        font-weight: 800;
        color: {CORES_HEADER["title"]};
        margin-bottom: 8px;
        letter-spacing: 1px;
    }}

    /* ====== MINI PAINEL DE DISPONIBILIDADE NO HEADER ====== */
    /* Widget de taxa de disponibilidade */
    .mini-disponibilidade {{
        background: linear-gradient(135deg, {CORES_DISPONIBILIDADE["background_start"]} 0%, {CORES_DISPONIBILIDADE["background_end"]} 100%);
        border: 1px solid {CORES_DISPONIBILIDADE["border"]};
        border-radius: 10px;
        padding: 18px 28px;
        text-align: center;
        flex-shrink: 0;
        min-width: 170px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255,255,255,0.05);
    }}

    .mini-disponibilidade .mini-label {{
        font-size: 0.65rem;
        font-weight: 700;
        color: {CORES_DISPONIBILIDADE["label"]};
        text-transform: uppercase;
        letter-spacing: 1.2px;
        margin-bottom: 6px;
    }}

    .mini-disponibilidade .mini-valor {{
        font-size: 3rem;
        font-weight: 700;
        color: {CORES_DISPONIBILIDADE["valor"]};
        line-height: 1.1;
        margin: 0;
    }}

    .mini-disponibilidade .mini-sub {{
        font-size: 0.62rem;
        color: {CORES_DISPONIBILIDADE["subtitle"]};
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-top: 4px;
    }}

    .mini-disponibilidade .mini-icon {{
        font-size: 0.8rem;
        margin-bottom: 2px;
    }}
    
    /* ====== SIRENE GIROFLEX ANIMADA ====== */
    /* Animação de sirene no header */
    .sirene-container {{
        position: relative;
        width: 60px;
        height: 60px;
        flex-shrink: 0;
    }}
    
    /* Base da sirene */
    .sirene-base {{
        position: absolute;
        bottom: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 50px;
        height: 15px;
        background: linear-gradient(180deg, {CORES_SIRENE["base_top"]} 0%, {CORES_SIRENE["base_bottom"]} 100%);
        border-radius: 0 0 8px 8px;
    }}
    
    /* Luz da sirene */
    .sirene-light {{
        position: absolute;
        top: 5px;
        left: 50%;
        transform: translateX(-50%);
        width: 40px;
        height: 35px;
        background: linear-gradient(180deg, {CORES_SIRENE["light_top"]} 0%, {CORES_SIRENE["light_bottom"]} 100%);
        border-radius: 50% 50% 20% 20%;
        box-shadow: 0 0 20px {CORES_SIRENE["light_glow"]};
        animation: giroflex 1s infinite;
    }}
    
    /* Brilho da luz */
    .sirene-light::before {{
        content: '';
        position: absolute;
        top: 5px;
        left: 5px;
        width: 30px;
        height: 25px;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.3) 0%, transparent 100%);
        border-radius: 50% 50% 20% 20%;
    }}
    
    /* Feixe de luz */
    .sirene-beam {{
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 0;
        height: 0;
        border-left: 60px solid transparent;
        border-right: 60px solid transparent;
        border-top: 40px solid {CORES_SIRENE["beam"]};
        animation: beam-rotate 1s infinite;
        transform-origin: 50% 0%;
    }}
    
    /* Animação pulsante da luz */
    @keyframes giroflex {{
        0%, 100% {{
            background: linear-gradient(180deg, {CORES_SIRENE["light_top"]} 0%, {CORES_SIRENE["light_bottom"]} 100%);
            box-shadow: 0 0 20px {CORES_SIRENE["light_glow"]};
        }}
        50% {{
            background: linear-gradient(180deg, {CORES_SIRENE["light_top_alt"]} 0%, {CORES_SIRENE["light_bottom_alt"]} 100%);
            box-shadow: 0 0 40px {CORES_SIRENE["light_glow_alt"]}, 0 0 60px rgba(255, 87, 34, 0.6);
        }}
    }}
    
    /* Animação de rotação do feixe */
    @keyframes beam-rotate {{
        0% {{
            transform: translate(-50%, -50%) rotate(0deg);
            opacity: 0.3;
        }}
        50% {{
            opacity: 0.6;
        }}
        100% {{
            transform: translate(-50%, -50%) rotate(360deg);
            opacity: 0.3;
        }}
    }}
    
    /* Indicador de status pulsante */
    .status-dot {{
        display: inline-block;
        width: 8px;
        height: 8px;
        background-color: {CORES_HEADER["dot"]};
        border-radius: 50%;
        margin-right: 8px;
        animation: pulse 2s infinite;
    }}
    
    /* Animação de pulso */
    @keyframes pulse {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0.5; }}
    }}
    
    /* ====== TABELAS ====== */
    /* Estilo das tabelas de dados */
    .dataframe {{
        font-size: 0.85rem !important;
        color: {CORES_INTERFACE["texto_principal"]} !important;
    }}
    
    /* Cabeçalho da tabela */
    .dataframe thead tr th {{
        background-color: {CORES_INTERFACE["tabela_header_bg"]} !important;
        color: {CORES_INTERFACE["texto_secundario"]} !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        font-size: 0.7rem !important;
        letter-spacing: 0.5px !important;
        border-bottom: 1px solid {CORES_INTERFACE["painel_border"]} !important;
    }}
    
    /* Linhas da tabela */
    .dataframe tbody tr td {{
        background-color: {CORES_INTERFACE["tabela_row_bg"]} !important;
        color: {CORES_INTERFACE["texto_principal"]} !important;
        border-bottom: 1px solid {CORES_INTERFACE["painel_border"]} !important;
    }}
    
    /* Hover nas linhas */
    .dataframe tbody tr:hover td {{
        background-color: {CORES_INTERFACE["tabela_row_hover"]} !important;
    }}
    
    /* ====== GRÁFICOS PLOTLY ====== */
    /* Fundo transparente nos gráficos */
    .js-plotly-plot {{
        background-color: transparent !important;
    }}
    
    /* ====== SIDEBAR ====== */
    /* Barra lateral de filtros */
    section[data-testid="stSidebar"] {{
        background-color: {CORES_INTERFACE["sidebar_background"]} !important;
        border-right: 1px solid {CORES_INTERFACE["sidebar_border"]} !important;
    }}
    
    section[data-testid="stSidebar"] * {{
        color: {CORES_INTERFACE["texto_principal"]} !important;
    }}
    
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] div {{
        color: {CORES_INTERFACE["texto_principal"]} !important;
    }}
    
    section[data-testid="stSidebar"] .stMultiSelect label,
    section[data-testid="stSidebar"] .stCheckbox label {{
        color: {CORES_INTERFACE["texto_principal"]} !important;
    }}
    
    section[data-testid="stSidebar"] label[data-testid="stWidgetLabel"] {{
        color: {CORES_INTERFACE["texto_principal"]} !important;
        font-weight: 600 !important;
    }}
    
    section[data-testid="stSidebar"] .stMarkdown small {{
        color: #cccccc !important;
    }}
    
    /* ====== UPLOAD DE ARQUIVO ====== */
    /* Área de upload na sidebar */
    section[data-testid="stSidebar"] .stFileUploader label {{
        color: {CORES_INTERFACE["texto_principal"]} !important;
    }}
    
    section[data-testid="stSidebar"] .stFileUploader {{
        color: {CORES_INTERFACE["texto_principal"]} !important;
    }}
    
    section[data-testid="stSidebar"] [data-testid="stFileUploader"] p,
    section[data-testid="stSidebar"] [data-testid="stFileUploader"] span,
    section[data-testid="stSidebar"] [data-testid="stFileUploader"] small {{
        color: #000000 !important;
    }}
    
    section[data-testid="stSidebar"] [data-testid="stFileUploadDropzone"] {{
        background-color: #ffffff !important;
    }}
    
    section[data-testid="stSidebar"] [data-testid="stFileUploadDropzone"] * {{
        color: #000000 !important;
    }}
    
    /* ====== BOTÕES ====== */
    /* Estilo dos botões */
    .stButton button {{
        background-color: {CORES_INTERFACE["botao_primary"]} !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        padding: 10px 20px !important;
        transition: all 0.3s !important;
    }}
    
    .stButton button:hover {{
        background-color: {CORES_INTERFACE["botao_hover"]} !important;
        box-shadow: 0 4px 12px rgba(33, 150, 243, 0.4) !important;
    }}
    
    /* ====== MÉTRICAS ====== */
    /* Esconde delta das métricas */
    div[data-testid="stMetricDelta"] {{
        display: none !important;
    }}
    
    /* ====== TEXTOS GERAIS ====== */
    /* Cor padrão dos textos */
    .stMarkdown, .stMarkdown p, .stMarkdown span, .stMarkdown div {{
        color: {CORES_INTERFACE["texto_principal"]} !important;
    }}
    
    .stInfo, .stWarning, .stSuccess, .stError {{
        color: {CORES_INTERFACE["texto_principal"]} !important;
    }}
    
    .stInfo *, .stWarning *, .stSuccess *, .stError * {{
        color: {CORES_INTERFACE["texto_principal"]} !important;
    }}
    
    h1, h2, h3, h4, h5, h6 {{
        color: {CORES_INTERFACE["texto_principal"]} !important;
    }}
    
    p {{
        color: {CORES_INTERFACE["texto_principal"]} !important;
    }}
    
    hr {{
        border-color: {CORES_INTERFACE["painel_border"]} !important;
    }}
    
    /* ====== ALERTAS ====== */
    /* Caixas de alerta */
    .alert-box {{
        background-color: {CORES_INTERFACE["sidebar_background"]};
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        border-left: 4px solid #ff5722;
    }}
    
    .alert-success {{
        border-left-color: {CORES_KPI["DISPONIVEIS"]["border"]};
    }}
    
    /* ====== DISPONIBILIDADE ====== */
    /* Display de taxa de disponibilidade */
    .availability-display {{
        background-color: {CORES_INTERFACE["sidebar_background"]};
        padding: 30px;
        border-radius: 8px;
        text-align: center;
    }}
    
    .availability-display h2 {{
        color: {CORES_KPI["DISPONIVEIS"]["text"]} !important;
        font-size: 3.5rem !important;
        font-weight: 700 !important;
        margin: 0 !important;
    }}
    
    .availability-display p {{
        color: {CORES_INTERFACE["texto_secundario"]} !important;
        font-size: 0.9rem !important;
        text-transform: uppercase !important;
        margin-top: 10px !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# =====================================================
# CONSTANTES E CONFIGURAÇÕES
# Listas de status aceitos para filtros
# =====================================================
STATUS_OFICIAIS = [
    "MANUTENÇÃO", 
    "DISPONÍVEIS NÃO TRIPULADO", 
    "CARREGADO", 
    "RETORNANDO DISPONÍVEIS", 
    "DISPONÍVEIS TRIPULADO", 
    "APOIO FILIAL"
]

STATUS_ADICIONAIS = [
    "INDISPONÍVEIS", 
    "FORA DE OPERAÇÃO", 
    "RETORNANDO INDISPONÍVEIS"
]

ORDEM_STATUS = STATUS_OFICIAIS + STATUS_ADICIONAIS

# =====================================================
# FUNÇÕES DE PROCESSAMENTO DE DADOS
# Limpeza e tratamento dos dados do Excel
# =====================================================
def renomear_colunas_duplicadas(df):
    """Renomeia colunas duplicadas (especialmente UF para UF_ORIGEM e UF_DESTINO)"""
    cols = pd.Series(df.columns)
    for dup in cols[cols.duplicated()].unique():
        dup_indices = [i for i, x in enumerate(cols) if x == dup]
        if dup == 'UF' and len(dup_indices) == 2:
            cols[dup_indices[0]] = 'UF_ORIGEM'
            cols[dup_indices[1]] = 'UF_DESTINO'
        else:
            for idx, position in enumerate(dup_indices):
                if idx > 0:
                    cols[position] = f"{dup}_{idx}"
    df.columns = cols
    return df

# =====================================================
# FUNÇÃO COM CACHE PARA CARREGAR DADOS
# Carrega e processa dados do Excel (com cache)
# =====================================================
@st.cache_data
def load_data_from_file(file_source):
    """
    Carrega arquivo Excel e processa dados
    file_source deve ser um objeto UploadedFile
    """
    try:
        # Lê Excel
        df = pd.read_excel(file_source, sheet_name="Frota Agro ")
        # Primeira linha como header
        df.columns = df.iloc[0]
        df = df[1:].reset_index(drop=True)
        # Renomeia duplicadas
        df = renomear_colunas_duplicadas(df)
        
        # Colunas para converter em texto
        colunas_texto = [
            "STATUS", "TIPO", "POSIÇÃO ATUAL", "PLACA", 
            "MOTORISTA", "OPERAÇÃO", "UF_ORIGEM", "UF_DESTINO", "DESTINO FINAL"
        ]
        
        # Padroniza texto: uppercase, remove espaços
        for col in colunas_texto:
            if col in df.columns:
                df[col] = (
                    df[col].astype(str).str.strip().str.upper()
                    .replace('NAN', pd.NA).replace('', pd.NA)
                )
        
        # Remove linhas sem status
        df = df[df["STATUS"].notna()]
        df = df[df["STATUS"] != ""]
        return df
    except Exception as e:
        st.error(f"❌ Erro ao carregar dados: {str(e)}")
        return pd.DataFrame()

def aplicar_cor_status(row):
    """Aplica cor de fundo nas linhas da tabela conforme status"""
    status = row["STATUS"]
    if status == "MANUTENÇÃO":
        return ['background-color: #3d1f1f; color: #ff5722'] * len(row)
    if "DISPONÍVEL" in status:
        return ['background-color: #1f3d1f; color: #4caf50'] * len(row)
    return ['background-color: #252525; color: #ffffff'] * len(row)

# =====================================================
# FUNÇÕES DE GRÁFICOS
# Criação de visualizações com Plotly
# =====================================================
def criar_grafico_status(status_df):
    """Gráfico horizontal de barras por status"""
    fig = go.Figure()
    for idx, row in status_df.iterrows():
        cor = CORES_STATUS.get(row["STATUS"], "#888888")
        fig.add_trace(go.Bar(
            y=[row["STATUS"]],
            x=[row["QUANTIDADE"]],
            orientation='h',
            marker=dict(color=cor),
            text=row["QUANTIDADE"],
            textposition='outside',
            textfont=dict(color='#ffffff', size=14, family='Arial Black'),
            hovertemplate='<b>%{y}</b><br>Quantidade: %{x}<extra></extra>',
            showlegend=False
        ))
    
    fig.update_layout(
        height=320,
        showlegend=False,
        margin=dict(l=0, r=40, t=10, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#ffffff', size=11),
        xaxis=dict(showgrid=True, gridcolor=CORES_INTERFACE["grid"], showline=False, zeroline=False, color=CORES_INTERFACE["texto_secundario"]),
        yaxis=dict(showgrid=False, showline=False, color='#ffffff', tickfont=dict(size=12))
    )
    return fig

def criar_grafico_tipo(tipo_df):
    """Gráfico vertical de barras por tipo de veículo"""
    fig = go.Figure()
    
    for idx, row in tipo_df.iterrows():
        fig.add_trace(go.Bar(
            x=[row["TIPO"]],
            y=[row["QUANTIDADE"]],
            marker=dict(color=CORES_TIPO_VEICULO[idx % len(CORES_TIPO_VEICULO)]),
            text=row["QUANTIDADE"],
            textposition='outside',
            textfont=dict(color='#ffffff', size=14, family='Arial Black'),
            hovertemplate='<b>%{x}</b><br>Quantidade: %{y}<extra></extra>',
            showlegend=False
        ))
    
    valor_max = tipo_df["QUANTIDADE"].max() if not tipo_df.empty else 10
    altura_minima = max(320, valor_max * 4 + 80)
    
    fig.update_layout(
        height=altura_minima,
        showlegend=False,
        margin=dict(l=0, r=0, t=30, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#ffffff'),
        xaxis=dict(showgrid=False, showline=False, color=CORES_INTERFACE["texto_secundario"], tickangle=0, tickfont=dict(size=10)),
        yaxis=dict(showgrid=True, gridcolor=CORES_INTERFACE["grid"], showline=False, zeroline=False, color=CORES_INTERFACE["texto_secundario"], range=[0, valor_max * 1.15])
    )
    return fig

def criar_grafico_posicao(posicao_df):
    """Gráfico de pizza (donut) por posição atual"""
    fig = go.Figure(data=[go.Pie(
        labels=posicao_df.head(10)["POSIÇÃO ATUAL"],
        values=posicao_df.head(10)["QUANTIDADE"],
        hole=0.6,
        marker=dict(colors=CORES_POSICAO),
        textfont=dict(color='#ffffff', size=12),
        textinfo='value',
        hovertemplate='<b>%{label}</b><br>Quantidade: %{value}<extra></extra>'
    )])
    
    fig.update_layout(
        height=320,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=True,
        legend=dict(
            orientation="v", yanchor="middle", y=0.5,
            xanchor="left", x=1.02,
            font=dict(color='#ffffff', size=10),
            bgcolor='rgba(0,0,0,0)'
        )
    )
    return fig

def criar_grafico_uf_origem(uf_df):
    """Gráfico vertical de barras por UF de origem"""
    fig = go.Figure()
    
    for idx, row in uf_df.iterrows():
        fig.add_trace(go.Bar(
            x=[row["UF_ORIGEM"]],
            y=[row["QUANTIDADE"]],
            marker=dict(color=CORES_UF[idx % len(CORES_UF)]),
            text=row["QUANTIDADE"],
            textposition='outside',
            textfont=dict(color='#ffffff', size=14, family='Arial Black'),
            hovertemplate='<b>%{x}</b><br>Veículos: %{y}<extra></extra>',
            showlegend=False
        ))
    
    valor_max = uf_df["QUANTIDADE"].max() if not uf_df.empty else 10
    altura_minima = max(320, valor_max * 4 + 80)
    
    fig.update_layout(
        height=altura_minima,
        showlegend=False,
        margin=dict(l=0, r=0, t=30, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#ffffff'),
        xaxis=dict(showgrid=False, showline=False, color=CORES_INTERFACE["texto_secundario"], tickangle=0, tickfont=dict(size=11)),
        yaxis=dict(showgrid=True, gridcolor=CORES_INTERFACE["grid"], showline=False, zeroline=False, color=CORES_INTERFACE["texto_secundario"], range=[0, valor_max * 1.15])
    )
    return fig

# =====================================================
# FUNÇÕES DE INTERFACE
# Componentes visuais da aplicação
# =====================================================
def criar_header(taxa_disponibilidade=0.0):
    """Cabeçalho principal com sirene animada e taxa de disponibilidade"""
    # Carrega a logo em base64
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
        <div class="header-left">
            <p><span class="status-dot"></span>ATUALIZADO EM: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}</p>
        </div>
        <div class="header-center">
            {logo_html}
        </div>
        <div class="mini-disponibilidade">
            <div class="mini-label">DISPONIBILIDADE</div>
            <div class="mini-valor">{taxa_disponibilidade:.1f}%</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def criar_kpis(df_filtrado):
    """
    KPIs principais: Total, Em Operação, Disponíveis, Manutenção
    Usa HTML customizado para manter cores corretas
    """
    total = len(df_filtrado)
    em_operacao = len(df_filtrado[df_filtrado["STATUS"].isin(["CARREGADO", "RETORNANDO DISPONÍVEIS"])])
    disponiveis = len(df_filtrado[df_filtrado["STATUS"].isin(["DISPONÍVEIS TRIPULADO", "DISPONÍVEIS NÃO TRIPULADO"])])
    manutencao = len(df_filtrado[df_filtrado["STATUS"] == "MANUTENÇÃO"])

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="kpi-card kpi-azul">
            <div class="kpi-label">TOTAL DE VEÍCULOS</div>
            <div class="kpi-value">{total}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="kpi-card kpi-laranja">
            <div class="kpi-label">EM OPERAÇÃO</div>
            <div class="kpi-value">{em_operacao}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="kpi-card kpi-verde">
            <div class="kpi-label">DISPONÍVEIS</div>
            <div class="kpi-value">{disponiveis}</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="kpi-card kpi-vermelho">
            <div class="kpi-label">MANUTENÇÃO</div>
            <div class="kpi-value">{manutencao}</div>
        </div>
        """, unsafe_allow_html=True)

    return em_operacao, disponiveis, manutencao

def criar_sidebar(main_loading_placeholder):
    """Barra lateral com upload de arquivo e filtros"""
    with st.sidebar:
        st.header("🎛️ FILTROS OPERACIONAIS")
        st.divider()
        
        # ===== UPLOAD MANUAL OBRIGATÓRIO =====
        st.subheader("📁 CARREGAR ARQUIVO")
        
        uploaded_file = st.file_uploader(
            "Faça upload do arquivo Excel",
            type=['xlsx', 'xls'],
            help="Selecione o arquivo da planilha de frota"
        )
        
        df_base = pd.DataFrame()
        
        # Só processa se houver arquivo
        if uploaded_file is not None:
            show_loading_screen(main_loading_placeholder)
            df_base = load_data_from_file(uploaded_file)
            main_loading_placeholder.empty()
            
            if not df_base.empty:
                st.success("✅ Arquivo carregado com sucesso!")
        
        st.divider()
        
        # Se não há dados, retorna vazios
        if df_base.empty:
            st.info("⬆️ Faça upload de um arquivo Excel para visualizar os dados.")
            return pd.DataFrame(), [], [], [], []
        
        # Checkbox para incluir todos status
        incluir_todos_status = st.checkbox("📋 Incluir TODOS os STATUS", value=False)
        
        if incluir_todos_status:
            STATUS_PARA_USAR = STATUS_OFICIAIS + STATUS_ADICIONAIS
        else:
            STATUS_PARA_USAR = STATUS_OFICIAIS
        
        # Filtra base pelos status permitidos
        df_base_filtrado = df_base[df_base["STATUS"].isin(STATUS_PARA_USAR)].copy()
        
        # Filtro de Status
        status_disponiveis = sorted([s for s in df_base_filtrado["STATUS"].unique() if s in STATUS_PARA_USAR])
        status_sel = st.multiselect("📊 STATUS", status_disponiveis, default=status_disponiveis)
        
        # Filtro de Tipo
        tipos_disponiveis = sorted([t for t in df_base_filtrado["TIPO"].unique() if pd.notna(t) and t != ""])
        tipo_sel = st.multiselect("🚛 TIPO DE VEÍCULO", tipos_disponiveis, default=tipos_disponiveis)
        
        # Filtro de Posição
        posicoes_disponiveis = sorted([p for p in df_base_filtrado["POSIÇÃO ATUAL"].unique() if pd.notna(p) and p != ""])
        pos_sel = st.multiselect("📍 POSIÇÃO ATUAL", posicoes_disponiveis, default=posicoes_disponiveis)
        
        # Filtro de UF
        if "UF_ORIGEM" in df_base_filtrado.columns:
            ufs_disponiveis = sorted([u for u in df_base_filtrado["UF_ORIGEM"].unique() if pd.notna(u) and u != ""])
            uf_sel = st.multiselect("🗺️ UF DE ORIGEM", ufs_disponiveis, default=ufs_disponiveis)
        else:
            uf_sel = []
        
        # Botão atualizar manual
        if st.button("🔄 ATUALIZAR DADOS AGORA", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
        
        return df_base_filtrado, status_sel, tipo_sel, pos_sel, uf_sel

def criar_painel_status(status_df):
    """Painel com gráfico de distribuição por status"""
    with st.container(border=True):
        st.markdown('<div class="card-title">📊 STATUS DA FROTA</div>', unsafe_allow_html=True)
        fig_status = criar_grafico_status(status_df)
        st.plotly_chart(fig_status, use_container_width=True, config={'displayModeBar': False})

def criar_painel_uf(uf_df):
    """Painel com gráfico de distribuição por UF de origem"""
    with st.container(border=True):
        st.markdown('<div class="card-title">🗺️ DISTRIBUIÇÃO POR UF (ORIGEM)</div>', unsafe_allow_html=True)
        fig_uf = criar_grafico_uf_origem(uf_df)
        st.plotly_chart(fig_uf, use_container_width=True, config={'displayModeBar': False})

def criar_painel_tipo(tipo_df):
    """Painel com gráfico de distribuição por tipo de veículo"""
    with st.container(border=True):
        st.markdown('<div class="card-title">🚛 TIPO DE VEÍCULO</div>', unsafe_allow_html=True)
        fig_tipo = criar_grafico_tipo(tipo_df)
        st.plotly_chart(fig_tipo, use_container_width=True, config={'displayModeBar': False})

def criar_painel_posicao(posicao_df):
    """Painel com gráfico pizza de posições atuais"""
    with st.container(border=True):
        st.markdown('<div class="card-title">📍 POSIÇÃO ATUAL</div>', unsafe_allow_html=True)
        fig_pos = criar_grafico_posicao(posicao_df)
        st.plotly_chart(fig_pos, use_container_width=True, config={'displayModeBar': False})

def criar_tabela_detalhada(df_filtrado):
    """Tabela detalhada com todos os veículos filtrados"""
    with st.container(border=True):
        st.markdown('<div class="card-title">📋 DETALHAMENTO COMPLETO DA FROTA</div>', unsafe_allow_html=True)
        
        # Seleciona colunas para exibir
        colunas_exibir = ["PLACA", "STATUS", "TIPO", "POSIÇÃO ATUAL"]
        
        if "UF_ORIGEM" in df_filtrado.columns:
            colunas_exibir.append("UF_ORIGEM")
        if "DESTINO FINAL" in df_filtrado.columns:
            colunas_exibir.append("DESTINO FINAL")
        if "UF_DESTINO" in df_filtrado.columns:
            colunas_exibir.append("UF_DESTINO")
        
        colunas_exibir.append("MOTORISTA")
        
        df_display = df_filtrado[colunas_exibir].copy()
        
        # Tabela com cores por status
        st.dataframe(
            df_display.style.apply(aplicar_cor_status, axis=1),
            hide_index=True,
            use_container_width=True,
            height=400
        )

# =====================================================
# FUNÇÃO PRINCIPAL
# Orquestra toda a aplicação
# =====================================================
def main():
    # Carrega CSS
    load_custom_css()
    
    # Placeholder global para tela de loading
    loading_placeholder = st.empty()
    
    # Cria sidebar e processa upload
    df_base_filtrado, status_sel, tipo_sel, pos_sel, uf_sel = criar_sidebar(loading_placeholder)
    
    # Se não houver dados, para execução
    if df_base_filtrado.empty:
        st.warning("⚠️ Por favor, carregue um arquivo Excel na barra lateral para visualizar os dados.")
        st.stop()
    
    # Aplica filtros selecionados
    filtro_aplicado = (
        (df_base_filtrado["STATUS"].isin(status_sel)) &
        (df_base_filtrado["TIPO"].isin(tipo_sel)) &
        (df_base_filtrado["POSIÇÃO ATUAL"].isin(pos_sel))
    )
    
    if "UF_ORIGEM" in df_base_filtrado.columns and uf_sel:
        filtro_aplicado = filtro_aplicado & (df_base_filtrado["UF_ORIGEM"].isin(uf_sel))
    
    df_filtrado = df_base_filtrado[filtro_aplicado].copy()
    
    # Calcula taxa de disponibilidade
    manutencao_count = len(df_filtrado[df_filtrado["STATUS"] == "MANUTENÇÃO"])
    taxa_disponibilidade = ((len(df_filtrado) - manutencao_count) / len(df_filtrado) * 100) if len(df_filtrado) > 0 else 0.0

    # Cria header
    criar_header(taxa_disponibilidade)
    
    # Cria KPIs
    em_operacao, disponiveis, manutencao = criar_kpis(df_filtrado)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Prepara DataFrames para gráficos
    status_counts = df_filtrado["STATUS"].value_counts()
    status_df = pd.DataFrame({
        "STATUS": [s for s in ORDEM_STATUS if s in status_counts.index],
        "QUANTIDADE": [status_counts.get(s, 0) for s in ORDEM_STATUS if s in status_counts.index]
    })
    status_df = status_df[status_df["QUANTIDADE"] > 0]
    
    tipo_df = df_filtrado["TIPO"].value_counts().reset_index().rename(columns={"count": "QUANTIDADE"})
    posicao_df = df_filtrado["POSIÇÃO ATUAL"].value_counts().reset_index().rename(columns={"count": "QUANTIDADE"})
    
    if "UF_ORIGEM" in df_filtrado.columns:
        uf_origem_df = (
            df_filtrado["UF_ORIGEM"]
            .value_counts()
            .reset_index()
            .rename(columns={"count": "QUANTIDADE"})
        )
    else:
        uf_origem_df = pd.DataFrame()
    
    # ========== PRIMEIRA LINHA DE PAINÉIS ==========
    # Status e Posição
    col_graf1, col_graf2 = st.columns(2)
    
    with col_graf1:
        criar_painel_status(status_df)
    
    with col_graf2:
        criar_painel_posicao(posicao_df)
    
    # ========== SEGUNDA LINHA DE PAINÉIS ==========
    # Tipo e UF
    st.markdown("<br>", unsafe_allow_html=True)
    col_graf4, col_graf5 = st.columns(2)
    
    with col_graf4:
        criar_painel_tipo(tipo_df)
    
    with col_graf5:
        if not uf_origem_df.empty:
            criar_painel_uf(uf_origem_df)
    
    # Tabela detalhada
    st.markdown("<br>", unsafe_allow_html=True)
    criar_tabela_detalhada(df_filtrado)

# =====================================================
# EXECUÇÃO
# Ponto de entrada do programa
# =====================================================
if __name__ == "__main__":
    main()
