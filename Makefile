format:
	black .

lint:
	ruff check .

test:
	pytest -q

run:
	python -m datapulse.cli --source weather --city "São Paulo" --days 3
	python -m datapulse.cli --source fx --base BRL --quote USD --days 7
	python -m datapulse.cli --source aqi --city "Medianeira" --days 3

dashboard:
	python -m streamlit run app/streamlit_app.py

