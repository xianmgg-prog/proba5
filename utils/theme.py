import streamlit as st

def apply_theme():
    """Tema corporativo sobrio - estilo Notion/SAP"""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    :root {
        --bg: #fafafa;
        --surface: #ffffff;
        --border: #e5e7eb;
        --text: #111827;
        --text-secondary: #6b7280;
        --accent: #1f2937;
        --accent-light: #374151;
        --success: #065f46;
        --warning: #92400e;
        --danger: #991b1b;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    .stApp {
        background: var(--bg) !important;
    }

    /* Sidebar - gris oscuro plano */
    [data-testid="stSidebar"] {
        background: #111827 !important;
        border-right: 1px solid #1f2937 !important;
    }

    [data-testid="stSidebar"] .stRadio label {
        color: #9ca3af !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        padding: 0.5rem 0.75rem !important;
        border-radius: 0.375rem !important;
        margin: 0.125rem 0 !important;
        transition: none !important;
    }

    [data-testid="stSidebar"] .stRadio label:hover {
        color: #f3f4f6 !important;
        background: #1f2937 !important;
    }

    [data-testid="stSidebar"] .stRadio [role="radiogroup"] > div > div {
        background: #1f2937 !important;
        border-radius: 0.375rem !important;
    }

    [data-testid="stSidebar"] .stRadio [role="radiogroup"] > div > div > div {
        color: #f3f4f6 !important;
        font-weight: 600 !important;
    }

    /* Headers */
    h1 {
        font-size: 1.5rem !important;
        font-weight: 700 !important;
        color: #111827 !important;
        letter-spacing: -0.025em !important;
        margin-bottom: 0.5rem !important;
    }

    h2 {
        font-size: 1.125rem !important;
        font-weight: 600 !important;
        color: #374151 !important;
        margin-top: 1.5rem !important;
        margin-bottom: 0.75rem !important;
    }

    h3 {
        font-size: 1rem !important;
        font-weight: 600 !important;
        color: #4b5563 !important;
    }

    /* KPI Cards - planos, bordes sutiles */
    div[data-testid="stMetric"] {
        background: var(--surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: 0.5rem !important;
        padding: 1rem !important;
    }

    div[data-testid="stMetric"] label {
        font-size: 0.7rem !important;
        font-weight: 600 !important;
        color: #6b7280 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }

    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        font-size: 1.375rem !important;
        font-weight: 700 !important;
        color: #111827 !important;
    }

    /* Botones - planos, sin gradientes */
    .stButton > button {
        background: #111827 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 0.375rem !important;
        padding: 0.5rem 1.25rem !important;
        font-weight: 500 !important;
        font-size: 0.875rem !important;
        transition: background 0.15s !important;
    }

    .stButton > button:hover {
        background: #374151 !important;
    }

    .stButton > button:active {
        background: #1f2937 !important;
    }

    /* Formularios */
    [data-testid="stForm"] {
        background: var(--surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: 0.5rem !important;
        padding: 1.25rem !important;
    }

    /* Inputs */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > div {
        border-radius: 0.375rem !important;
        border: 1px solid #d1d5db !important;
        padding: 0.5rem 0.75rem !important;
        font-size: 0.875rem !important;
        background: #ffffff !important;
    }

    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: #111827 !important;
        box-shadow: 0 0 0 1px #111827 !important;
    }

    /* Tablas */
    .stDataFrame {
        border-radius: 0.5rem !important;
        border: 1px solid var(--border) !important;
    }

    .stDataFrame thead tr {
        background: #f9fafb !important;
    }

    .stDataFrame thead th {
        color: #374151 !important;
        font-weight: 600 !important;
        font-size: 0.75rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.025em !important;
        padding: 0.625rem 1rem !important;
        border-bottom: 1px solid #e5e7eb !important;
    }

    .stDataFrame tbody tr {
        border-bottom: 1px solid #f3f4f6 !important;
    }

    .stDataFrame tbody tr:hover {
        background: #f9fafb !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0 !important;
        border-bottom: 1px solid #e5e7eb !important;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 0 !important;
        padding: 0.625rem 1rem !important;
        font-weight: 500 !important;
        font-size: 0.875rem !important;
        color: #6b7280 !important;
        border-bottom: 2px solid transparent !important;
    }

    .stTabs [aria-selected="true"] {
        color: #111827 !important;
        border-bottom: 2px solid #111827 !important;
        background: transparent !important;
    }

    /* Expanders */
    .streamlit-expanderHeader {
        background: var(--surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: 0.5rem !important;
        font-weight: 500 !important;
        color: #374151 !important;
        font-size: 0.875rem !important;
    }

    /* Info/Warning boxes */
    .stAlert {
        border-radius: 0.5rem !important;
        border: 1px solid !important;
    }

    .stAlert[data-baseweb="notification"][kind="info"] {
        background: #eff6ff !important;
        border-color: #bfdbfe !important;
        color: #1e40af !important;
    }

    .stAlert[data-baseweb="notification"][kind="warning"] {
        background: #fffbeb !important;
        border-color: #fde68a !important;
        color: #92400e !important;
    }

    .stAlert[data-baseweb="notification"][kind="success"] {
        background: #ecfdf5 !important;
        border-color: #a7f3d0 !important;
        color: #065f46 !important;
    }

    /* Ocultar menú y footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Scrollbar minimal */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: #d1d5db; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #9ca3af; }
    </style>
    """, unsafe_allow_html=True)

def kpi_card(title, value, icon="", subtitle=""):
    """Tarjeta KPI minimalista"""
    sub = f'<div style="font-size:0.75rem;color:#6b7280;margin-top:0.25rem;">{subtitle}</div>' if subtitle else ""
    st.markdown(f"""
    <div style="background:#ffffff;border:1px solid #e5e7eb;border-radius:0.5rem;padding:1rem;">
        <div style="font-size:0.7rem;font-weight:600;color:#6b7280;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:0.5rem;">{title}</div>
        <div style="font-size:1.375rem;font-weight:700;color:#111827;">{value}</div>
        {sub}
    </div>
    """, unsafe_allow_html=True)

def section_header(title, subtitle=""):
    """Header de sección corporativo"""
    sub = f'<p style="color:#6b7280;font-size:0.875rem;margin:0.25rem 0 0 0;">{subtitle}</p>' if subtitle else ""
    st.markdown(f"""
    <div style="margin-bottom:1.25rem;">
        <h1 style="font-size:1.5rem;font-weight:700;color:#111827;letter-spacing:-0.025em;margin:0;">{title}</h1>
        {sub}
    </div>
    """, unsafe_allow_html=True)

def status_badge(status):
    """Badge de estado minimalista"""
    colors = {
        "borrador": ("#f3f4f6", "#374151"),
        "pendiente": ("#fef3c7", "#92400e"),
        "aprobada": ("#d1fae5", "#065f46"),
        "recibida": ("#dbeafe", "#1e40af"),
        "cancelada": ("#fee2e2", "#991b1b"),
        "enviada": ("#fef3c7", "#92400e"),
        "pagada": ("#d1fae5", "#065f46"),
        "vencida": ("#fee2e2", "#991b1b"),
        "anulada": ("#f3f4f6", "#6b7280"),
        "activa": ("#d1fae5", "#065f46"),
        "pausada": ("#fef3c7", "#92400e"),
        "pendiente": ("#fef3c7", "#92400e"),
        "aprobada": ("#d1fae5", "#065f46"),
        "rechazada": ("#fee2e2", "#991b1b"),
        "ejecutada": ("#dbeafe", "#1e40af"),
    }
    bg, fg = colors.get(status.lower(), ("#f3f4f6", "#374151"))
    return f'<span style="background:{bg};color:{fg};padding:0.125rem 0.5rem;border-radius:0.25rem;font-size:0.7rem;font-weight:600;text-transform:uppercase;letter-spacing:0.025em;">{status}</span>'
