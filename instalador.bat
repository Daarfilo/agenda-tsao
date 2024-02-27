@echo off
pip install pipenv
python -m pipenv install
python -m pipenv install -r requirements.txt
echo.
echo Instalación completada.
echo.
pause
