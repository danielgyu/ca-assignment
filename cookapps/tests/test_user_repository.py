from aiomysql import Connection
import pytest
import pytest_asyncio

from cookapps.database import get_db_connection
from cookapps.models import User
from cookapps.user_repository import UserRepository
from cookapps.tests.conftest import count_table


pytestmark = pytest.mark.asyncio


@pytest.fixture
def user_repo():
    return UserRepository()


@pytest_asyncio.fixture
async def conn(
    populate_data: None,
):
    conn = await get_db_connection()
    yield conn
    conn.close()


async def test_is_unique_true(
    user_repo: UserRepository,
    conn: Connection,
):
    res = await user_repo.is_unique(conn, "lee")
    assert res is True


async def test_is_unique_false(
    user_repo: UserRepository,
    conn: Connection,
):
    res = await user_repo.is_unique(conn, "kim")
    assert res is False


async def test_save_user(user_repo: UserRepository, conn: Connection):
    before = await count_table(conn, "users")
    res = await user_repo.save_user(conn, "park", "satisfying-password")
    after = await count_table(conn, "users")
    assert res is True
    assert before + 1 == after


async def test_get_user_success(user_repo: UserRepository, conn: Connection):
    res = await user_repo.get_user(conn, "kim")
    assert isinstance(res, User) is True
    assert res.id == 1


async def test_get_user_none(user_repo: UserRepository, conn: Connection):
    res = await user_repo.get_user(conn, "Jin")
    assert res is None
