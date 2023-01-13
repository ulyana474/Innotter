#!/bin/bash
set -e
python3 -m uvicorn statisticService.main:app --host 0.0.0.0 --port 80 --reload
exec "$@"