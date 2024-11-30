import logging

import mapproxy.config.loader
import mapproxy.config.spec
import mapproxy.config.validator
import mapproxy.wsgiapp
import pydantic
import yaml
from fastapi.middleware.wsgi import WSGIMiddleware

from .config import Settings

logger = logging.getLogger(__name__)


def create_mapproxy_app(settings: Settings) -> WSGIMiddleware:
    mapproxy_config = load_mapproxy_configuration(
        settings=settings, seed=False, ignore_warnings=settings.debug, renderd=False
    )
    services = mapproxy_config.configured_services()
    app = mapproxy.wsgiapp.MapProxyApp(services, mapproxy_config.base_config)
    if settings.debug:
        app = mapproxy.wsgiapp.wrap_wsgi_debug(app, mapproxy_config)
    app.config_files = None
    return WSGIMiddleware(app)


def build_mapproxy_config(settings: Settings) -> dict:
    """Build MapProxy configuration.

    Args:
        settings (Settings): whole settings for the wrapper

    Returns:
        dict: Dictionary of the MapProxy configuration
    """
    config_path = settings.mapproxy_config_path
    with config_path.open() as config_file:
        mapproxy_config = yaml.safe_load(config_file.read())

    return mapproxy_config


def load_mapproxy_configuration(
    settings: Settings, seed: bool, ignore_warnings: bool, renderd: bool
) -> mapproxy.config.loader.ProxyConfiguration:
    mapproxy.config.loader.load_plugins()

    conf_dict = build_mapproxy_config(settings=settings)
    errors, informal_only = mapproxy.config.spec.validate_options(conf_dict)
    for error in errors:
        logger.warning(error)
    if not informal_only or (errors and not ignore_warnings):
        raise mapproxy.config.loader.ConfigurationError("invalid configuration")

    errors = mapproxy.config.validator.validate(conf_dict)
    for error in errors:
        logger.warning(error)

    return mapproxy.config.loader.ProxyConfiguration(
        conf_dict, seed=seed, renderd=renderd
    )


try:
    mapproxy_settings = Settings()
except pydantic.ValidationError:
    logger.error("MapProxy configuration file doesn't exist!")
    raise


mapproxy_app = create_mapproxy_app(settings=mapproxy_settings)
