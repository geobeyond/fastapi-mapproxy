from typing import Optional

from fastapi import FastAPI


class MapProxyApp:
    def __init__(
        self, prefix: str = "/mapproxy", title: str = "Mapproxy API Application"
    ):
        self.app = FastAPI(title=title)
        self.prefix = prefix
        self._setup_routes()

    def _setup_routes(self):
        """Add additional routes"""

        @self.app.get(f"{self.prefix}/status")
        async def status():
            return {"status": "operational"}

    def get_app(self) -> FastAPI:
        """Return a FastAPI application

        Returns:
            FastAPI: the application
        """
        return self.app

    def mount_to(self, parent_app: FastAPI, prefix: Optional[str] = None):
        """Mount this application into another FastAPI application."""
        from mapproxy_.app import mapproxy_app

        mount_prefix = prefix or self.prefix
        parent_app.mount(mount_prefix, mapproxy_app)


app = FastAPI(title="MapProxy Example Application")

map_proxy = MapProxyApp(prefix="/mapproxy")
map_proxy.mount_to(app)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5000)
