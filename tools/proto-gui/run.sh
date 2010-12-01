#!/bin/sh
export VERSIONER_PYTHON_PREFER_32_BIT=yes
export PYTHONPATH=$PYTHONPATH:../../libs/pycloudvibe/
python proto-gui.py
