#!/bin/bash

set -ex

if [ "$TRAVIS_OS_NAME" = "osx" ]; then
    curl -Lo macpython.pkg https://www.python.org/ftp/python/${MACPYTHON}/python-${MACPYTHON}-macosx10.6.pkg
    sudo installer -pkg macpython.pkg -target /
    ls /Library/Frameworks/Python.framework/Versions/*/bin/
    PYTHON_EXE=/Library/Frameworks/Python.framework/Versions/*/bin/python3
    sudo $PYTHON_EXE -m pip install virtualenv
    $PYTHON_EXE -m virtualenv testenv
    source testenv/bin/activate
fi

pip install -U pip setuptools wheel

python setup.py sdist --formats=zip
pip install dist/*.zip

if [ "$CHECK_DOCS" = "1" ]; then
    pip install -Ur setup/rtd-requirements.txt
    cd docs
    # -n (nit-picky): warn on missing references
    # -W: turn warnings into errors
    sphinx-build -nW  -b html source build
else
    # Actual tests
    pip install -Ur setup/test-requirements.txt

    mkdir empty
    cd empty

    pytest -W error -ra -v --cov=trio_mysql --cov-config=../.coveragerc --verbose ../tests

    bash <(curl -s https://codecov.io/bash)
fi
