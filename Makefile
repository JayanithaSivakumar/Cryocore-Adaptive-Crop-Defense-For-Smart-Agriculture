PYTHON ?= python3

.PHONY: python-install python-api etl test demo
python-install:
	$(PYTHON) -m pip install -r python_core/requirements.txt
python-api:
	cd python_core && uvicorn app:app --reload --port 8790
etl:
	$(PYTHON) python_core/spark_etl.py
test:
	pytest python_core/tests
demo: etl
	@echo "Start the node API with: make python-api"
