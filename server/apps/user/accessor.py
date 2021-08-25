import uuid
from hashlib import md5
from typing import Optional

from server.apps.user.models import User
from server.apps.user.schema import Session
from server.store.accessor import Accessor
from server.web.exceptions import AlreadyExists, InvalidCredentials, NotFound


class UserAccessor:
    async def register(self, username: str, password: str) -> User:
        user = await User.query.where(User.username == username).gino.first()
        if user is not None:
            raise AlreadyExists
        password = md5(password.encode()).hexdigest()
        return await User.create(username=username, password=password)

    async def login(self, username: str, password: str) -> User:
        user = await User.query.where(User.username == username).gino.first()
        if not user:
            raise InvalidCredentials
        if user.password != md5(password.encode()).hexdigest():
            raise InvalidCredentials
        return user

    async def get_by_username(self, username: str) -> User:
        user = await User.query.where(User.username == username).gino.first()
        if user is None:
            raise NotFound
        return user


class SessionAccessor(Accessor):
    async def generate_session(self, username: str) -> Session:
        session_id = uuid.uuid4().hex
        row = await self.store.pg.conn.fetchrow("""
            INSERT INTO session VALUES ($1, $2) RETURNING *
        """, session_id, username)
        return Session(**dict(row))

    async def get_by_id(self, session_id) -> Optional[Session]:
        row = await self.store.pg.conn.fetchrow("""
            SELECT * FROM session WHERE id = $1
        """, session_id)
        if row:
            return Session(**dict(row))
