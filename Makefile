restart:
	sudo sv restart sincity

update:
	git pull
	python manage.py migrate
	sudo sv restart sincity

.PHONY: restart update