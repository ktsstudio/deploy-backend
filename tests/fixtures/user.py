import pytest


@pytest.fixture
async def user1(store):
    return await store.user.register('username', 'password')
