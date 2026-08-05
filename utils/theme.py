import streamlit as st

def apply_theme():
    """Aplica estilos CSS profesionales al ERP"""
    st.markdown("""
    <style>
    /* Fuentes y colores corporativos */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    :root {
        --primary: #1e3a5f;
        --primary-light: #2d5a8f;
        --accent: #00b4d8;
        --success: #10b981;
        --warning: #f59e0b;
        --danger: #ef4444;
        --bg: #f8fafc;
        --card: #ffffff;
        --text: #1e293b;
        --text-muted: #64748b;
        --border: #e2e8f0;
    }

    /* Reset y base */
    .stApp {
        font-family: 'Inter', sans-serif !important;
        background: var(--bg) !important;
    }

    /* Sidebar profesional */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e3a5f 0%, #0f1f33 100%) !important;
        border-right: none !important;
    }

    [data-testid="stSidebar"] .stRadio label {
        color: rgba(255,255,255,0.85) !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
        padding: 0.5rem 0.75rem !important;
        border-radius: 0.5rem !important;
        transition: all 0.2s !important;
    }

    [data-testid="stSidebar"] .stRadio label:hover {
        background: rgba(255,255,255,0.1) !important;
        color: white !important;
    }

    [data-testid="stSidebar"] .stRadio [role="radiogroup"] > div > div {
        background: rgba(0,180,216,0.2) !important;
        border-radius: 0.5rem !important;
    }

    /* Headers */
    h1, h2, h3 {
        font-family: 'Inter', sans-serif !important;
        color: var(--primary) !important;
        font-weight: 700 !important;
    }

    h1 {
        font-size: 1.8rem !important;
        margin-bottom: 1.5rem !important;
    }

    /* Cards / Containers */
    [data-testid="stVerticalBlock"] > div > div[data-testid="stVerticalBlock"] {
        gap: 1rem !important;
    }

    div[data-testid="stMetric"] {
        background: var(--card) !important;
        border: 1px solid var(--border) !important;
        border-radius: 1rem !important;
        padding: 1.25rem !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
        transition: transform 0.2s, box-shadow 0.2s !important;
    }

    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08) !important;
    }

    div[data-testid="stMetric"] label {
        font-size: 0.75rem !important;
        font-weight: 600 !important;
        color: var(--text-muted) !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }

    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        font-size: 1.5rem !important;
        font-weight: 700 !important;
        color: var(--primary) !important;
    }

    /* Botones */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 0.75rem !important;
        padding: 0.6rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        transition: all 0.2s !important;
        box-shadow: 0 2px 8px rgba(30,58,95,0.25) !important;
    }

    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 16px rgba(30,58,95,0.35) !important;
    }

    .stButton > button:active {
        transform: translateY(0) !important;
    }

    /* Formularios */
    [data-testid="stForm"] {
        background: var(--card) !important;
        border: 1px solid var(--border) !important;
        border-radius: 1rem !important;
        padding: 1.5rem !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
    }

    /* Inputs */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > div {
        border-radius: 0.5rem !important;
        border: 1px solid var(--border) !important;
        padding: 0.6rem 0.8rem !important;
        font-size: 0.9rem !important;
    }

    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 3px rgba(0,180,216,0.15) !important;
    }

    /* Tablas */
    .stDataFrame {
        border-radius: 1rem !important;
        overflow: hidden !important;
        border: 1px solid var(--border) !important;
    }

    .stDataFrame thead tr {
        background: var(--primary) !important;
    }

    .stDataFrame thead th {
        color: white !important;
        font-weight: 600 !important;
        font-size: 0.8rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        padding: 0.75rem 1rem !important;
    }

    .stDataFrame tbody tr:nth-child(even) {
        background: #f8fafc !important;
    }

    .stDataFrame tbody tr:hover {
        background: #e0f2fe !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem !important;
        border-bottom: 2px solid var(--border) !important;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 0.5rem 0.5rem 0 0 !important;
        padding: 0.75rem 1.25rem !important;
        font-weight: 600 !important;
        color: var(--text-muted) !important;
    }

    .stTabs [aria-selected="true"] {
        color: var(--primary) !important;
        background: rgba(0,180,216,0.1) !important;
        border-bottom: 2px solid var(--accent) !important;
    }

    /* Expanders */
    .streamlit-expanderHeader {
        background: var(--card) !important;
        border: 1px solid var(--border) !important;
        border-radius: 0.75rem !important;
        font-weight: 600 !important;
        color: var(--primary) !important;
    }

    /* Info/Warning/Success boxes */
    .stAlert {
        border-radius: 0.75rem !important;
        border: none !important;
    }

    /* Ocultar el menú de hamburguesa y footer de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Scrollbar bonita */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #f1f5f9;
    }
    ::-webkit-scrollbar-thumb {
        background: #cbd5e1;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #94a3b8;
    }
    </style>
    """, unsafe_allow_html=True)

def kpi_card(title, value, icon="📊", delta=None, color="#1e3a5f"):
    """Renderiza una tarjeta KPI estilizada"""
    delta_html = f'<div style="font-size:0.85rem;color:{"#10b981" if delta and delta.startswith("+") else "#ef4444"};font-weight:600;">{delta}</div>' if delta else ""
    st.markdown(f"""
    <div style="background:white;border:1px solid #e2e8f0;border-radius:1rem;padding:1.25rem;box-shadow:0 1px 3px rgba(0,0,0,0.05);transition:all 0.2s;" onmouseover="this.style.transform='translateY(-2px)';this.style.boxShadow='0 4px 12px rgba(0,0,0,0.08)';" onmouseout="this.style.transform='translateY(0)';this.style.boxShadow='0 1px 3px rgba(0,0,0,0.05)';">
        <div style="display:flex;align-items:center;gap:0.75rem;margin-bottom:0.5rem;">
            <div style="width:40px;height:40px;border-radius:0.75rem;background:{color}15;display:flex;align-items:center;justify-content:center;font-size:1.25rem;">{icon}</div>
            <div style="font-size:0.75rem;font-weight:600;color:#64748b;text-transform:uppercase;letter-spacing:0.05em;">{title}</div>
        </div>
        <div style="font-size:1.5rem;font-weight:700;color:#1e293b;margin-left:3.25rem;">{value}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)

def section_header(title, subtitle=""):
    """Renderiza un header de sección profesional"""
    st.markdown(f"""
    <div style="margin-bottom:1.5rem;">
        <h2 style="color:#1e3a5f;font-size:1.4rem;font-weight:700;margin-bottom:0.25rem;">{title}</h2>
        {f'<p style="color:#64748b;font-size:0.9rem;margin:0;">{subtitle}</p>' if subtitle else ''}
    </div>
    <hr style="border:none;border-top:1px solid #e2e8f0;margin-bottom:1.5rem;">
    """, unsafe_allow_html=True)

def status_pill(status, color):
    """Renderiza una pastilla de estado"""
    return f'<span style="background:{color}15;color:{color};padding:0.25rem 0.75rem;border-radius:9999px;font-size:0.75rem;font-weight:600;">{status}</span>'
