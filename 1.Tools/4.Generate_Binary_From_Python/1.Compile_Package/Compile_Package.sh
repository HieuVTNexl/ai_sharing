#!/bin/bash

python3 -m compileall $1 -b
find $1 -name "*.py" -and -not -name "__init__.py" -type f -delete
find $1 -name "__init__.pyc" -type f -delete