web: gunicorn app:app --workers 1 --threads 2 --timeout 120 --keep-alive 5 --max-requests 1000 --max-requests-jitter 50 --worker-class sync --bind 0.0.0.0:$PORT

