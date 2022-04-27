from aiomysql import Connection
from typing import Optional

from cookapps.models import User


class UserRepository:

    async def is_unique(
        self,
        conn: Connection,
        username: str
    ) -> bool:
        async with conn.cursor() as cur:
            query = f"""
            SELECT username 
            FROM users 
            WHERE username = "{username}";
            """
            await cur.execute(query)
            res = await cur.fetchone()
            
            return False if res else True

    async def save_user(
        self,
        conn: Connection,
        username: str,
        password: str
    ) -> bool:
        async with conn.cursor() as cur:
            query = f"""
            INSERT INTO users (username, password)
            VALUES ( "{username}", "{password}" );
            """
            await cur.execute(query)
            await conn.commit()
            return True 

    async def get_user(
        self,
        conn: Connection,
        username: str,
    ) -> Optional[User]:
        async with conn.cursor() as cur:
            query = f"""
            SELECT id, password
            FROM users
            WHERE username = "{username}";
            """
            await cur.execute(query)
            res = await cur.fetchone()
            if res:
                (user_id, password) = res
                return User(id=user_id, password=password)
            return None
