# FastAPI wrapper for MapProxy

## How to install

```shell
TBD
```

## How to develop

### Getting started

There is a FastAPI demo application under the folder `example` that can be started to run
MapProxy with a sample configuration `example/mapproxy.yaml` provided in the `.env` file.

First of all, you have to install the package running

```shell
poetry install
```

Start the demo application with the following command:

```shell
uvicorn example.main:app --host 0.0.0.0 --port 5000 --reload
```

Open the browser at the following url [http://localhost:5000/mapproxy/demo](http://localhost:5000/mapproxy/demo) to find a MapProxy demo page.
