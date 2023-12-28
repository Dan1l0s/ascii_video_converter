#!/bin/bash

width=205
height=76

resize -s $height $width

pip install -r requirements.txt --quiet
python script.py