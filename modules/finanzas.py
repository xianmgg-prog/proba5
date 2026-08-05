import streamlit as st
from database import SessionLocal
from models import Account, JournalEntry, BankTransaction, Invoice, InvoiceStatus
from utils.helpers import format_currency
from sqlalchemy import func
from sqlalchemy.orm import joinedload
import pandas as pd
from datetime import date

@st.cache_data(ttl=30)
def get_accounts():
    db = SessionLocal()
    result = db.query(Account).all()
    db.close()
    return result

@st.cache_data(ttl=30)
def get_journal_entries():
    db = SessionLocal()
    result = db.query(JournalEntry).order_by(JournalEntry.date.desc()).all()
    db.close()
    return result

@st.cache_data(ttl=30)
def get_bank_transactions():
    db = SessionLocal()
    result = db.query(BankTransaction).options(joinedload(BankTransaction.invoice)).order_by(BankTransaction.date.desc()).all()
    db.close()
    return result

def show():
    st.header("💼 Finanzas y Contabilidad")
    db = SessionLocal()

    tab1, tab2, tab3, tab4 = st.tabs(["Cuentas", "Libro Diario", "Banco / Sandbox", "Balance"])

    with tab1:
        accounts = get_accounts()
        data = [{"Código": a.code, "Nombre": a.name, "Tipo": a.type.value, "Saldo": format_currency(a.balance)} for a in accounts]
        st.dataframe(pd.DataFrame(data), use_container_width=True)

    with tab2:
        entries = get_journal_entries()
        data = []
        for e in entries:
            data.append({
                "Fecha": e.date,
                "Ref": e.reference,
                "Descripción": e.description,
                "Debe": format_currency(e.amount) if e.debit_account_id else "",
                "Haber": format_currency(e.amount) if e.credit_account_id else "",
            })
        st.dataframe(pd.DataFrame(data), use_container_width=True)

    with tab3:
        st.info("🏦 **Modo Sandbox** — Conectado a datos simulados de BBVA Sandbox")
        st.markdown("Para conectar con banco real, configura las credenciales en `.env` (ver docs/sandbox_banking.md)")

        txs = get_bank_transactions()
        data = []
        for t in txs:
            data.append({
                "Fecha": t.date,
                "Concepto": t.description,
                "Importe": format_currency(t.amount),
                "Saldo": format_currency(t.balance),
                "Conciliado": "✅" if t.is_reconciled else "❌",
                "Factura": t.invoice_id or "-",
                "Origen": t.source
            })
        st.dataframe(pd.DataFrame(data), use_container_width=True)

        if st.button("🔄 Simular conciliación automática"):
            pending_invs = db.query(Invoice).filter(Invoice.status == InvoiceStatus.sent).all()
            for inv in pending_invs:
                tx = db.query(BankTransaction).filter(
                    BankTransaction.amount > 0,
                    BankTransaction.is_reconciled == False
                ).first()
                if tx:
                    tx.is_reconciled = True
                    tx.invoice_id = inv.id
                    inv.status = InvoiceStatus.paid
                    inv.paid_date = date.today()
            db.commit()
            st.success("Conciliación simulada completada")
            st.cache_data.clear()
            st.rerun()

    with tab4:
        st.subheader("Balance Simplificado")
        assets = db.query(func.sum(Account.balance)).filter(Account.type == "activo").scalar() or 0
        liabilities = db.query(func.sum(Account.balance)).filter(Account.type == "pasivo").scalar() or 0
        equity = db.query(func.sum(Account.balance)).filter(Account.type == "patrimonio").scalar() or 0
        income = db.query(func.sum(Account.balance)).filter(Account.type == "ingreso").scalar() or 0
        expense = db.query(func.sum(Account.balance)).filter(Account.type == "gasto").scalar() or 0

        col1, col2 = st.columns(2)
        with col1:
            st.metric("ACTIVO", format_currency(assets))
            st.metric("PASIVO", format_currency(liabilities))
            st.metric("PATRIMONIO", format_currency(equity))
        with col2:
            st.metric("INGRESOS", format_currency(income))
            st.metric("GASTOS", format_currency(expense))
            result = float(income) - float(expense)
            st.metric("RESULTADO", format_currency(result), delta=f"{'Beneficio' if result > 0 else 'Pérdida'}")

    db.close()
