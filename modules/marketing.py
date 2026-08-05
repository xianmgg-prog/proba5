import streamlit as st
from database import SessionLocal
from models import Campaign, ApiCredential
from utils.helpers import format_currency
from utils.theme import section_header
import pandas as pd
import plotly.express as px

@st.cache_data(ttl=30)
def get_campaigns():
    db = SessionLocal()
    result = db.query(Campaign).all()
    db.close()
    return result

def show():
    section_header("Marketing y publicidad", "Campañas y rendimiento")
    db = SessionLocal()
    google = db.query(ApiCredential).filter_by(service="google_ads").first()
    meta = db.query(ApiCredential).filter_by(service="meta_ads").first()
    linkedin = db.query(ApiCredential).filter_by(service="linkedin_ads").first()
    openai = db.query(ApiCredential).filter_by(service="openai").first()
    db.close()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Google Ads", "●" if (google and google.is_active) else "○")
    col2.metric("Meta Ads", "●" if (meta and meta.is_active) else "○")
    col3.metric("LinkedIn", "●" if (linkedin and linkedin.is_active) else "○")
    col4.metric("OpenAI", "●" if (openai and openai.is_active) else "○")

    campaigns = get_campaigns()

    col1, col2, col3 = st.columns(3)
    total_budget = sum(c.budget for c in campaigns)
    total_spent = sum(c.spent for c in campaigns)
    avg_roas = sum(c.roas for c in campaigns) / len(campaigns) if campaigns else 0

    col1.metric("Presupuesto", format_currency(total_budget))
    col2.metric("Gastado", format_currency(total_spent))
    col3.metric("ROAS medio", f"{avg_roas:.2f}x")

    st.markdown("**Campañas activas**")
    data = []
    for c in campaigns:
        progress = float(c.spent) / float(c.budget) * 100 if c.budget else 0
        data.append({
            "Campaña": c.name,
            "Plataforma": c.platform,
            "Presupuesto": format_currency(c.budget),
            "Gastado": format_currency(c.spent),
            "Progreso": f"{progress:.0f}%",
            "ROAS": f"{c.roas}x",
            "Estado": c.status,
        })
    st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)

    col1, col2 = st.columns(2)
    with col1:
        fig = px.pie(pd.DataFrame(data), names="Plataforma", values="Gastado", title="Gasto por plataforma",
                     template="plotly_white", hole=0.55)
        fig.update_layout(height=280, margin=dict(l=20, r=20, t=40, b=20),
                          paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font=dict(family="Inter, sans-serif", size=12))
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        df_roas = pd.DataFrame([{"Campaña": c.name, "ROAS": float(c.roas)} for c in campaigns])
        fig = px.bar(df_roas, x="Campaña", y="ROAS", title="ROAS por campaña",
                     color="ROAS", color_continuous_scale="Greys", template="plotly_white")
        fig.update_layout(height=280, margin=dict(l=20, r=20, t=40, b=20),
                          paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font=dict(family="Inter, sans-serif", size=12))
        st.plotly_chart(fig, use_container_width=True)

    with st.expander("Generar copy"):
        if not (openai and openai.is_active):
            st.info("Configura la API de OpenAI en Integraciones para usar esta función.")
        product = st.text_input("Producto")
        audience = st.text_input("Audiencia")
        if st.button("Generar"):
            st.success(f"Headline: ¡{product} con 20% de descuento!")
            st.write(f"Body: Descubre por qué {audience} eligen {product}.")
