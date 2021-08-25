#!/bin/bash
cat config/prod_config.yaml | envsubst > config/config.yaml

set -e
cat config/config.yaml
alembic upgrade head
python main.py
