import psycopg2
from typing import List, Tuple

from src.utils.config import Config


class DBManager:
    """Класс для работы с данными в базе данных PostgreSQL."""

    def __init__(self) -> None:
        self.conn = psycopg2.connect(
            dbname=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            host=Config.DB_HOST,
            port=Config.DB_PORT
        )

    def get_companies_and_vacancies_count(self) -> List[Tuple[str, int]]:
        """
        Получает список всех компаний и количество вакансий у каждой компании.
        """
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT c.name, COUNT(v.vacancy_id)
                FROM companies c
                LEFT JOIN vacancies v ON c.company_id = v.company_id
                GROUP BY c.name
            """)
            return cur.fetchall()

    def get_all_vacancies(self) -> List[Tuple]:
        """
        Получает список всех вакансий с указанием компании, названия вакансии,
        зарплаты и ссылки.
        """
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT
                    c.name,
                    v.title,
                    v.salary_from,
                    v.salary_to,
                    v.url
                FROM vacancies v
                JOIN companies c ON v.company_id = c.company_id
            """)
            return cur.fetchall()

    def get_avg_salary(self) -> float:
        """
        Получает среднюю зарплату по всем вакансиям.
        """
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT AVG(
                    COALESCE(salary_from, salary_to)
                )
                FROM vacancies
            """)
            result = cur.fetchone()[0]
            return round(result, 2) if result else 0

    def get_vacancies_with_higher_salary(self) -> List[Tuple]:
        """
        Получает вакансии с зарплатой выше средней.
        """
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT
                    c.name,
                    v.title,
                    v.salary_from,
                    v.salary_to,
                    v.url
                FROM vacancies v
                JOIN companies c ON v.company_id = c.company_id
                WHERE COALESCE(v.salary_from, v.salary_to) >
                      (SELECT AVG(COALESCE(salary_from, salary_to)) FROM vacancies)
            """)
            return cur.fetchall()

    def get_vacancies_with_keyword(self, keyword: str) -> List[Tuple]:
        """
        Получает вакансии, в названии которых содержится ключевое слово.
        """
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT
                    c.name,
                    v.title,
                    v.salary_from,
                    v.salary_to,
                    v.url
                FROM vacancies v
                JOIN companies c ON v.company_id = c.company_id
                WHERE LOWER(v.title) LIKE %s
            """, (f"%{keyword.lower()}%",))
            return cur.fetchall()

    def close(self) -> None:
        """Закрывает соединение с БД."""
        self.conn.close()
