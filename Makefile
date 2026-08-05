runserver:
	python manage.py runserver

mig:
	python manage.py makemigrations && python manage.py migrate

admin:
	python manage.py createsuperuser

regions:
	python manage.py loaddata apps/shared/regions.json

runserver2:
	python manage.py runserver 8001

regions:
	python manage.py loaddata apps/shared/regions