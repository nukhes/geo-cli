#!/bin/bash

# Generate README.md

PYTHONPATH=src/ typer src/main.py utils docs --output README.md --name "geo-cli" --title "geo-cli"
