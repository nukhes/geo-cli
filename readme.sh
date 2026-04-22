#!/bin/bash

# Generate README.md

PYTHONPATH=src/geociencias_cli typer src/geociencias_cli/main.py utils docs --output README.md --name "geo-cli" --title "geo-cli"
