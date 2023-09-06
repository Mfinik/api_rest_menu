#!/bin/sh
export PYTHONPATH=.
poetry run alembic -c alembic/alembic.ini revision --autogenerate -m "add_ololo_to_menu"
poetry run alembic -c alembic/alembic.ini upgrade head
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000
