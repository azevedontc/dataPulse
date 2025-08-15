# dataPulse

<h1 align="center">📊 DataPulse</h1>
<p align="center">Daily, data‑driven insights in Python — fetch → clean → visualize → write.</p>

<p align="center">
  <img src="https://komarev.com/ghpvc/?username=SEU_USER&label=views&color=blueviolet" />
</p>

## Sobre
**DataPulse** é um “diário de dados” em Python. Ele busca dados públicos (começando por clima via Open‑Meteo), transforma com `pandas`, gera um gráfico com `matplotlib` e salva um **relatório diário** em Markdown em `reports/` com a imagem em `reports/img/`.

---

## Quickstart

```bash
# clonar e preparar
git clone https://github.com/azevedontc/dataPulse
cd dataPulse
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# gerar relatório (ex.: 3 dias, São Paulo)
python -m datapulse.cli --source weather --city "São Paulo" --days 3
