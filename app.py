import streamlit as st
st.set_page_config(page_title="ERP Nexus — Gestión Empresarial", page_icon="🏢", layout="wide", initial_sidebar_state="expanded")

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

# Login screen profesional
if "user" not in st.session_state:
    st.markdown("""
    <div style="max-width:420px;margin:8vh auto 0 auto;text-align:center;">
        <div style="width:64px;height:64px;background:linear-gradient(135deg,#1e3a5f,#2d5a8f);border-radius:16px;display:flex;align-items:center;justify-content:center;margin:0 auto 1.5rem auto;font-size:2rem;">🏢</div>
        <h1 style="font-size:1.75rem;font-weight:700;color:#1e3a5f;margin-bottom:0.5rem;">ERP Nexus</h1>
        <p style="color:#64748b;font-size:0.95rem;margin-bottom:2rem;">Sistema integral de gestión empresarial</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        login_form()

    st.markdown("""
    <div style="max-width:420px;margin:2rem auto 0 auto;text-align:center;">
        <p style="color:#94a3b8;font-size:0.8rem;">Demo: <b>admin</b> / <b>admin</b> · <b>ventas</b> / <b>ventas</b> · <b>almacen</b> / <b>almacen</b></p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

require_login()

# Sidebar profesional
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:1rem 0 1.5rem 0;border-bottom:1px solid rgba(255,255,255,0.1);margin-bottom:1rem;">
        <div style="width:48px;height:48px;background:rgba(255,255,255,0.1);border-radius:12px;display:flex;align-items:center;justify-content:center;margin:0 auto 0.75rem auto;font-size:1.5rem;">🏢</div>
        <div style="color:white;font-weight:700;font-size:1.1rem;">ERP Nexus</div>
        <div style="color:rgba(255,255,255,0.5);font-size:0.75rem;">v1.0 · Demo</div>
    </div>
    """, unsafe_allow_html=True)

    show_user_info()

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

    st.markdown("<div style='margin-top:2rem;border-top:1px solid rgba(255,255,255,0.1);padding-top:1rem;'></div>", unsafe_allow_html=True)
    logout()

# Main content
if page == "🏠 Dashboard":
    section_header("Dashboard Principal", "Visión general de tu empresa en tiempo real")
    kpi_cards()

    col1, col2 = st.columns(2)
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
