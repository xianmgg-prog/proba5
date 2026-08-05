import streamlit as st
from database import SessionLocal
from models import ApiCredential
from config import SANDBOX_CONFIG

def show():
    st.header("🏦 Integración Bancaria (Open Banking)")
    db = SessionLocal()

    # Leer credenciales guardadas
    gocardless = db.query(ApiCredential).filter_by(service="gocardless").first()
    plaid = db.query(ApiCredential).filter_by(service="plaid").first()
    db.close()

    col1, col2 = st.columns(2)
    with col1:
        st.metric("GoCardless", "🟢 Configurado" if (gocardless and gocardless.is_active) else "🔴 No configurado")
    with col2:
        st.metric("Plaid", "🟢 Configurado" if (plaid and plaid.is_active) else "🔴 No configurado")

    if not gocardless and not plaid:
        st.warning("🔧 No tienes APIs bancarias configuradas. Ve a **🔌 Integraciones** para añadirlas.")

    st.divider()
    st.subheader("1. Agregadores Soportados")
    for key, info in SANDBOX_CONFIG.items():
        if "bank" in key or key in ["gocardless", "plaid"]:
            with st.container(border=True):
                st.markdown(f"**{info['name']}**")
                st.markdown(f"🔗 [Documentación Sandbox]({info['sandbox_url']})")
                st.caption(info['notes'])

    st.subheader("2. Flujo de Conexión PSD2")
    st.markdown("1. Registro en sandbox del agregador")
    st.markdown("2. Crear app y obtener client_id + secret")
    st.markdown("3. Usuario autoriza acceso vía SCA (doble factor)")
    st.markdown("4. Lectura de movimientos y saldos en tiempo real")
    st.markdown("5. Iniciar pagos con consentimiento explícito")

    st.subheader("3. Datos Actuales")
    st.info("Los datos de banco que ves en Finanzas > Banco son generados por mock.")

    if gocardless and gocardless.is_active:
        st.success(f"✅ GoCardless configurado (Sandbox: {gocardless.sandbox_mode})")
        st.code(f"Access Token: {'*' * 10}{gocardless.access_token[-4:] if gocardless.access_token else 'N/A'}")
        if st.button("🔄 Sincronizar con GoCardless"):
            st.info("(Aquí iría la llamada real a la API de GoCardless)")

    if plaid and plaid.is_active:
        st.success(f"✅ Plaid configurado (Sandbox: {plaid.sandbox_mode})")
        st.code(f"Client ID: {'*' * 10}{plaid.client_id[-4:] if plaid.client_id else 'N/A'}")
        if st.button("🔄 Sincronizar con Plaid"):
            st.info("(Aquí iría la llamada real a la API de Plaid)")

    st.subheader("4. Cumplimiento Legal")
    st.markdown("- PSD2: Requiere consentimiento explícito del titular")
    st.markdown("- SCA: Autenticación fuerte (2FA) para iniciar pagos")
    st.markdown("- RGPD: Datos bancarios sensibles — cifrado AES-256 requerido")
    st.markdown("- Registro: Agregador debe estar registrado en Banco de España / ACPR")
