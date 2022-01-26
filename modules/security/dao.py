from security.db import engine, users
from sqlalchemy import select, update


class DAO:
    def create_user_in_db(self, login: str, hashed_pass: str) -> int:
        conn = engine.connect()
        with conn.begin():
            insert_query = users.insert().values(login=login, hashed_pass=hashed_pass)
            result = conn.execute(insert_query)
            new_user_id = result.inserted_primary_key[0]

        return new_user_id

    def extract_userdata_from_db(self, login: str) -> dict:
        conn = engine.connect()
        query = select(
            [
                users.c.id,
                users.c.login,
                users.c.hashed_pass,
            ]
        ).where(users.c.login == login)

        result = conn.execute(query).first()
        return dict(result)
