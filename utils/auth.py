import streamlit as st
from models import UserRole

def check_role(required_roles):
    if "user" not in st.session_state:
        return False
    return st.session_state.user.get("role") in [r.value for r in required_roles]

def require_login():
    if "user" not in st.session_state:
        st.warning("🔒 Acceso restringido. Inicia sesión.")
        st.stop()

def login_form():
    with st.form("login"):
        st.subheader("🔐 Iniciar sesión")
        user = st.text_input("Usuario")
        pwd = st.text_input("Contraseña", type="password")
        if st.form_submit_button("Entrar"):
            demo_users = {
                "admin": {"role": "admin", "name": "Administrador"},
                "ventas": {"role": "sales", "name": "Jefe Ventas"},
                "almacen": {"role": "warehouse", "name": "Responsable Almacén"},
                "contable": {"role": "accounting", "name": "Contable"},
            }
            if user in demo_users and pwd == user:
                st.session_state.user = {"username": user, **demo_users[user]}
                st.rerun()
            else:
                st.error("Credenciales incorrectas")

def logout():
    if st.sidebar.button("🚪 Cerrar sesión"):
        del st.session_state.user
        st.rerun()

def show_user_info():
    if "user" in st.session_state:
        name = st.session_state.user["name"]
        role = st.session_state.user["role"]
        st.sidebar.markdown("**👤 " + name + "**")
        st.sidebar.markdown("*Rol: " + role + "*")