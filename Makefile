# Makefile for ADAS CAN Sensor Simulator & Visualizer

# Python binary (override with `make PYTHON=python3.11` if needed)
PYTHON ?= python3

install:
	$(PYTHON) -m pip install -e .

run:
	$(PYTHON) src/main.py --mode live

replay:
	$(PYTHON) src/main.py --mode replay --file data/demo_drive_log.csv --delay 0.3

web:
	$(PYTHON) scripts/run_live_web.py

plot:
	$(PYTHON) scripts/plot_log.py

test:
	pytest

logs:
	@echo "Showing Dash logs:"
	tail -f logs/dash.log

lint:
	flake8 src tests

docker-build:
	docker build -t adas-can-demo .

docker-run-replay:
	docker run --rm -v "$(PWD)/data:/app/data" adas-can-demo

docker-run-web:
	docker run -p 8050:8050 \
		-v "$(PWD)/data:/app/data" \
		-v "$(PWD)/config:/app/config" \
		-v "$(PWD)/logs:/app/logs" \
		adas-can-demo python scripts/run_live_web.py

.PHONY: install run replay web plot test logs lint docker-build docker-run-replay docker-run-web
