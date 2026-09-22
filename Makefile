UV = uv

.PHONY: all run clean fclean re test flake8 mypy check

all: run

run:
	$(UV) run python -m src.main $(MAP)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .mypy_cache .pytest_cache

fclean: clean
	rm -rf .venv .vscode

re: fclean all

test:
	PYTHONPATH=. $(UV) run pytest

flake8:
	$(UV) run flake8 src

mypy:
	$(UV) run mypy -p src

check: flake8 mypy test