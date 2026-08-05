import streamlit as st
from database import SessionLocal
from models import Campaign, ApiCredential
from utils.helpers import format_currency
import pandas as pd
import plotly.express as px

@st.cache_data(ttl=30)
def get_campaigns():
    db = SessionLocal()
    result = db.query(Campaign).all()
    db.close()
    return result

def show():
    st.header("📢 Marketing y Publicidad")
    db = SessionLocal()

    # Leer credenciales
    google = db.query(ApiCredential).filter_by(service="google_ads").first()
    meta = db.query(ApiCredential).filter_by(service="meta_ads").first()
    linkedin = db.query(ApiCredential).filter_by(service="linkedin_ads").first()
    openai = db.query(ApiCredential).filter_by(service="openai").first()
    db.close()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Google Ads", "🟢" if (google and google.is_active) else "🔴")
    col2.metric("Meta Ads", "🟢" if (meta and meta.is_active) else "🔴")
    col3.metric("LinkedIn", "🟢" if (linkedin and linkedin.is_active) else "🔴")
    col4.metric("OpenAI", "🟢" if (openai and openai.is_active) else "🔴")

    if not google and not meta and not linkedin:
        st.warning("🔧 No tienes APIs de publicidad configuradas. Ve a **🔌 Integraciones** para añadirlas.")

    campaigns = get_campaigns()

    col1, col2, col3 = st.columns(3)
    total_budget = sum(c.budget for c in campaigns)
    total_spent = sum(c.spent for c in campaigns)
    avg_roas = sum(c.roas for c in campaigns) / len(campaigns) if campaigns else 0

    col1.metric("Presupuesto Total", format_currency(total_budget))
    col2.metric("Gastado", format_currency(total_spent))
    col3.metric("ROAS Medio", f"{avg_roas:.2f}x")

    st.subheader("Campañas Activas")
    data = []
    for c in campaigns:
        progress = float(c.spent) / float(c.budget) * 100 if c.budget else 0
        data.append({
            "Campaña": c.name,
            "Plataforma": c.platform,
            "Presupuesto": format_currency(c.budget),
            "Gastado": format_currency(c.spent),
            "%": f"{progress:.1f}%",
            "ROAS": f"{c.roas}x",
            "Estado": c.status,
            "Inicio": c.start_date,
            "Fin": c.end_date
        })
    st.dataframe(pd.DataFrame(data), use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        fig = px.pie(pd.DataFrame(data), names="Plataforma", values="Gastado", title="Gasto por Plataforma")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        df_roas = pd.DataFrame([{"Campaña": c.name, "ROAS": float(c.roas), "Gastado": float(c.spent)} for c in campaigns])
        fig = px.scatter(df_roas, x="Gastado", y="ROAS", size="ROAS", color="Campaña", title="Eficiencia ROAS vs Gasto")
        st.plotly_chart(fig, use_container_width=True)

    with st.expander("🤖 Generar Copy Asistido"):
        if not (openai and openai.is_active):
            st.warning("⚠️ Configura la API de OpenAI en **🔌 Integraciones** para usar esta función.")

        product = st.text_input("Producto a promocionar")
        audience = st.text_input("Audiencia objetivo")
        tone = st.selectbox("Tono", ["Profesional", "Divertido", "Urgente", "Emocional"])

        if st.button("Generar copy"):
            if openai and openai.is_active:
                st.success(f"**Headline:** ¡{product} ahora con 20% de descuento!")
                st.write(f"**Body:** Descubre por qué {audience} eligen {product}. Envío gratis 24h.")
                st.write(f"**CTA:** Comprar ahora →")
                st.caption(f"(Tono: {tone} | En producción: se llamaría a OpenAI API con tu key)")
            else:
                st.error("Necesitas configurar la API de OpenAI primero.")
