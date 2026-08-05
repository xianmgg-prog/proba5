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
        st.markdown("<p style='color:#64748b;font-size:0.85rem;margin-bottom:1rem;'>Inicia sesión para continuar</p>", unsafe_allow_html=True)
        user = st.text_input("Usuario", placeholder="admin", label_visibility="collapsed")
        pwd = st.text_input("Contraseña", type="password", placeholder="••••••", label_visibility="collapsed")

        cols = st.columns([1,1])
        with cols[0]:
            remember = st.checkbox("Recordarme", value=True)
        with cols[1]:
            st.markdown("<p style='text-align:right;font-size:0.8rem;color:#00b4d8;'>¿Olvidaste la contraseña?</p>", unsafe_allow_html=True)

        if st.form_submit_button("🔐 Entrar al sistema", use_container_width=True):
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
                st.error("❌ Credenciales incorrectas", icon="⚠️")

def logout():
    if st.sidebar.button("🚪 Cerrar sesión", use_container_width=True):
        del st.session_state.user
        st.rerun()

def show_user_info():
    if "user" in st.session_state:
        name = st.session_state.user["name"]
        role = st.session_state.user["role"]
        role_colors = {"admin": "#10b981", "sales": "#f59e0b", "warehouse": "#00b4d8", "accounting": "#8b5cf6"}
        role_color = role_colors.get(role, "#64748b")
        st.sidebar.markdown(f"""
        <div style="background:rgba(255,255,255,0.05);border-radius:0.75rem;padding:0.75rem 1rem;margin-bottom:1rem;">
            <div style="display:flex;align-items:center;gap:0.75rem;">
                <div style="width:36px;height:36px;background:{role_color};border-radius:50%;display:flex;align-items:center;justify-content:center;color:white;font-weight:700;font-size:0.85rem;">{name[0]}</div>
                <div>
                    <div style="color:white;font-weight:600;font-size:0.85rem;">{name}</div>
                    <div style="color:rgba(255,255,255,0.5);font-size:0.7rem;text-transform:uppercase;letter-spacing:0.05em;">{role}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
