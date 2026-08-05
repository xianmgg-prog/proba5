import streamlit as st
from database import SessionLocal
from models import Supplier, PurchaseOrder, PurchaseOrderStatus, PurchaseOrderItem, Product
from utils.helpers import format_currency, status_badge
from datetime import date

def show():
    st.header("📋 Compras y Proveedores")
    db = SessionLocal()

    tab1, tab2, tab3 = st.tabs(["Proveedores", "Órdenes de Compra", "Nueva OC"])

    with tab1:
        suppliers = db.query(Supplier).all()
        data = [{"Nombre": s.name, "Contacto": s.contact, "Email": s.email, "Teléfono": s.phone, 
                 "Rating": "⭐" * int(s.rating), "Aprobado": "✅" if s.is_approved else "❌", "Plazo": s.payment_terms} for s in suppliers]
        import pandas as pd
        st.dataframe(pd.DataFrame(data), use_container_width=True)

    with tab2:
        orders = db.query(PurchaseOrder).all()
        data = []
        for o in orders:
            data.append({
                "ID": o.id,
                "Proveedor": o.supplier.name,
                "Total": format_currency(o.total),
                "Estado": status_badge(o.status.value),
                "Aprobado por": o.approved_by or "-",
                "Fecha": o.created_at
            })
        st.dataframe(pd.DataFrame(data), use_container_width=True)

    with tab3:
        with st.form("new_po"):
            supplier = st.selectbox("Proveedor", [f"{s.id} - {s.name}" for s in db.query(Supplier).all()])
            notes = st.text_area("Notas")

            lines = []
            products = db.query(Product).all()
            for idx in range(3):
                cols = st.columns([3,1,1])
                prod_sel = cols[0].selectbox(f"Producto {idx+1}", [""] + [f"{p.id} - {p.name}" for p in products], key=f"po_prod_{idx}")
                qty = cols[1].number_input(f"Cant {idx+1}", min_value=0, value=0, key=f"po_qty_{idx}")
                price = cols[2].number_input(f"Precio {idx+1}", min_value=0.0, value=0.0, key=f"po_price_{idx}")
                if prod_sel and qty > 0:
                    pid = int(prod_sel.split(" - ")[0])
                    lines.append({"product_id": pid, "quantity": qty, "unit_price": price, "total": qty * price})

            if st.form_submit_button("Crear Orden"):
                sid = int(supplier.split(" - ")[0])
                total = sum(l["total"] for l in lines)
                po = PurchaseOrder(supplier_id=sid, status=PurchaseOrderStatus.draft, total=total, notes=notes)
                db.add(po)
                db.commit()
                for line in lines:
                    db.add(PurchaseOrderItem(order_id=po.id, **line))
                db.commit()
                st.success(f"Orden de compra #{po.id} creada")
                st.rerun()

    db.close()
