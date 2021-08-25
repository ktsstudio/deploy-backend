from aiohttp import web


class Store:
    def __init__(self, app: web.Application):
        from server.store.pg import PgAccessor
        from server.store.gino import GinoAccessor

        self.pg = PgAccessor(app)
        self.gino = GinoAccessor(app)

        from server.apps.user.accessor import UserAccessor, SessionAccessor

        self.user = UserAccessor()
        self.session = SessionAccessor(app)

    def setup(
        self,
    ):
        self.pg.setup()
        self.gino.setup()
