#!/bin/bash

if [ ! -d ./_celery ]; then mkdir -p ./_celery; fi

rm -rf ./_celery/*.{pid,db}

if [ "$DEBUG" = "true" ]; then
    celery -A project worker --beat -l INFO -s ./_celery/celerybeat-schedule.db
else
    celery -A project multi start w1 \
        --pidfile="./_celery/%n.pid" \
        --logfile="./_celery/%n%I.log" \
        --loglevel=INFO \
        ${CELERY_OPTS:---time-limit=300 --concurrency=8}

    tail -f ./_celery/w*.log
fi
