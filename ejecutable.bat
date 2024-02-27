@echo off
cd /d C:\Users\Tsao\Documents\python scripts\agenda tsao
start /wait python -m pipenv shell /c python "reservas.py"
