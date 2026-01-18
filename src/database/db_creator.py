import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from src.utils.config import Config


class DBCreator:
    """Класс для создания базы данных и таблиц PostgreSQL."""

    def __init__(self) -> None:
        self.db_name = Config.DB_NAME
        self.user = Config.DB_USER
        self.password = Config.DB_PASSWORD
        self.host = Config.DB_HOST
        self.port = Config.DB_PORT

    def create_database(self) -> None:
        """
        Создаёт базу данных, если она не существует.
        """
        conn = psycopg2.connect(
            dbname="postgres",
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        with conn.cursor() as cur:
            cur.execute(
                f"SELECT 1 FROM pg_database WHERE datname = '{self.db_name}'"
            )
            exists = cur.fetchone()

            if not exists:
                cur.execute(f"CREATE DATABASE {self.db_name}")

        conn.close()

    def create_tables(self) -> None:
        """
        Создаёт таблицы companies и vacancies.
        """
        conn = psycopg2.connect(
            dbname=self.db_name,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )

        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS companies (
                    company_id SERIAL PRIMARY KEY,
                    hh_id INT UNIQUE NOT NULL,
                    name VARCHAR(255) NOT NULL
                );
            """)

            cur.execute("""
                CREATE TABLE IF NOT EXISTS vacancies (
                    vacancy_id SERIAL PRIMARY KEY,
                    company_id INT REFERENCES companies(company_id),
                    title VARCHAR(255) NOT NULL,
                    salary_from INT,
                    salary_to INT,
                    url TEXT
                );
            """)

            conn.commit()

        conn.close()
