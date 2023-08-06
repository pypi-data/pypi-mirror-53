...
pipenv uninstall dps-rtm
pipenv install
python setup.py sdist bdist_wheel
python -m pip install -e .

pipenv install dist\dps_rtm-0.1.14-py3-none-any.whl
