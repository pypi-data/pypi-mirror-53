.PHONY: init publish clean

IMAGE = deep3/news2play:latest
PYPI_USERNAME = __token__
PYPI_PASSWORD = pypi-AgEIcHlwaS5vcmcCJDgzNTc2OWQ4LTlmNzUtNDBjYy05YTQ4LWU0YmVlNzc4OGNiOQACOnsicGVybWlzc2lvbnMiOiB7InByb2plY3RzIjogWyJuZXdzMnBsYXkiXX0sICJ2ZXJzaW9uIjogMX0AAAYgy9B6pTDSOWod4rH5-cuEHqJKOka70Oj4vLJll5HD1Qg
CONTAINER_DIR = $(pwd)/app/storage
HOST_DIR = ~/.new2play_storage

init: Pipfile
	pip3 install pipenv --upgrade
	pipenv install --dev
# tag commit, before use publish
publish:
	echo [pypi] > ~/.pypirc
	echo "username=$(PYPI_USERNAME)" >> ~/.pypirc
	echo "password=$(PYPI_PASSWORD)" >> ~/.pypirc

	rm -rf build dist .eggs *.egg-info

	pip3 install 'twine>=1.5.0'
	python3 setup.py publish

	rm -rf build dist .eggs *.egg-info

	rm ~/.pypirc
clean:
	rm -rf build dist .eggs *.egg-info
docker_build:
	docker build --no-cache -t $(IMAGE) .
docker_push:
	docker push $(IMAGE)
docker_run:
# docker run will search local first, but docker push will always pull the latest
# in registry(example:docker hub), so use pull to synchronize local with latest image.
	docker pull $(IMAGE)
	docker run -it -v $(HOST_DIR):$(CONTAINER_DIR) -p 5000:5000 $(IMAGE)
