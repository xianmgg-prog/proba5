import streamlit as st
from database import SessionLocal
from models import CostAlert
from utils.helpers import format_currency
import pandas as pd

@st.cache_data(ttl=30)
def get_alerts():
    db = SessionLocal()
    result = db.query(CostAlert).order_by(CostAlert.created_at.desc()).all()
    db.close()
    return result

def show():
    st.header("🤖 Agentes Inteligentes de Optimización")

    st.info("🧠 Human-in-the-Loop — El agente detecta y propone. Tú decides.")

    alerts = get_alerts()

    tab1, tab2 = st.tabs(["Alertas Activas", "Configuración"])

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
                        st.markdown(f"💰 Actual: `{format_currency(alert.current_price)}` → Alternativa: `{format_currency(alert.alternative_price)}` ({alert.alternative_provider})")
                        st.markdown(f"💚 Ahorro potencial: **{format_currency(alert.savings_potential)}**")
                    with col2:
                        st.markdown(f"Estado: `{alert.status}`")
                        if alert.approved_by:
                            st.caption(f"Aprobado por: {alert.approved_by}")
                    with col3:
                        if alert.status == "pendiente":
                            if st.button("✅ Aprobar", key=f"app_{alert.id}"):
                                db = SessionLocal()
                                a = db.query(CostAlert).get(alert.id)
                                a.status = "aprobada"
                                a.approved_by = st.session_state.user["username"]
                                db.commit()
                                db.close()
                                st.success("Aprobado")
                                st.cache_data.clear()
                                st.rerun()
                            if st.button("❌ Rechazar", key=f"rej_{alert.id}"):
                                db = SessionLocal()
                                a = db.query(CostAlert).get(alert.id)
                                a.status = "rechazada"
                                db.commit()
                                db.close()
                                st.rerun()
                        elif alert.status == "aprobada":
                            if st.button("⚡ Ejecutar", key=f"exe_{alert.id}"):
                                db = SessionLocal()
                                a = db.query(CostAlert).get(alert.id)
                                a.status = "ejecutada"
                                db.commit()
                                db.close()
                                st.success("Cambio ejecutado (simulado)")
                                st.cache_data.clear()
                                st.rerun()

    with tab2:
        st.subheader("Configurar Vigilancia de Gastos")
        with st.form("agent_config"):
            st.multiselect("Categorías a monitorizar", ["Seguro", "Energía", "Software", "Telefonía", "Alquiler", "Suministros"], default=["Seguro", "Energía", "Software"])
            st.number_input("Umbral mínimo de ahorro (€)", min_value=10, value=50)
            st.selectbox("Modo de ejecución", ["Human-in-the-loop (recomendado)", "Autónomo (solo bajo riesgo)"])
            st.text_input("Excepciones (proveedores a ignorar)")
            if st.form_submit_button("Guardar Configuración"):
                st.success("Configuración guardada (simulado)")
                st.caption("En producción: el agente compararía vía APIs de comparadores o scraping autorizado")
