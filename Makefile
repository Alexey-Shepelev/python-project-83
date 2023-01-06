install:
	poetry install

build:
	poetry build

package-install:
	python3 -m pip install --user dist/*.whl

package-reinstall:
	python3 -m pip install --user --force-reinstall dist/*.whl

package-uninstall:
	python3 -m pip uninstall --yes dist/*.whl

dev:
	poetry run flask --app page_analyzer:app --debug run

PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

lint:
	poetry run flake8 page_analyzer

#test:
#	poetry run pytest

#test-coverage:
#	poetry run pytest --cov=page_loader tests/ --cov-report xml

selfcheck:
	poetry check

check: selfcheck lint #test

.PHONY: install build publish
