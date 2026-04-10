#!/bin/zsh

cd "$(dirname "$0")/.."
python3 generate_homepage.py
python3 generate_research.py
