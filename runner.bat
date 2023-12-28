@echo off

mode con: cols=205 lines=76

pip install -r requirements.txt --quiet
python script.py