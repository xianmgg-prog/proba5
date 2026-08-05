import pandas as pd
from typing import Optional, Dict


def status_badge(value: str) -> str:
    """Devuelve un badge HTML según el estado."""
    v = str(value).lower().strip()
    styles = {
        "activo": ("#059669", "#d1fae5"),
        "active": ("#059669", "#d1fae5"),
        "pagado": ("#059669", "#d1fae5"),
        "paid": ("#059669", "#d1fae5"),
        "completado": ("#059669", "#d1fae5"),
        "completed": ("#059669", "#d1fae5"),
        "entregado": ("#059669", "#d1fae5"),
        "delivered": ("#059669", "#d1fae5"),
        "pendiente": ("#d97706", "#fef3c7"),
        "pending": ("#d97706", "#fef3c7"),
        "en proceso": ("#d97706", "#fef3c7"),
        "processing": ("#d97706", "#fef3c7"),
        "enviado": ("#2563eb", "#dbeafe"),
        "shipped": ("#2563eb", "#dbeafe"),
        "cancelado": ("#dc2626", "#fee2e2"),
        "cancelled": ("#dc2626", "#fee2e2"),
        "baja": ("#dc2626", "#fee2e2"),
        "low": ("#dc2626", "#fee2e2"),
        "crítico": ("#dc2626", "#fee2e2"),
        "critical": ("#dc2626", "#fee2e2"),
        "agotado": ("#dc2626", "#fee2e2"),
        "out of stock": ("#dc2626", "#fee2e2"),
        "medio": ("#d97706", "#fef3c7"),
        "medium": ("#d97706", "#fef3c7"),
        "alto": ("#059669", "#d1fae5"),
        "high": ("#059669", "#d1fae5"),
        "disponible": ("#059669", "#d1fae5"),
        "available": ("#059669", "#d1fae5"),
        "inactivo": ("#64748b", "#f1f5f9"),
        "inactive": ("#64748b", "#f1f5f9"),
    }
    color, bg = styles.get(v, ("#475569", "#f1f5f9"))
    return f'<span style="display:inline-block;padding:3px 10px;border-radius:6px;font-size:0.72rem;font-weight:700;color:{color};background:{bg};">{value}</span>'


def currency_fmt(val) -> str:
    return f"€{val:,.2f}" if pd.notna(val) else "—"


def percent_fmt(val) -> str:
    return f"{val:.1f}%" if pd.notna(val) else "—"


def int_fmt(val) -> str:
    return f"{val:,}" if pd.notna(val) else "—"


def pro_table(
    df: pd.DataFrame,
    title: Optional[str] = None,
    columns_config: Optional[Dict[str, Dict]] = None,
    height: Optional[int] = None,
    max_rows: int = 50,
    show_index: bool = False,
    empty_msg: str = "No hay datos disponibles",
) -> None:
    """
    Renderiza una tabla profesional con HTML/CSS puro.
    """
    import streamlit as st

    if df.empty:
        st.info(empty_msg)
        return

    df = df.head(max_rows).copy()
    if not show_index:
        df = df.reset_index(drop=True)

    cfg = columns_config or {}
    for col in df.columns:
        if col not in cfg:
            cfg[col] = {}

    thead = ""
    for col in df.columns:
        c = cfg.get(col, {})
        label = c.get("label", col)
        align = c.get("align", "left")
        width = c.get("width", "")
        w_style = f"width:{width};" if width else ""
        thead += f'<th style="text-align:{align};{w_style}">{label}</th>'

    tbody = ""
    for _, row in df.iterrows():
        tbody += "<tr>"
        for col in df.columns:
            c = cfg.get(col, {})
            align = c.get("align", "left")
            typ = c.get("type", "text")
            val = row[col]

            if typ == "status":
                cell = status_badge(val)
            elif typ == "currency":
                cell = currency_fmt(val)
            elif typ == "percent":
                cell = percent_fmt(val)
            elif typ == "int":
                cell = int_fmt(val)
            else:
                cell = str(val) if pd.notna(val) else "—"

            tbody += f'<td style="text-align:{align};">{cell}</td>'
        tbody += "</tr>"

    h_style = f"max-height:{height}px;" if height else ""
    overflow = "overflow-y:auto;" if height else ""

    html = f"""
    <style>
    .pro-table-wrap {{
        background: white;
        border-radius: 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 4px 12px rgba(0,0,0,0.02);
        border: 1px solid #f1f5f9;
        overflow: hidden;
        margin-bottom: 18px;
    }}
    .pro-table-title {{
        padding: 18px 22px 0;
        font-size: 0.95rem;
        font-weight: 700;
        color: #0f172a;
    }}
    .pro-table-scroll {{
        {overflow}
        {h_style}
        padding: 14px 22px 18px;
    }}
    .pro-table {{
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        font-size: 0.82rem;
    }}
    .pro-table thead th {{
        position: sticky;
        top: 0;
        background: #f8fafc;
        color: #64748b;
        font-weight: 700;
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        padding: 10px 12px;
        border-bottom: 1.5px solid #e2e8f0;
        white-space: nowrap;
    }}
    .pro-table tbody td {{
        padding: 12px;
        color: #334155;
        border-bottom: 1px solid #f1f5f9;
        vertical-align: middle;
    }}
    .pro-table tbody tr:last-child td {{
        border-bottom: none;
    }}
    .pro-table tbody tr:hover td {{
        background: #f8fafc;
        transition: background 0.15s;
    }}
    .pro-table-footer {{
        padding: 10px 22px;
        border-top: 1px solid #f1f5f9;
        color: #94a3b8;
        font-size: 0.75rem;
        font-weight: 500;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}
    </style>
    <div class="pro-table-wrap">
        {f'<div class="pro-table-title">{title}</div>' if title else ''}
        <div class="pro-table-scroll">
            <table class="pro-table">
                <thead><tr>{thead}</tr></thead>
                <tbody>{tbody}</tbody>
            </table>
        </div>
        <div class="pro-table-footer">
            <span>Mostrando {len(df)} de {len(df)} registros</span>
            <span>Actualizado hace un momento</span>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
