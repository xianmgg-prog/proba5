import streamlit as st
st.set_page_config(page_title="ERP Nexus", page_icon="🏢", layout="wide", initial_sidebar_state="expanded")

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

# Login screen sobrio
if "user" not in st.session_state:
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("<div style='height:15vh'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div style="text-align:center;margin-bottom:2rem;">
            <div style="width:48px;height:48px;background:#111827;border-radius:10px;display:inline-flex;align-items:center;justify-content:center;color:white;font-size:1.5rem;font-weight:700;margin-bottom:1rem;">N</div>
            <h1 style="font-size:1.5rem;font-weight:700;color:#111827;margin:0;letter-spacing:-0.025em;">ERP Nexus</h1>
            <p style="color:#6b7280;font-size:0.875rem;margin:0.25rem 0 0 0;">Sistema de gestión empresarial</p>
        </div>
        """, unsafe_allow_html=True)
        login_form()
        st.markdown("""
        <div style="text-align:center;margin-top:1.5rem;">
            <p style="color:#9ca3af;font-size:0.75rem;">Demo: admin/admin · ventas/ventas · almacen/almacen</p>
        </div>
        """, unsafe_allow_html=True)
    st.stop()

require_login()

# Sidebar sobrio
with st.sidebar:
    st.markdown("""
    <div style="padding:0.5rem 0 1.25rem 0;border-bottom:1px solid #1f2937;margin-bottom:0.75rem;">
        <div style="display:flex;align-items:center;gap:0.625rem;">
            <div style="width:32px;height:32px;background:#1f2937;border-radius:8px;display:flex;align-items:center;justify-content:center;color:#f3f4f6;font-size:0.875rem;font-weight:700;">N</div>
            <div>
                <div style="color:#f3f4f6;font-weight:600;font-size:0.9375rem;letter-spacing:-0.01em;">ERP Nexus</div>
                <div style="color:#6b7280;font-size:0.6875rem;">v1.0</div>
            </div>
        </div>
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

    st.markdown("<div style='margin-top:auto;padding-top:1rem;border-top:1px solid #1f2937;'></div>", unsafe_allow_html=True)
    logout()

# Main content
if page == "🏠 Dashboard":
    section_header("Dashboard", "Visión general de tu empresa")
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
