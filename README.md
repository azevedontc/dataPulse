<h1 align="center">📊 DataPulse</h1>
<p align="center">Daily, data-driven insights in Python — fetch → clean → visualize → write.</p>

<p align="center">
  <img src="https://komarev.com/ghpvc/?username=azevedontc&label=views&color=blueviolet" alt="views"/>
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
## Output
```
# Clima (3 dias)
python -m datapulse.cli --source weather --city "São Paulo" --days 3

# Câmbio BRL/USD (7 dias)
python -m datapulse.cli --source fx --base BRL --quote USD --days 7

# Qualidade do ar (AQI, 3 dias)
python -m datapulse.cli --source aqi --city "São Paulo" --days 3
```

## Flags
```
# somente Markdown (sem PNG)
python -m datapulse.cli --source weather --city "Curitiba" --days 3 --no-plot

# somente PNG/Markdown (sem CSV)
python -m datapulse.cli --source fx --base BRL --quote USD --days 7 --no-csv
```

## Weekly
```
# via Makefile
make weekly-weather   # clima (últimos 7 CSVs)
make weekly-fx        # câmbio
make weekly-aqi       # qualidade do ar

# ou via Python
python -c "from datapulse import build_weekly_summary as b; b('reports','weather')"
```

## Qualidade do Código
```
ruff check . --fix
black .
pytest -q  # (opcional) pytest -q --cov=datapulse --cov-report=term-missing
```

## Rotina
```
# diário (no main)
source .venv/bin/activate
git pull
python -m datapulse.cli --source weather --city "São Paulo" --days 3
git add reports/
git commit -m "chore(reports): add daily report for YYYY-MM-DD"
git push

# semanal (1x/semana)
make weekly-weather
git add reports/
git commit -m "feat(summary): add weekly weather summary for YYYY-WW"
git push
```

## Arquivos Gerados

reports/YYYY-MM-DD.md
reports/img/YYYY-MM-DD_<source>.png
reports/YYYY-MM-DD_<source>.csv
reports/YYYY-MM-DD_<source>_weekly.md (semanal)
reports/img/YYYY-MM-DD_<source>_weekly.png