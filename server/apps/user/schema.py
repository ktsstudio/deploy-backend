import datetime

from marshmallow_dataclass import dataclass

from server.web.schema import BaseSchema


@dataclass
class Session(BaseSchema):
    id: str
    username: str


@dataclass
class UserRegisterRequest(BaseSchema):
    username: str
    password: str


@dataclass
class UserResponse(BaseSchema):
    id: int
    username: str
    password: str


@dataclass
class TestResponse(BaseSchema):
    status: int
    body: str
