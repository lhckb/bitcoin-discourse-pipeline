import psycopg2
from dotenv import load_dotenv
import os
from typing import Any
import polars as pl


load_dotenv()

class PGSQLConnector:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
        )
        self.uri = f"postgresql+psycopg2://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}"

    def select(self, query: str) -> list[tuple[Any, ...]]:
        cursor = self.conn.cursor()

        cursor.execute(query)

        rows = cursor.fetchall()

        cursor.close()

        return rows

    def insert(self, query: str, values: tuple):
        cursor = self.conn.cursor()

        cursor.execute(query, values)

        self.conn.commit()

        cursor.close()

    def insert_polars(self, dataframe: pl.DataFrame, table_name):
        dataframe.write_database(
            table_name=table_name,
            connection=self.uri,
            if_table_exists="append",
            engine="sqlalchemy"
        )
