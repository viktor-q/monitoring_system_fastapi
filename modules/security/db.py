from sqlalchemy import Column, Integer, MetaData, String, Table, create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = MetaData()
engine = create_engine("sqlite:///users.db")


users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("login", String(80), unique=False),
    Column("hashed_pass", String(), unique=False),
)


metadata.create_all(engine)
