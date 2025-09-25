# streamlit_app.py
from __future__ import annotations

from datetime import date, timedelta

import pandas as pd
import streamlit as st

from datapulse.datasets import load_reports_csvs

st.set_page_config(page_title="DataPulse Dashboard", page_icon="📊", layout="wide")

st.title("📊 DataPulse Dashboard")
st.caption("Explore seus relatórios diários — weather • fx • aqi")

# --- sidebar filters ---
with st.sidebar:
    st.header("Filtros")
    srcs = st.multiselect(
        "Fontes", ["weather", "fx", "aqi"], default=["weather", "fx", "aqi"]
    )
    # range de datas padrão: últimos 14 dias
    today = date.today()
    start_default = today - timedelta(days=14)
    start, end = st.date_input(
        "Intervalo de datas", value=(start_default, today), max_value=today
    )
    st.markdown("---")
    st.caption(
        "Gere novos relatórios com `python -m datapulse.cli` e recarregue a página."
    )

# --- load data ---
df = load_reports_csvs(source=None)
if df.empty:
    st.info("Nenhum CSV encontrado em `reports/`. Gere relatórios primeiro.")
    st.stop()

df["date"] = pd.to_datetime(df["date"])
start_ts = pd.to_datetime(start)
end_ts = pd.to_datetime(end)

# filtros
if srcs:
    df = df[df["source"].isin(srcs)]
df = df[(df["date"] >= start_ts) & (df["date"] <= end_ts)]

if df.empty:
    st.warning("Sem dados para os filtros selecionados.")
    st.stop()

# --- KPIs ---
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Registros", len(df))
with col2:
    st.metric("Fontes ativas", df["source"].nunique())
with col3:
    first, last = df["date"].min().date(), df["date"].max().date()
    st.metric("Período", f"{first} → {last}")

st.markdown("### Série temporal")
# pivot para plotar várias fontes lado a lado
pv = df.pivot_table(index="date", columns="source", values="value", aggfunc="mean")
st.line_chart(pv)

st.markdown("### Tabela detalhada")
st.dataframe(
    df.sort_values(["source", "date"], ascending=[True, False]),
    use_container_width=True,
)

st.markdown("### Arquivos de origem")
st.write(df.groupby(["source", "file"]).size().reset_index(name="rows"))
