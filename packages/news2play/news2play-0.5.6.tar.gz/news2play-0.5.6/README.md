# News To Play

## Index:
    0. python version >= 3.6
    1. How to setup dev environment
    2. How to use news2play package
    3. How to deploy

## How to setup dev/running environment

##### Command for init dev/running environment
```bash
make init
```

## How to use news2play package

##### Command for install news2play from PyPI
```bash
pip3 install news2play
```

##### Command for run news2play after installation.
```python
import news2play

news2play.app.run()
```

After the process finished, you can find the generated audios for news in ./storage/data

##### Command for run Docker from DockerHub
```bash
make docker_run
```
or:
```bash
docker run -it -p 5000:5000 deep3/news2play
```

## How to deploy

##### Command for deploy to PyPI
```bash
git tag [major].[monor].[patch] [none/commit id]
git push & git push --tags
make publish
```

##### Command for push to DockerHub, docker image will use news2play in PyPI
```bash
mkae docker_build
make docker_push
```
or:
```bash
docker build -t deep3/news2play:latest .
docker push deep3/news2play:latest
```

## Backup

```bash
echo hello news2play
```
```python
print('hello news2play')
```
```javascript
```