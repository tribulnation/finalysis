mod finalysis

VENV := ".venv"
BIN := ".venv/bin"
PYTHON := ".venv/bin/python"

help:
  @just --list

init:
  rm -drf {{VENV}} || :
  python3.11 -m venv {{VENV}}
  {{PYTHON}} -m pip install --upgrade pip
  {{PYTHON}} -m pip install -r requirements.txt

app:
  {{BIN}}/streamlit run app.py