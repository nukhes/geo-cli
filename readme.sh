#!/bin/bash
source .venv/bin/activate
python -m typer src/geociencias_cli/main.py utils docs --output README.md --name "geo-cli" --title "geo-cli"
