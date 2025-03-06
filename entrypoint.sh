#!/bin/sh

alembic upgrade head

uvicorn pamps.app:app --reload --host=0.0.0.0 --port=8000