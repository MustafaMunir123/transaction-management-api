migrations:
	python manage.py makemigrations && python manage.py runserver
run:
	python manage.py runserver
.PHONY: activate migrations run