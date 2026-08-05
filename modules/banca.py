import streamlit as st
from database import SessionLocal
from models import ApiCredential
from utils.theme import section_header

def show():
    section_header("Banca", "Integración Open Banking")
    db = SessionLocal()
    gocardless = db.query(ApiCredential).filter_by(service="gocardless").first()
    plaid = db.query(ApiCredential).filter_by(service="plaid").first()
    db.close()

    col1, col2 = st.columns(2)
    with col1:
        st.metric("GoCardless", "Conectado" if (gocardless and gocardless.is_active) else "No configurado")
    with col2:
        st.metric("Plaid", "Conectado" if (plaid and plaid.is_active) else "No configurado")

    if not gocardless and not plaid:
        st.info("No tienes APIs bancarias configuradas. Ve a Integraciones para añadirlas.")

    st.markdown("**Agregadores soportados**")
    st.markdown("• **GoCardless** — [Documentación](https://developer.gocardless.com/)")
    st.markdown("• **Plaid** — [Documentación](https://plaid.com/docs/quickstart/)")
    st.markdown("• **Redsys** — [Documentación](https://pagosonline.redsys.es/)")

    st.markdown("**Flujo PSD2**")
    st.markdown("1. Registro en sandbox del agregador")
    st.markdown("2. Crear app y obtener credenciales")
    st.markdown("3. Usuario autoriza acceso vía SCA")
    st.markdown("4. Lectura de movimientos y saldos")
    st.markdown("5. Iniciar pagos con consentimiento")

    st.markdown("**Cumplimiento legal**")
    st.markdown("• PSD2: consentimiento explícito del titular")
    st.markdown("• SCA: autenticación fuerte para pagos")
    st.markdown("• RGPD: cifrado AES-256 para datos bancarios")
