#!/bin/bash
set -e
celery -A app worker -B -l info
exec "$@"