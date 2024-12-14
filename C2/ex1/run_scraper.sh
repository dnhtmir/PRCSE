#!/bin/bash
cd "$(dirname "$0")"
python3 ex1.py C2/ex1/generated > C2/ex1/generated/report_$(date +%Y-%m-%d).txt