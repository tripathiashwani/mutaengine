#!/bin/bash



screen -S django -X stuff "pkill -f runserver\n"
screen -S django -X stuff "git fetch origin deployment && git reset --hard origin/deployment && pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput && python manage.py runserver 0.0.0.0:8000
\n"


# check if the pipeline is working testing pipeline test3 for the third time ,test4 for the fourth time