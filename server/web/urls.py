from aiohttp import web


def setup_urls(app: web.Application):
    from server.apps.user.urls import setup_urls

    setup_urls(app)
