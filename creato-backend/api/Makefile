FORCE:

tests: FORCE
	python3 -m autopep8 --in-place --aggressive --recursive --verbose .
	python3 manage.py test --with-coverage

prod: tests
	- pip freeze > requirements.txt
	git add .
	git commit -am "Make prod commit"
	git push origin master

dev_env: FORCE
	python3 -m pip install -r requirements.txt
	python3 manage.py runserver

docs: FORCE
	mkdir -p doc
	python3 django-pydoc.py -w api.views
	mv *.html doc