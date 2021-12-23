from sqlalchemy import Column, ForeignKey, Integer, MetaData, String, Table, create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = MetaData()
engine = create_engine("sqlite:///hardware.db")


hardware = Table(
    "hardware",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("hard_type", String(80), unique=False),
    Column("hard_name", String(120), unique=False),
    Column("hard_ip", String(120), unique=False),
    Column("hard_place", String(120), unique=False),
)


comments = Table(
    "comments",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("hardware_id", Integer, ForeignKey("hardware.id"), unique=True),
    Column("comment", String),
)

metadata.create_all(engine)
