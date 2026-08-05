import streamlit as st
st.set_page_config(page_title="ERP MVP", page_icon="🏢", layout="wide", initial_sidebar_state="expanded")

from database import init_db
from seed_data import seed
from utils.auth import login_form, logout, show_user_info, require_login
from utils.dashboard import kpi_cards, sales_chart, stock_alert_chart, campaign_chart, cashflow_forecast

@st.cache_resource
def setup_database():
    """Solo se ejecuta una vez por sesión de usuario"""
    init_db()
    seed()
    return True

setup_database()

# Navegación
if "user" not in st.session_state:
    st.title("🏢 ERP MVP — Versión de Prueba")
    st.markdown("Sistema integral de gestión empresarial. **Demo credentials:** `admin`/`admin`, `ventas`/`ventas`, `almacen`/`almacen`, `contable`/`contable`")
    login_form()
    st.stop()

require_login()
show_user_info()
logout()

st.sidebar.title("📂 Módulos")
page = st.sidebar.radio("", [
    "🏠 Dashboard",
    "📦 Inventario",
    "💶 Ventas",
    "📋 Compras",
    "💼 Finanzas",
    "🤝 CRM",
    "📢 Marketing",
    "🏦 Banca (Sandbox)",
    "🤖 Agentes",
    "👥 RRHH",
], key="nav")

if page == "🏠 Dashboard":
    st.title("🏠 Dashboard Principal")
    kpi_cards()
    col1, col2 = st.columns(2)
    with col1:
        sales_chart()
    with col2:
        stock_alert_chart()
    campaign_chart()
    cashflow_forecast()
    st.divider()
    st.caption("ERP MVP v0.1 | Datos de demostración | Render")

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

elif page == "🏦 Banca (Sandbox)":
    from modules import banca
    banca.show()

elif page == "🤖 Agentes":
    from modules import agentes
    agentes.show()

elif page == "👥 RRHH":
    from modules import rrhh
    rrhh.show()
