import streamlit as st
from database import SessionLocal
from models import Customer
from utils.helpers import format_currency
from sqlalchemy.orm import joinedload
import pandas as pd

@st.cache_data(ttl=30)
def get_customers():
    db = SessionLocal()
    result = db.query(Customer).options(joinedload(Customer.invoices)).all()
    db.close()
    return result

def show():
    st.header("🤝 CRM - Clientes y Leads")

    tab1, tab2 = st.tabs(["Clientes", "Pipeline"])

    with tab1:
        type_filter = st.selectbox("Tipo", ["Todos", "cliente", "lead"])
        customers = get_customers()
        if type_filter != "Todos":
            customers = [c for c in customers if c.type == type_filter]

        data = [{"Nombre": c.name, "Email": c.email, "Teléfono": c.phone, "NIF": c.tax_id, 
                 "Segmento": c.segment, "Tipo": c.type, "Alta": c.created_at} for c in customers]
        st.dataframe(pd.DataFrame(data), use_container_width=True)

        with st.expander("➕ Añadir Cliente/Lead"):
            with st.form("new_customer"):
                name = st.text_input("Nombre")
                email = st.text_input("Email")
                phone = st.text_input("Teléfono")
                tax_id = st.text_input("NIF/CIF")
                ctype = st.selectbox("Tipo", ["cliente", "lead"])
                segment = st.selectbox("Segmento", ["PYME", "Startup", "Retail", "Servicios", "General"])
                if st.form_submit_button("Guardar"):
                    db = SessionLocal()
                    db.add(Customer(name=name, email=email, phone=phone, tax_id=tax_id, type=ctype, segment=segment))
                    db.commit()
                    db.close()
                    st.success("Cliente añadido")
                    st.cache_data.clear()
                    st.rerun()

    with tab2:
        st.subheader("Pipeline de Ventas (Simplificado)")
        stages = ["Contacto", "Propuesta", "Negociación", "Cierre"]
        for stage in stages:
            with st.container(border=True):
                st.markdown(f"**{stage}**")
                if stage == "Contacto":
                    st.caption("• Startup Beta (nuevo lead web)")
                    st.caption("• Empresa Delta (referido)")
                elif stage == "Propuesta":
                    st.caption("• Consultoría Gamma (presupuesto enviado)")
                elif stage == "Negociación":
                    st.caption("• Empresa Alpha (ampliación licencias)")
                else:
                    st.caption("• Ninguno en cierre esta semana")
