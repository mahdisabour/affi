celery -A affi worker --loglevel=debug --concurrency=8 &
celery -A bot beat -l debug &