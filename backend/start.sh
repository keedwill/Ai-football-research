#!/bin/bash
# Backend startup script for Render
# This ensures proper working directory and environment

cd backend
exec gunicorn app.main:app \
  --workers 2 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:$PORT \
  --log-level info \
  --access-logfile - \
  --error-logfile -
