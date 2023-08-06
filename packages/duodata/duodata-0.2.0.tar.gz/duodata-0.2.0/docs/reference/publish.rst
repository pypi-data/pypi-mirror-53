Releasing the project
=====================
Before releasing your package on PyPI you should have all the tox environments passing.

Version management
This template provides a basic bumpversion configuration. It's as simple as running:

bumpversion patch to increase version from 1.0.0 to 1.0.1.
bumpversion minor to increase version from 1.0.0 to 1.1.0.
bumpversion major to increase version from 1.0.0 to 2.0.0.
You should read Semantic Versioning 2.0.0 before bumping versions.

Building and uploading
Before building dists make sure you got a clean build area:

rm -rf build
rm -rf src/*.egg-info
tox -e check
python setup.py clean --all sdist bdist_wheel

twine upload --skip-existing dist/*.whl dist/*.gz dist/*.zip
