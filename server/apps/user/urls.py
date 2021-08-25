from aiohttp import web

from server.apps.user.views import (
    UserRegisterView,
    UserLoginView,
    UserMeView,
    UserTestView,
)


def setup_urls(app: web.Application):
    app.router.add_view("/user.register", UserRegisterView)
    app.router.add_view("/user.login", UserLoginView)
    app.router.add_view("/user.me", UserMeView)
    app.router.add_view("/user.test", UserTestView)
