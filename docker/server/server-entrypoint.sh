#!/bin/sh

alembic upgrade head

exec fastapi run