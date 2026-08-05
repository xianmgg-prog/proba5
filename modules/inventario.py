import streamlit as st
from database import SessionLocal
from models import Product, Stock, Warehouse, StockMovement, StockMovementType
from utils.helpers import format_currency, format_number, status_badge
from sqlalchemy import func
from sqlalchemy.orm import joinedload
import pandas as pd

def show():
    st.header("📦 Inventario y Stock en Tiempo Real")
    db = SessionLocal()

    tab1, tab2, tab3 = st.tabs(["Stock Actual", "Movimientos", "Alertas"])

    with tab1:
        wh_filter = st.selectbox("Almacén", ["Todos"] + [w.name for w in db.query(Warehouse).all()])
        search = st.text_input("Buscar producto...")

        query = db.query(Product).options(joinedload(Product.stocks).joinedload(Stock.warehouse))
        if search:
            query = query.filter(Product.name.contains(search) | Product.sku.contains(search))
        products = query.all()

        data = []
        for p in products:
            for s in p.stocks:
                if wh_filter == "Todos" or s.warehouse.name == wh_filter:
                    data.append({
                        "SKU": p.sku,
                        "Producto": p.name,
                        "Almacén": s.warehouse.name,
                        "Cantidad": s.quantity,
                        "Mínimo": p.min_stock,
                        "Máximo": p.max_stock,
                        "Estado": "🔴 BAJO" if s.quantity <= p.min_stock else "🟢 OK",
                        "PVP": format_currency(p.price_sale),
                        "Coste": format_currency(p.price_cost),
                    })

        if data:
            st.dataframe(pd.DataFrame(data), use_container_width=True)
        else:
            st.info("No hay productos")

    with tab2:
        st.subheader("Nuevo Movimiento")
        with st.form("movement"):
            col1, col2, col3 = st.columns(3)
            prod = col1.selectbox("Producto", [f"{p.id} - {p.name}" for p in db.query(Product).all()])
            wh = col2.selectbox("Almacén", [f"{w.id} - {w.name}" for w in db.query(Warehouse).all()])
            mtype = col3.selectbox("Tipo", [t.value for t in StockMovementType])
            qty = st.number_input("Cantidad", min_value=1, value=1)
            notes = st.text_area("Notas")
            if st.form_submit_button("Registrar Movimiento"):
                pid = int(prod.split(" - ")[0])
                wid = int(wh.split(" - ")[0])
                stock = db.query(Stock).filter_by(product_id=pid, warehouse_id=wid).first()
                if not stock:
                    stock = Stock(product_id=pid, warehouse_id=wid, quantity=0)
                    db.add(stock)

                if mtype in ["salida", "merma", "traspaso"] and stock.quantity < qty:
                    st.error("Stock insuficiente")
                else:
                    if mtype == "entrada":
                        stock.quantity += qty
                    elif mtype in ["salida", "merma"]:
                        stock.quantity -= qty

                    db.add(StockMovement(product_id=pid, warehouse_id=wid, type=mtype, quantity=qty, notes=notes, created_by=st.session_state.user["username"]))
                    db.commit()
                    st.success("Movimiento registrado")
                    st.rerun()

        st.subheader("Historial")
        moves = db.query(StockMovement).options(joinedload(StockMovement.product), joinedload(StockMovement.warehouse)).order_by(StockMovement.created_at.desc()).limit(50).all()
        if moves:
            df = pd.DataFrame([{
                "Fecha": m.created_at,
                "Producto": m.product.name,
                "Tipo": m.type.value,
                "Cantidad": m.quantity,
                "Almacén": m.warehouse.name if m.warehouse else "N/A",
                "Notas": m.notes,
                "Usuario": m.created_by
            } for m in moves])
            st.dataframe(df, use_container_width=True)

    with tab3:
        st.subheader("⚠️ Productos con Stock Bajo")
        products_all = db.query(Product).options(joinedload(Product.stocks)).all()
        low = []
        for p in products_all:
            total = sum(s.quantity for s in p.stocks)
            if total <= p.min_stock:
                low.append({"Producto": p.name, "SKU": p.sku, "Stock Actual": total, "Mínimo": p.min_stock, "Sugerencia": f"Reponer {p.max_stock - total} uds"})
        if low:
            st.dataframe(pd.DataFrame(low), use_container_width=True)
            if st.button("Generar Orden de Compra para Stock Bajo"):
                st.info("Redirigiendo a Compras...")
                st.session_state.page = "compras"
                st.rerun()
        else:
            st.success("No hay alertas de stock")

    db.close()
