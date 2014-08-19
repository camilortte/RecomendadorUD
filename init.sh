python manage.py syncdb --noinput
python manage.py shell < notes.py
python manage.py loaddata tipos_usuarios.json
python manage.py runserver 0.0.0.0:8000
