import streamlit as st
from decimal import Decimal

def format_currency(value):
    if value is None:
        return "0,00 €"
    return f"{float(value):,.2f} €".replace(",", "X").replace(".", ",").replace("X", ".")

def format_number(value):
    if value is None:
        return "0"
    return f"{int(value):,}".replace(",", ".")

def status_badge(status):
    colors = {
        "borrador": "⚪",
        "pendiente": "🟡",
        "aprobada": "🟢",
        "recibida": "🔵",
        "cancelada": "🔴",
        "enviada": "🟠",
        "pagada": "🟢",
        "vencida": "🔴",
        "anulada": "⚫",
        "activa": "🟢",
        "pausada": "🟡",
    }
    return f"{colors.get(status, '⚪')} {status.upper()}"
