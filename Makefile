install:
	pip install poetry && \
	poetry install

start:
	poetry run python tg_bot.py