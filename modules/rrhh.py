import streamlit as st
from database import SessionLocal
from models import Employee
from utils.helpers import format_currency
import pandas as pd

def show():
    st.header("👥 Recursos Humanos")
    db = SessionLocal()

    tab1, tab2 = st.tabs(["Empleados", "Nóminas Básicas"])

    with tab1:
        emps = db.query(Employee).all()
        data = [{"Nombre": f"{e.first_name} {e.last_name}", "Email": e.email, "Departamento": e.department, 
                 "Puesto": e.position, "Salario": format_currency(e.salary), "Alta": e.hire_date, "Contrato": e.contract_type, "Activo": "✅" if e.is_active else "❌"} for e in emps]
        st.dataframe(pd.DataFrame(data), use_container_width=True)

        with st.expander("➕ Añadir Empleado"):
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
                    db.add(Employee(first_name=first, last_name=last, email=email, department=dept, position=pos, salary=salary, hire_date=hire))
                    db.commit()
                    st.success("Empleado añadido")
                    st.rerun()

    with tab2:
        st.subheader("Resumen Nóminas (Simulado)")
        total_salaries = sum(e.salary for e in emps if e.is_active)
        st.metric("Massa Salarial Mensual", format_currency(total_salaries))
        st.metric("Coste Empresarial Est.", format_currency(float(total_salaries) * 1.35))

        st.caption("En producción: integrar con gestoría o API de nóminas (Factorial, Personio, etc.)")

    db.close()
