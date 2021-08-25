import datetime

import aiohttp
from aiohttp import web
from aiohttp_apispec import json_schema, response_schema

from server.apps.user.accessor import User
from server.apps.user.schema import UserRegisterRequest, UserResponse, TestResponse
from server.web.view import BaseView, require_auth


class UserRegisterView(BaseView):
    @json_schema(UserRegisterRequest.Schema)
    @response_schema(UserResponse.Schema)
    async def post(self):
        user_data = self.request["json"]
        return await self.store.user.register(user_data.username, user_data.password)


class UserLoginView(BaseView):
    @json_schema(UserRegisterRequest.Schema)
    @response_schema(UserResponse.Schema)
    async def post(self):
        user_data = self.request["json"]
        user = await self.store.user.login(user_data.username, user_data.password)
        session = await self.store.session.generate_session(user.username)
        response = web.json_response({"data": UserResponse.Schema().dump(user)})
        response.set_cookie("session_id", session.id)
        return response


class UserMeView(BaseView):
    @response_schema(UserResponse.Schema)
    @require_auth
    async def get(self):
        return await self.store.user.get_by_username(self.session.username)


class UserTestView(BaseView):
    @response_schema(TestResponse.Schema)
    async def get(self):
        async with aiohttp.ClientSession() as session:
            async with session.get("http://httpbin.org/get") as resp:
                status = resp.status
                body = await resp.text()
        return {"status": status, "body": body}
