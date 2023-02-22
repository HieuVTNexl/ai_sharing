#!/bin/bash

cd $1
python3 setup.py bdist_wheel
cp dist/*.whl ..