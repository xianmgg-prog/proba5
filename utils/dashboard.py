import streamlit as st
import plotly.express as px
from sqlalchemy import func
from sqlalchemy.orm import joinedload
from database import SessionLocal
from models import Product, Stock, Invoice, InvoiceStatus, BankTransaction, Campaign
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
        kpi_card("Stock Total", f"{int(total_stock):,} uds")
    with col2:
        kpi_card("Ventas Pagadas", format_currency(total_sales))
    with col3:
        kpi_card("Pendientes", format_currency(pending))
    with col4:
        kpi_card("Balance Banco", format_currency(balance))

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

    fig = px.bar(df, x="Fecha", y="Importe", title="Ventas por fecha",
                 color_discrete_sequence=["#111827"], template="plotly_white")
    fig.update_layout(height=300, margin=dict(l=20, r=20, t=40, b=20),
                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font=dict(family="Inter, sans-serif", size=12))
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
                     title="Alertas de stock bajo", template="plotly_white",
                     color_discrete_sequence=["#ef4444", "#d1d5db"])
        fig.update_layout(height=300, margin=dict(l=20, r=20, t=40, b=20),
                          paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font=dict(family="Inter, sans-serif", size=12))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.success("No hay alertas de stock")

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
        fig = px.pie(df, names="Campaña", values="Gastado", title="Gasto por plataforma",
                     template="plotly_white", hole=0.55)
        fig.update_layout(height=300, margin=dict(l=20, r=20, t=40, b=20),
                          paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font=dict(family="Inter, sans-serif", size=12))
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = px.bar(df, x="Campaña", y="ROAS", title="ROAS por campaña",
                     color="ROAS", color_continuous_scale="Greys", template="plotly_white")
        fig.update_layout(height=300, margin=dict(l=20, r=20, t=40, b=20),
                          paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font=dict(family="Inter, sans-serif", size=12))
        st.plotly_chart(fig, use_container_width=True)

def cashflow_forecast():
    st.markdown("<h2 style='font-size:1.125rem;font-weight:600;color:#374151;margin:1.5rem 0 0.75rem 0;'>Previsión de tesorería (30 días)</h2>", unsafe_allow_html=True)
    import pandas as pd
    from datetime import datetime, timedelta

    dates = [datetime.now().date() + timedelta(days=i) for i in range(30)]
    base = 21750
    values = [base + (i * 150) - (500 if i % 7 == 0 else 0) for i in range(30)]

    df = pd.DataFrame({"Fecha": dates, "Saldo Previsto": values})
    fig = px.line(df, x="Fecha", y="Saldo Previsto", title="", template="plotly_white")
    fig.add_hline(y=20000, line_dash="dash", line_color="#ef4444", annotation_text="Mínimo")
    fig.update_traces(line_color="#111827", line_width=2)
    fig.update_layout(height=260, margin=dict(l=20, r=20, t=20, b=20),
                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font=dict(family="Inter, sans-serif", size=12))
    st.plotly_chart(fig, use_container_width=True)
