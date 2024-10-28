echo "at gunicorn.sh"
cd /var/lib/jenkins/workspace/career_backend
. venv/bin/activate


echo "$PWD"
echo "Migrations started" 
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py collectstatic -- no-input

python3 manage.py runserver