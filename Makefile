format:
\tblack .
lint:
\truff check .
test:
\tpytest -q
run:
\tpython -m datapulse.cli run --source weather --city "São Paulo" --days 3
