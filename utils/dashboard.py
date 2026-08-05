import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import func
from sqlalchemy.orm import joinedload
from database import SessionLocal
from models import Product, Stock, Invoice, InvoiceStatus, PurchaseOrder, BankTransaction, Campaign, CostAlert
from utils.theme import kpi_card
from utils.helpers import format_currency

@st.cache_data(ttl=60)
def get_kpi_data():
    db = SessionLocal()
    total_stock = db.query(func.sum(Stock.quantity)).scalar() or 0
    total_sales = db.query(func.sum(Invoice.total)).filter(Invoice.status == InvoiceStatus.paid).scalar() or 0
    pending = db.query(func.sum(Invoice.total)).filter(Invoice.status == InvoiceStatus.sent).scalar() or 0
    last_tx = db.query(BankTransaction).order_by(BankTransaction.date.desc()).first()
    balance = last_tx.balance if last_tx else 0
    db.close()
    return total_stock, total_sales, pending, balance

def kpi_cards():
    total_stock, total_sales, pending, balance = get_kpi_data()
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        kpi_card("Stock Total", f"{int(total_stock):,} uds", "📦", color="#3b82f6")
    with col2:
        kpi_card("Ventas Pagadas", format_currency(total_sales), "💰", color="#10b981")
    with col3:
        kpi_card("Facturas Pendientes", format_currency(pending), "⏳", color="#f59e0b")
    with col4:
        kpi_card("Balance Banco", format_currency(balance), "🏦", color="#8b5cf6")

@st.cache_data(ttl=60)
def get_sales_data():
    db = SessionLocal()
    invoices = db.query(Invoice).filter(Invoice.status == InvoiceStatus.paid).all()
    db.close()
    return [{"Fecha": i.issue_date, "Importe": float(i.total)} for i in invoices]

def sales_chart():
    data = get_sales_data()
    if not data:
        st.info("Sin datos de ventas")
        return
    import pandas as pd
    df = pd.DataFrame(data)
    df = df.groupby("Fecha").sum().reset_index()

    fig = px.bar(df, x="Fecha", y="Importe", title="📈 Ventas por Fecha", 
                 color_discrete_sequence=["#1e3a5f"], template="plotly_white")
    fig.update_layout(height=320, margin=dict(l=20, r=20, t=40, b=20),
                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

@st.cache_data(ttl=60)
def get_stock_alert_data():
    db = SessionLocal()
    products = db.query(Product).options(joinedload(Product.stocks)).all()
    db.close()
    data = []
    for p in products:
        total = sum(s.quantity for s in p.stocks)
        if total <= p.min_stock:
            data.append({"Producto": p.name, "Stock": total, "Mínimo": int(p.min_stock)})
    return data

def stock_alert_chart():
    data = get_stock_alert_data()
    if data:
        import pandas as pd
        df = pd.DataFrame(data)
        fig = px.bar(df, x="Producto", y=["Stock", "Mínimo"], barmode="group", 
                     title="⚠️ Alertas de Stock Bajo", template="plotly_white",
                     color_discrete_sequence=["#ef4444", "#cbd5e1"])
        fig.update_layout(height=320, margin=dict(l=20, r=20, t=40, b=20),
                          paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.success("✅ No hay alertas de stock")

@st.cache_data(ttl=60)
def get_campaign_data():
    db = SessionLocal()
    camps = db.query(Campaign).all()
    db.close()
    return [{"Campaña": c.name, "Presupuesto": float(c.budget), "Gastado": float(c.spent), "ROAS": float(c.roas)} for c in camps]

def campaign_chart():
    data = get_campaign_data()
    import pandas as pd
    df = pd.DataFrame(data)

    col1, col2 = st.columns(2)
    with col1:
        fig = px.pie(df, names="Campaña", values="Gastado", title="💸 Distribución Gasto Publicidad",
                     template="plotly_white", hole=0.4)
        fig.update_layout(height=320, margin=dict(l=20, r=20, t=40, b=20),
                          paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = px.bar(df, x="Campaña", y="ROAS", title="🎯 ROAS por Campaña", 
                     color="ROAS", color_continuous_scale="RdYlGn", template="plotly_white")
        fig.update_layout(height=320, margin=dict(l=20, r=20, t=40, b=20),
                          paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)

def cashflow_forecast():
    st.markdown("<h3 style='color:#1e3a5f;font-size:1.1rem;font-weight:700;margin:1.5rem 0 1rem 0;'>📊 Previsión de Tesorería (30 días)</h3>", unsafe_allow_html=True)
    import pandas as pd
    from datetime import datetime, timedelta

    dates = [datetime.now().date() + timedelta(days=i) for i in range(30)]
    base = 21750
    values = [base + (i * 150) - (500 if i % 7 == 0 else 0) for i in range(30)]

    df = pd.DataFrame({"Fecha": dates, "Saldo Previsto": values})
    fig = px.line(df, x="Fecha", y="Saldo Previsto", title="", template="plotly_white")
    fig.add_hline(y=20000, line_dash="dash", line_color="#ef4444", annotation_text="Límite mínimo")
    fig.update_traces(line_color="#1e3a5f", line_width=3)
    fig.update_layout(height=280, margin=dict(l=20, r=20, t=20, b=20),
                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)
