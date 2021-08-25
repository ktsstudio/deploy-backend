import logging
logging.getLogger().setLevel(logging.DEBUG)

from aiohttp import web

from settings import config
from server.web.app import create_app


if __name__ == "__main__":
    app = create_app()
    web.run_app(app, port=config["common"]["port"])
