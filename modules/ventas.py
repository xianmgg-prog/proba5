import streamlit as st
from database import SessionLocal
from models import Customer, Invoice, InvoiceStatus, InvoiceItem, Product, Stock, StockMovement, StockMovementType
from utils.helpers import format_currency, status_badge
from sqlalchemy import func
from sqlalchemy.orm import joinedload
from datetime import date
import pandas as pd

@st.cache_data(ttl=30)
def get_customers():
    db = SessionLocal()
    result = db.query(Customer).all()
    db.close()
    return result

@st.cache_data(ttl=30)
def get_invoices():
    db = SessionLocal()
    result = db.query(Invoice).options(joinedload(Invoice.customer)).all()
    db.close()
    return result

@st.cache_data(ttl=30)
def get_products():
    db = SessionLocal()
    result = db.query(Product).all()
    db.close()
    return result

def show():
    st.header("💶 Ventas y Facturación")
    db = SessionLocal()

    tab1, tab2, tab3 = st.tabs(["Facturas", "Nueva Factura", "POS Rápido"])

    with tab1:
        status_filter = st.selectbox("Estado", ["Todos"] + [s.value for s in InvoiceStatus])
        invoices = get_invoices()
        if status_filter != "Todos":
            invoices = [i for i in invoices if i.status.value == status_filter]

        data = []
        for i in invoices:
            data.append({
                "Nº": f"{i.series}-{i.number:04d}",
                "Cliente": i.customer.name,
                "Fecha": i.issue_date,
                "Vencimiento": i.due_date,
                "Total": format_currency(i.total),
                "Estado": status_badge(i.status.value),
                "Pagada": i.paid_date or "No"
            })
        st.dataframe(pd.DataFrame(data), use_container_width=True)

    with tab2:
        st.subheader("Crear Factura")
        customers = get_customers()
        products = get_products()
        with st.form("invoice"):
            customer = st.selectbox("Cliente", [f"{c.id} - {c.name}" for c in customers])
            series = st.text_input("Serie", value="F2026")
            num = st.number_input("Número", min_value=1, value=4)
            due_days = st.number_input("Vencimiento (días)", min_value=1, value=30)

            st.write("Líneas de factura")
            lines = []
            for idx in range(3):
                cols = st.columns([3,1,1,1])
                prod_sel = cols[0].selectbox(f"Producto {idx+1}", [""] + [f"{p.id} - {p.name}" for p in products], key=f"prod_{idx}")
                qty = cols[1].number_input(f"Cant {idx+1}", min_value=0, value=0, key=f"qty_{idx}")
                if prod_sel and qty > 0:
                    pid = int(prod_sel.split(" - ")[0])
                    p = db.query(Product).get(pid)
                    lines.append({"product_id": pid, "description": p.name, "quantity": qty, "unit_price": p.price_sale, "tax_rate": p.tax_rate})

            if st.form_submit_button("Guardar Borrador"):
                cid = int(customer.split(" - ")[0])
                inv = Invoice(series=series, number=num, customer_id=cid, status=InvoiceStatus.draft, issue_date=date.today(), due_date=date.today())
                db.add(inv)
                db.commit()

                subtotal = 0
                for line in lines:
                    total = line["quantity"] * float(line["unit_price"])
                    tax = total * float(line["tax_rate"]) / 100
                    subtotal += total
                    db.add(InvoiceItem(invoice_id=inv.id, **line, total=total))

                inv.subtotal = subtotal
                inv.tax_total = subtotal * 0.21
                inv.total = subtotal * 1.21
                db.commit()
                st.success(f"Factura {series}-{num:04d} creada")
                st.cache_data.clear()
                st.rerun()

    with tab3:
        st.subheader("🛒 Punto de Venta Rápido")
        products = get_products()
        prod_quick = st.selectbox("Producto", [f"{p.id} - {p.name} ({format_currency(p.price_sale)})" for p in products])
        qty_quick = st.number_input("Cantidad", min_value=1, value=1)

        if st.button("Registrar Venta"):
            pid = int(prod_quick.split(" - ")[0])
            p = db.query(Product).get(pid)
            stock = db.query(Stock).filter_by(product_id=pid, warehouse_id=1).first()
            if stock and stock.quantity >= qty_quick:
                stock.quantity -= qty_quick
                db.add(StockMovement(product_id=pid, warehouse_id=1, type=StockMovementType.exit, quantity=qty_quick, notes="Venta POS", created_by=st.session_state.user["username"]))
                db.commit()
                st.success(f"Venta registrada: {p.name} x{qty_quick} = {format_currency(float(p.price_sale)*qty_quick)}")
                st.cache_data.clear()
            else:
                st.error("Stock insuficiente en almacén central")

    db.close()
