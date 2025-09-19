format:
\tblack .
lint:
\truff check .
test:
\tpytest -q
run:
\tpython -m datapulse.cli run --source weather --city "São Paulo" --days 3
\tpython -m datapulse.cli --source fx --base BRL --quote USD --days 7
\tpython -m datapulse.cli --source aqi --city "Medianeira" --days 3  