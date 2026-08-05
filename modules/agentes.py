import streamlit as st
from database import SessionLocal
from models import CostAlert
from utils.helpers import format_currency
from utils.theme import section_header, status_badge

@st.cache_data(ttl=30)
def get_alerts():
    db = SessionLocal()
    result = db.query(CostAlert).order_by(CostAlert.created_at.desc()).all()
    db.close()
    return result

def show():
    section_header("Agentes de optimización", "Detección automática de ahorro")

    alerts = get_alerts()

    tab1, tab2 = st.tabs(["Alertas", "Configuración"])

    with tab1:
        if not alerts:
            st.success("No hay alertas pendientes")
        else:
            for alert in alerts:
                with st.container(border=True):
                    col1, col2, col3 = st.columns([3,1,1])
                    with col1:
                        st.markdown(f"**{alert.category}** — {alert.provider}")
                        st.caption(alert.description)
                        st.markdown(f"Actual: `{format_currency(alert.current_price)}` → `{format_currency(alert.alternative_price)}` ({alert.alternative_provider})")
                        st.markdown(f"Ahorro: **{format_currency(alert.savings_potential)}**")
                    with col2:
                        st.markdown(status_badge(alert.status), unsafe_allow_html=True)
                        if alert.approved_by:
                            st.caption(f"Por: {alert.approved_by}")
                    with col3:
                        if alert.status == "pendiente":
                            if st.button("Aprobar", key=f"app_{alert.id}"):
                                db = SessionLocal()
                                a = db.query(CostAlert).get(alert.id)
                                a.status = "aprobada"
                                a.approved_by = st.session_state.user["username"]
                                db.commit()
                                db.close()
                                st.cache_data.clear()
                                st.rerun()
                            if st.button("Rechazar", key=f"rej_{alert.id}"):
                                db = SessionLocal()
                                a = db.query(CostAlert).get(alert.id)
                                a.status = "rechazada"
                                db.commit()
                                db.close()
                                st.cache_data.clear()
                                st.rerun()
                        elif alert.status == "aprobada":
                            if st.button("Ejecutar", key=f"exe_{alert.id}"):
                                db = SessionLocal()
                                a = db.query(CostAlert).get(alert.id)
                                a.status = "ejecutada"
                                db.commit()
                                db.close()
                                st.cache_data.clear()
                                st.rerun()

    with tab2:
        st.markdown("**Configurar vigilancia**")
        with st.form("agent_config"):
            st.multiselect("Categorías", ["Seguro", "Energía", "Software", "Telefonía", "Alquiler", "Suministros"], default=["Seguro", "Energía", "Software"])
            st.number_input("Umbral mínimo (€)", min_value=10, value=50)
            st.selectbox("Modo", ["Human-in-the-loop", "Autónomo"])
            if st.form_submit_button("Guardar"):
                st.success("Configuración guardada")
