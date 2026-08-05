import streamlit as st

st.set_page_config(
    page_title="ERP Nexus",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

from database import init_db
from seed_data import seed
from utils.theme import apply_theme, section_header
from utils.auth import login_form, logout, show_user_info, require_login
from utils.dashboard import kpi_cards, sales_chart, stock_alert_chart, campaign_chart, cashflow_forecast

apply_theme()

@st.cache_resource
def setup_database():
    init_db()
    seed()
    return True

setup_database()

# ============================================================
# ESTILOS GLOBALES PROFESIONALES
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
}

/* Ocultar elementos por defecto de Streamlit que rompen el diseño */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display: none !important;}

/* Scrollbar elegante */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #94a3b8; }

/* Inputs profesionales */
.stTextInput > div > div > input,
.stTextInput > div > div > input:focus {
    border-radius: 10px !important;
    border: 1.5px solid #e2e8f0 !important;
    padding: 10px 14px !important;
    font-size: 0.9rem !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
.stTextInput > div > div > input:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.1) !important;
}

/* Botones primarios */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 18px !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    box-shadow: 0 4px 14px rgba(99,102,241,0.35) !important;
    transition: transform 0.15s, box-shadow 0.15s !important;
}
.stButton > button[kind="primary"]:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(99,102,241,0.45) !important;
}

/* Botones secundarios */
.stButton > button[kind="secondary"] {
    background: white !important;
    color: #475569 !important;
    border: 1.5px solid #e2e8f0 !important;
    border-radius: 10px !important;
    padding: 10px 16px !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    transition: all 0.15s !important;
}
.stButton > button[kind="secondary"]:hover {
    background: #f1f5f9 !important;
    border-color: #cbd5e1 !important;
}

/* Sidebar profesional */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%) !important;
    box-shadow: 4px 0 24px rgba(0,0,0,0.15) !important;
    min-width: 260px !important;
    max-width: 260px !important;
}
[data-testid="stSidebar"] .stRadio > div {
    display: flex;
    flex-direction: column;
    gap: 2px;
}
[data-testid="stSidebar"] .stRadio label {
    display: flex !important;
    align-items: center !important;
    gap: 11px !important;
    padding: 10px 14px !important;
    margin: 0 !important;
    border-radius: 10px !important;
    color: #94a3b8 !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    border-left: 3px solid transparent !important;
}
[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(255,255,255,0.06) !important;
    color: #e2e8f0 !important;
}
[data-testid="stSidebar"] .stRadio [data-testid="stWidgetLabel"] {
    display: none !important;
}
[data-testid="stSidebar"] .stRadio > div > div > label[data-baseweb="radio"] > div:first-child {
    display: none !important;
}
[data-testid="stSidebar"] .stRadio > div > div:has(input:checked) label {
    background: linear-gradient(90deg, rgba(99,102,241,0.2) 0%, rgba(99,102,241,0.05) 100%) !important;
    color: #818cf8 !important;
    border-left: 3px solid #6366f1 !important;
    font-weight: 600 !important;
}

/* Main content */
.block-container {
    padding: 28px 32px !important;
    max-width: none !important;
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# LOGIN SCREEN PROFESIONAL
# ============================================================
if "user" not in st.session_state:
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #e0e7ff 50%, #f0fdf4 100%) !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.1, 1])
    with col2:
        st.markdown("<div style='height:12vh'></div>", unsafe_allow_html=True)
        
        # Tarjeta de login flotante
        st.markdown("""
        <div style="
            background: white;
            padding: 48px 40px;
            border-radius: 24px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.08), 0 0 0 1px rgba(0,0,0,0.03);
            text-align: center;
        ">
            <div style="
                width: 56px; height: 56px;
                background: linear-gradient(135deg, #6366f1, #8b5cf6);
                border-radius: 14px;
                display: inline-flex; align-items: center; justify-content: center;
                color: white; font-weight: 800; font-size: 1.4rem;
                margin-bottom: 20px;
                box-shadow: 0 8px 24px rgba(99,102,241,0.35);
            ">N</div>
            <h1 style="
                font-size: 1.4rem; font-weight: 800; color: #0f172a;
                margin: 0; letter-spacing: -0.02em;
            ">ERP Nexus</h1>
            <p style="color: #64748b; font-size: 0.9rem; margin: 6px 0 0 0;">
                Sistema de gestión empresarial
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        login_form()
        
        st.markdown("""
        <div style="text-align:center; margin-top:1.5rem;">
            <p style="color: #94a3b8; font-size: 0.78rem; font-weight: 500;">
                Demo: <b style="color:#64748b;">admin</b>/admin · 
                <b style="color:#64748b;">ventas</b>/ventas · 
                <b style="color:#64748b;">almacen</b>/almacen
            </p>
        </div>
        """, unsafe_allow_html=True)
    st.stop()

require_login()


# ============================================================
# SIDEBAR PROFESIONAL
# ============================================================
with st.sidebar:
    # Brand header
    st.markdown("""
    <div style="padding: 24px 20px 20px; border-bottom: 1px solid rgba(255,255,255,0.06); margin-bottom: 4px;">
        <div style="display: flex; align-items: center; gap: 12px;">
            <div style="
                width: 38px; height: 38px;
                background: linear-gradient(135deg, #6366f1, #8b5cf6);
                border-radius: 10px;
                display: flex; align-items: center; justify-content: center;
                color: white; font-weight: 800; font-size: 1.1rem;
                box-shadow: 0 4px 12px rgba(99,102,241,0.4);
            ">N</div>
            <div>
                <div style="color: #f1f5f9; font-weight: 700; font-size: 1.05rem; letter-spacing: -0.02em;">
                    ERP Nexus
                </div>
                <div style="color: #64748b; font-size: 0.7rem; margin-top: 1px;">v1.0 Professional</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # User card
    user = st.session_state.get("user", {})
    user_name = user.get("name", "Usuario")
    user_role = user.get("role", "Usuario")
    user_initial = user_name[0].upper() if user_name else "U"
    
    st.markdown(f"""
    <div style="
        margin: 14px 12px 8px;
        padding: 14px;
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 12px;
        display: flex; align-items: center; gap: 10px;
    ">
        <div style="
            width: 36px; height: 36px;
            background: linear-gradient(135deg, #10b981, #059669);
            border-radius: 50%;
            display: flex; align-items: center; justify-content: center;
            color: white; font-weight: 600; font-size: 0.85rem;
        ">{user_initial}</div>
        <div>
            <div style="color: #e2e8f0; font-weight: 600; font-size: 0.85rem;">{user_name}</div>
            <div style="color: #94a3b8; font-size: 0.72rem;">{user_role.capitalize()}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation
    page = st.radio("", [
        "🏠 Dashboard",
        "📦 Inventario",
        "💶 Ventas",
        "📋 Compras",
        "💼 Finanzas",
        "🤝 CRM",
        "📢 Marketing",
        "🏦 Banca",
        "🤖 Agentes",
        "🔌 Integraciones",
        "👥 RRHH",
    ], key="nav", label_visibility="collapsed")
    
    # Footer sidebar
    st.markdown("<div style='flex:1;'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="
        padding: 14px;
        border-top: 1px solid rgba(255,255,255,0.06);
        display: flex; align-items: center; justify-content: space-between;
    ">
    """, unsafe_allow_html=True)
    logout()
    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# MAIN CONTENT CON HEADER PROFESIONAL
# ============================================================
def page_header(title: str, subtitle: str):
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"""
        <div style="margin-bottom: 24px; padding-bottom: 20px; border-bottom: 1px solid #e2e8f0;">
            <h1 style="
                font-size: 1.6rem; font-weight: 800; color: #0f172a;
                margin: 0; letter-spacing: -0.03em; line-height: 1.2;
            ">{title}</h1>
            <p style="
                color: #64748b; font-size: 0.9rem; font-weight: 400;
                margin: 4px 0 0 0;
            ">{subtitle}</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.button("📅 Este mes", type="secondary", use_container_width=True)
        with c2:
            st.button("+ Nuevo", type="primary", use_container_width=True)


# ============================================================
# PÁGINAS
# ============================================================
if page == "🏠 Dashboard":
    page_header("Dashboard", "Visión general de tu empresa en tiempo real")
    kpi_cards()
    
    col1, col2 = st.columns([1.2, 1])
    with col1:
        sales_chart()
    with col2:
        stock_alert_chart()
    
    campaign_chart()
    cashflow_forecast()

elif page == "📦 Inventario":
    from modules import inventario
    inventario.show()

elif page == "💶 Ventas":
    from modules import ventas
    ventas.show()

elif page == "📋 Compras":
    from modules import compras
    compras.show()

elif page == "💼 Finanzas":
    from modules import finanzas
    finanzas.show()

elif page == "🤝 CRM":
    from modules import crm
    crm.show()

elif page == "📢 Marketing":
    from modules import marketing
    marketing.show()

elif page == "🏦 Banca":
    from modules import banca
    banca.show()

elif page == "🤖 Agentes":
    from modules import agentes
    agentes.show()

elif page == "🔌 Integraciones":
    from modules import integraciones
    integraciones.show()

elif page == "👥 RRHH":
    from modules import rrhh
    rrhh.show()
