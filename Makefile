main:
	uv run python main.py

devdb:
	psql -h 0.0.0.0 -U luis -d bitcoinpipeline