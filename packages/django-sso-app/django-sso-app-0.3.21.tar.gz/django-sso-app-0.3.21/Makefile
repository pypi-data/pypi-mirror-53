DOCKER=docker
DPATH=${CURDIR}

export DPATH
.PHONY:	clean build publish

clean:
	rm -rf ./dist/*

build-release:
	python setup.py sdist bdist_wheel

publish:
	twine upload dist/* --verbose
