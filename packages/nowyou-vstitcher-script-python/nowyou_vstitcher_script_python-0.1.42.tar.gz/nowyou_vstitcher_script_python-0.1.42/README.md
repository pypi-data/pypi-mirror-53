# NowYou Grafits script python

## Create new version to Pypi
1. Increase version in `setup.py` file
1. Build: `python setup.py sdist bdist_wheel`
2. Upload: `python -m twine upload --skip-existing dist/*`

### Virtualenv
You can use `pipenv` tool for development: 
 - create virtualenv: `pipenv --python /path/to/python`
 - install dependencies: `pipenv lock && pipenv install`
 - open virtualenv shell: `pipenv shell` (optional)