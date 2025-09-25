<h1 align="center">📊 DataPulse</h1>
<p align="center">Daily, data-driven insights in Python — fetch → clean → visualize → write.</p>

<p align="center">
  <img src="https://img.shields.io/badge/license-MIT-informational" alt="license"/>
  <img src="https://img.shields.io/badge/python-3.11%2B-blue" alt="python"/>
</p>

## Funcionalidades
- **3 fontes**: `weather` (Open-Meteo), `fx` (exchangerate.host) e **`aqi`** (Open-Meteo Air Quality).  
- **Flags**: `--no-csv` e `--no-plot` para controlar o que salvar.  
- **Relatórios semanais**: agregam os últimos 7 CSVs por fonte.  
- **Robustez**: geocoding automático, retry/backoff, cache diário, índice em `/reports/README.md`.

## Quickstart
```
bash
git clone https://github.com/azevedontc/dataPulse
cd dataPulse
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
## Diário
```
# Clima (3 dias)
python3 -m datapulse.cli --source weather --city "São Paulo" --days 3

# Câmbio BRL/USD (7 dias)
python3 -m datapulse.cli --source fx --base BRL --quote USD --days 7

# Qualidade do ar (AQI, 3 dias)
python3 -m datapulse.cli --source aqi --city "São Paulo" --days 3
```

## Semanal
```
# via Makefile
make weekly-weather   # clima (últimos 7 CSVs)
make weekly-fx        # câmbio
make weekly-aqi       # qualidade do ar

# ou via Python
python -c "from datapulse import build_weekly_summary as b; b('reports','weather')"
```

## Rotina
```
# diário (no main)
source .venv/bin/activate
git pull
python3 -m datapulse.cli --source weather --city "São Paulo" --days 3
python3 -m datapulse.cli --source fx --base BRL --quote USD --days 7
python3 -m datapulse.cli --source aqi --city "São Paulo" --days 3
git add reports/
git commit -m "chore(reports): add daily report for YYYY-MM-DD"
git push

# semanal (1x/semana)
make weekly-weather
git add reports/
git commit -m "feat(summary): add weekly weather summary for YYYY-WW"
git push
```

### Dashboard (Streamlit)
```
# instalar dependência (se ainda não tiver)
pip install streamlit

# rodar
make dashboard
# ou
streamlit run streamlit_app.py
```