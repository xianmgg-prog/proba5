import streamlit as st
from database import SessionLocal
from models import ApiCredential
import pandas as pd

SERVICES = {
    "gocardless": {
        "name": "GoCardless Bank Account Data",
        "fields": ["access_token", "client_secret"],
        "url": "https://developer.gocardless.com/",
        "help": "Regístrate → Crea app en sandbox → Copia access_token y secret_id"
    },
    "plaid": {
        "name": "Plaid",
        "fields": ["client_id", "client_secret", "access_token"],
        "url": "https://plaid.com/docs/quickstart/",
        "help": "Cuenta sandbox gratuita. Usa environment='sandbox'"
    },
    "google_ads": {
        "name": "Google Ads API",
        "fields": ["developer_token", "client_id", "client_secret", "access_token", "refresh_token", "account_id"],
        "url": "https://developers.google.com/google-ads/api/docs/start",
        "help": "Necesitas cuenta de Google Ads de prueba y developer token"
    },
    "meta_ads": {
        "name": "Meta Marketing API",
        "fields": ["access_token", "account_id"],
        "url": "https://developers.facebook.com/docs/marketing-api/overview",
        "help": "Usa Graph API Explorer con token de prueba. account_id = act_XXXXX"
    },
    "linkedin_ads": {
        "name": "LinkedIn Marketing API",
        "fields": ["client_id", "client_secret", "access_token", "account_id"],
        "url": "https://learn.microsoft.com/en-us/linkedin/marketing/",
        "help": "Cuenta de desarrollador + app en LinkedIn Developers"
    },
    "openai": {
        "name": "OpenAI (Agentes / Copy)",
        "fields": ["access_token"],
        "url": "https://platform.openai.com/api-keys",
        "help": "Crea una API key en platform.openai.com"
    }
}

def show():
    st.header("🔌 Integraciones y APIs")
    st.markdown("Configura aquí las credenciales de cada servicio. Se guardan en la base de datos de forma segura.")

    db = SessionLocal()

    tab1, tab2 = st.tabs(["Configurar APIs", "Estado de Conexiones"])

    with tab1:
        for key, info in SERVICES.items():
            with st.expander(f"**{info['name']}**"):
                st.markdown(f"🔗 [Documentación]({info['url']})")
                st.caption(info['help'])

                # Obtener credencial existente
                cred = db.query(ApiCredential).filter_by(service=key).first()

                with st.form(f"form_{key}"):
                    vals = {}
                    for field in info['fields']:
                        existing = getattr(cred, field, "") if cred else ""
                        # Ocultar tokens sensibles
                        is_secret = "token" in field or "secret" in field
                        vals[field] = st.text_input(
                            field.replace("_", " ").title(), 
                            value=existing or "",
                            type="password" if is_secret else "default"
                        )

                    sandbox = st.toggle("Modo Sandbox", value=cred.sandbox_mode if cred else True)
                    active = st.toggle("Activar", value=cred.is_active if cred else False)
                    notes = st.text_area("Notas", value=cred.notes if cred else "")

                    if st.form_submit_button("💾 Guardar"):
                        if not cred:
                            cred = ApiCredential(service=key, name=info['name'])
                            db.add(cred)

                        for field, val in vals.items():
                            setattr(cred, field, val)
                        cred.sandbox_mode = sandbox
                        cred.is_active = active
                        cred.notes = notes
                        db.commit()
                        st.success(f"✅ {info['name']} guardado")
                        st.rerun()

    with tab2:
        st.subheader("Estado de tus conexiones")
        creds = db.query(ApiCredential).all()

        if not creds:
            st.info("No hay APIs configuradas todavía. Ve a 'Configurar APIs'.")
        else:
            data = []
            for c in creds:
                status = "🟢 Activa" if c.is_active else "🔴 Inactiva"
                mode = "🧪 Sandbox" if c.sandbox_mode else "🚀 Producción"
                data.append({
                    "Servicio": c.name,
                    "Estado": status,
                    "Modo": mode,
                    "Última actualización": c.updated_at
                })
            st.dataframe(pd.DataFrame(data), use_container_width=True)

            st.divider()
            st.subheader("🧪 Probar conexión (Mock)")
            selected = st.selectbox("Seleccionar servicio", [c.service for c in creds])
            if st.button("Probar conexión"):
                cred = db.query(ApiCredential).filter_by(service=selected).first()
                if not cred.is_active:
                    st.error("El servicio está inactivo. Actívalo primero.")
                elif not cred.access_token:
                    st.error("Falta access_token.")
                else:
                    # Aquí iría la llamada real a la API
                    st.success(f"✅ Conexión simulada exitosa con {cred.name}")
                    st.balloons()
                    st.caption("(En producción: aquí se haría la llamada real a la API y se mostrarían los datos)")

    db.close()
