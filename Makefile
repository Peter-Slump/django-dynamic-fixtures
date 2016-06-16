
install-python:
	pip install --upgrade setuptools
	pip install -e .
	pip install "file://`pwd`#egg=django-dynamic-fixtures[dev,doc]"

bump-patch:
	bumpversion patch

bump-minor:
	bumpversion minor

deploy-pypi:
	python setup.py sdist bdist_wheel
	twine upload dist/*