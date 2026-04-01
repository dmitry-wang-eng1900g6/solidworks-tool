.PHONY: install test lint run clean

install:
	pip install -r requirements.txt

test:
	pytest tests/ -v

lint:
	ruff check .

run:
	python main.py

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	rm -rf .pytest_cache .ruff_cache *.egg-info dist build
