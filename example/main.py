from fastapi import FastAPI
from mapproxy_.app import MapProxyApp

app = FastAPI(title="MapProxy Example Application")

map_proxy = MapProxyApp(prefix="/mapproxy")
map_proxy.mount_to(app)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5000)
