import streamlit as st
from database import SessionLocal
from models import Employee
from utils.helpers import format_currency
from utils.theme import section_header
import pandas as pd

@st.cache_data(ttl=30)
def get_employees():
    db = SessionLocal()
    result = db.query(Employee).all()
    db.close()
    return result

def show():
    section_header("Recursos humanos", "Empleados y nóminas")

    tab1, tab2 = st.tabs(["Empleados", "Nóminas"])

    with tab1:
        emps = get_employees()
        data = [{"Nombre": f"{e.first_name} {e.last_name}", "Email": e.email, "Departamento": e.department, 
                 "Puesto": e.position, "Salario": format_currency(e.salary), "Alta": e.hire_date.strftime("%d/%m/%Y"), 
                 "Contrato": e.contract_type, "Activo": "Sí" if e.is_active else "No"} for e in emps]
        st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)

        with st.expander("Añadir empleado"):
            with st.form("new_emp"):
                cols = st.columns(2)
                first = cols[0].text_input("Nombre")
                last = cols[1].text_input("Apellidos")
                email = st.text_input("Email")
                dept = st.selectbox("Departamento", ["Ventas", "Almacén", "Administración", "Marketing", "IT"])
                pos = st.text_input("Puesto")
                salary = st.number_input("Salario bruto mensual", min_value=0.0, value=2000.0)
                hire = st.date_input("Fecha alta", value=pd.to_datetime("2026-01-01"))
                if st.form_submit_button("Guardar"):
                    db = SessionLocal()
                    db.add(Employee(first_name=first, last_name=last, email=email, department=dept, position=pos, salary=salary, hire_date=hire))
                    db.commit()
                    db.close()
                    st.cache_data.clear()
                    st.rerun()

    with tab2:
        emps = get_employees()
        total_salaries = sum(e.salary for e in emps if e.is_active)
        col1, col2 = st.columns(2)
        col1.metric("Masa salarial mensual", format_currency(total_salaries))
        col2.metric("Coste empresarial", format_currency(float(total_salaries) * 1.35))
        st.caption("En producción: integrar con gestoría o API de nóminas")
