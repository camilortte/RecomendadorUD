python manage.py syncdb --noinput
python manage.py shell < notes.py
python manage.py loaddata tipos_usuarios.json
python manage.py loaddata categorias.json
python manage.py loaddata sub_categorias.json
python manage.py loaddata establecimientos.json
python manage.py loaddata tipos_solicitud.json
python manage.py rebuild_index --noinput
python manage.py runserver 0.0.0.0:8000
