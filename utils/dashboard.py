import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import func
from sqlalchemy.orm import joinedload
from database import SessionLocal
from models import Product, Stock, Invoice, InvoiceStatus, PurchaseOrder, BankTransaction, Campaign, CostAlert
from utils.helpers import format_currency

def kpi_cards():
    db = SessionLocal()

    col1, col2, col3, col4 = st.columns(4)

    total_stock = db.query(func.sum(Stock.quantity)).scalar() or 0
    with col1:
        st.metric("📦 Stock Total", f"{int(total_stock):,} uds")

    total_sales = db.query(func.sum(Invoice.total)).filter(Invoice.status == InvoiceStatus.paid).scalar() or 0
    with col2:
        st.metric("💰 Ventas Pagadas", format_currency(total_sales))

    pending = db.query(func.sum(Invoice.total)).filter(Invoice.status == InvoiceStatus.sent).scalar() or 0
    with col3:
        st.metric("⏳ Facturas Pendientes", format_currency(pending))

    last_tx = db.query(BankTransaction).order_by(BankTransaction.date.desc()).first()
    balance = last_tx.balance if last_tx else 0
    with col4:
        st.metric("🏦 Balance Banco", format_currency(balance))

    db.close()

def sales_chart():
    db = SessionLocal()
    invoices = db.query(Invoice).filter(Invoice.status == InvoiceStatus.paid).all()
    db.close()

    if not invoices:
        st.info("Sin datos de ventas")
        return

    import pandas as pd
    df = pd.DataFrame([{"Fecha": i.issue_date, "Importe": float(i.total)} for i in invoices])
    df = df.groupby("Fecha").sum().reset_index()

    fig = px.bar(df, x="Fecha", y="Importe", title="Ventas por Fecha", color_discrete_sequence=["#1f77b4"])
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)

def stock_alert_chart():
    db = SessionLocal()
    # Usar joinedload para cargar stocks junto con productos
    products = db.query(Product).options(joinedload(Product.stocks).joinedload(Stock.warehouse)).all()

    data = []
    for p in products:
        total = sum(s.quantity for s in p.stocks)
        if total <= p.min_stock:
            data.append({"Producto": p.name, "Stock": total, "Mínimo": int(p.min_stock)})

    db.close()

    if data:
        import pandas as pd
        df = pd.DataFrame(data)
        fig = px.bar(df, x="Producto", y=["Stock", "Mínimo"], barmode="group", title="⚠️ Alertas de Stock Bajo")
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.success("✅ No hay alertas de stock")

def campaign_chart():
    db = SessionLocal()
    camps = db.query(Campaign).all()
    db.close()

    import pandas as pd
    df = pd.DataFrame([{"Campaña": c.name, "Presupuesto": float(c.budget), "Gastado": float(c.spent), "ROAS": float(c.roas)} for c in camps])

    col1, col2 = st.columns(2)
    with col1:
        fig = px.pie(df, names="Campaña", values="Gastado", title="Distribución Gasto Publicidad")
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = px.bar(df, x="Campaña", y="ROAS", title="ROAS por Campaña", color="ROAS", color_continuous_scale="RdYlGn")
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)

def cashflow_forecast():
    st.subheader("📈 Previsión de Tesorería (30 días)")
    import pandas as pd
    from datetime import datetime, timedelta

    dates = [datetime.now().date() + timedelta(days=i) for i in range(30)]
    base = 21750
    values = [base + (i * 150) - (500 if i % 7 == 0 else 0) for i in range(30)]

    df = pd.DataFrame({"Fecha": dates, "Saldo Previsto": values})
    fig = px.line(df, x="Fecha", y="Saldo Previsto", title="Flujo de Caja Proyectado")
    fig.add_hline(y=20000, line_dash="dash", line_color="red", annotation_text="Límite mínimo")
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)
