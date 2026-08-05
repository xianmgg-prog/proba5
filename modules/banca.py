import streamlit as st
from config import SANDBOX_CONFIG

def show():
    st.header("🏦 Integración Bancaria (Open Banking)")

    st.warning("🔒 Sandbox Mode — No se accede a cuentas reales. Preparado para agregadores homologados.")

    st.subheader("1. Agregadores Soportados")
    for key, info in SANDBOX_CONFIG.items():
        if "bank" in key or key in ["gocardless", "plaid"]:
            with st.container(border=True):
                st.markdown(f"**{info['name']}**")
                st.markdown(f"🔗 [Documentación Sandbox]({info['sandbox_url']})")
                st.caption(info['notes'])

    st.subheader("2. Flujo de Conexión PSD2")
    st.markdown("Paso 1: Registro en sandbox del agregador")
    st.markdown("Paso 2: Crear app y obtener client_id + secret")
    st.markdown("Paso 3: Usuario autoriza acceso vía SCA (doble factor)")
    st.markdown("Paso 4: Lectura de movimientos y saldos en tiempo real")
    st.markdown("Paso 5: Iniciar pagos con consentimiento explícito")

    st.subheader("3. Simulación Actual")
    st.info("Los datos de banco en Finanzas > Banco son mock. Para activar integración real configura en .env:")
    st.code("GOCARDLESS_ACCESS_TOKEN=tu_token_sandbox\nPLAID_CLIENT_ID=tu_client_id\nPLAID_SECRET=tu_secret_sandbox", language="bash")

    st.subheader("4. Cumplimiento Legal")
    st.markdown("- PSD2: Requiere consentimiento explícito del titular")
    st.markdown("- SCA: Autenticación fuerte (2FA) para iniciar pagos")
    st.markdown("- RGPD: Datos bancarios sensibles — cifrado AES-256 requerido")
    st.markdown("- Registro: Agregador debe estar registrado en Banco de España / ACPR")
