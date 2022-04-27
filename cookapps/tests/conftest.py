from aiomysql import Connection
import bcrypt
import cookapps.database
from pytest import MonkeyPatch 
import pytest_asyncio

from cookapps.database import get_db_connection


@pytest_asyncio.fixture
async def populate_data(monkeypatch: MonkeyPatch):
    monkeypatch.setattr(
        cookapps.database, "DB", "cookapps_kungyu_test",
    )
    # separate test database
    pwd = "satisfying-password"
    hashed = bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()

    conn = await get_db_connection()
    async with conn.cursor() as cur:
        query = f"""
        DROP TABLE IF EXISTS users;

        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTO_INCREMENT,
            username VARCHAR(64),
            password VARCHAR(255)
        );

        INSERT INTO users (username, password)
        VALUES ( "kim", "{hashed}" );
        """
        await cur.execute(query)
        await conn.commit()
    yield
    conn.close()


async def count_table(
    conn: Connection,
    table_name: str,
) -> int:
    async with conn.cursor() as cur:
        query = f"""
        SELECT COUNT(*) FROM {table_name};
        """
        await cur.execute(query)
        res = await cur.fetchone()
        return res[0]
