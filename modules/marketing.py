import streamlit as st
from database import SessionLocal
from models import Campaign
from utils.helpers import format_currency
import pandas as pd
import plotly.express as px

def show():
    st.header("📢 Marketing y Publicidad")
    db = SessionLocal()

    st.info("🧪 Modo Mock — Datos simulados. Para producción configura APIs reales.")

    campaigns = db.query(Campaign).all()

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

    with st.expander("🤖 Generar Copy Asistido (Mock)"):
        product = st.text_input("Producto a promocionar")
        audience = st.text_input("Audiencia objetivo")
        if st.button("Generar copy"):
            st.success(f"Headline: ¡{product} ahora con 20% de descuento!  Body: Descubre por qué {audience} eligen {product}. Envío gratis 24h.  CTA: Comprar ahora →")
            st.caption("(En producción: conectar con OpenAI/Claude API)")

    db.close()
