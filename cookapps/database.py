import aiomysql


DB = "cookapps_kungyu"


async def get_db_connection():
    return await aiomysql.connect(
        user="test",
        password="test",
        db=DB,
    )


async def setup_database():
    conn = await get_db_connection()
    async with conn.cursor() as cur:
        query = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTO_INCREMENT,
            username VARCHAR(64),
            password VARCHAR(255)
        );
        """
        await cur.execute(query)
        await conn.commit()
    conn.close()
