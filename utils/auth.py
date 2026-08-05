import streamlit as st
from models import UserRole

def check_role(required_roles):
    if "user" not in st.session_state:
        return False
    return st.session_state.user.get("role") in [r.value for r in required_roles]

def require_login():
    if "user" not in st.session_state:
        st.stop()

def login_form():
    with st.form("login", border=False):
        st.markdown("<p style='color:#6b7280;font-size:0.8125rem;margin-bottom:1.25rem;'>Inicia sesión para continuar</p>", unsafe_allow_html=True)
        user = st.text_input("Usuario", placeholder="admin")
        pwd = st.text_input("Contraseña", type="password", placeholder="••••••")

        if st.form_submit_button("Entrar", use_container_width=True):
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
    if st.sidebar.button("Cerrar sesión", use_container_width=True):
        del st.session_state.user
        st.rerun()

def show_user_info():
    if "user" in st.session_state:
        name = st.session_state.user["name"]
        role = st.session_state.user["role"]
        role_labels = {"admin": "Admin", "sales": "Ventas", "warehouse": "Almacén", "accounting": "Contable"}
        st.sidebar.markdown(f"""
        <div style="background:#1f2937;border-radius:0.375rem;padding:0.625rem 0.875rem;margin-bottom:0.75rem;">
            <div style="color:#f3f4f6;font-weight:600;font-size:0.8125rem;">{name}</div>
            <div style="color:#6b7280;font-size:0.6875rem;text-transform:uppercase;letter-spacing:0.05em;">{role_labels.get(role, role)}</div>
        </div>
        """, unsafe_allow_html=True)
