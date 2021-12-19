celery -A affi worker --loglevel=debug --concurrency=8 &
celery -A affi beat -l debug &