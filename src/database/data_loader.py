import psycopg2
from typing import Dict, List

from src.api.hh_api import HeadHunterAPI
from src.models.vacancy import Vacancy
from src.utils.config import Config


class DataLoader:
    """Класс для загрузки данных о компаниях и вакансиях в БД."""

    def __init__(self) -> None:
        self.api = HeadHunterAPI()

    def load_companies_and_vacancies(self, companies: Dict[str, int]) -> None:
        """
        Загружает компании и их вакансии в БД.

        :param companies: словарь {название компании: hh_id}
        """
        conn = psycopg2.connect(
            dbname=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            host=Config.DB_HOST,
            port=Config.DB_PORT
        )

        with conn.cursor() as cur:
            for company_name, hh_id in companies.items():
                # добавляем компанию
                cur.execute(
                    """
                    INSERT INTO companies (hh_id, name)
                    VALUES (%s, %s)
                    ON CONFLICT (hh_id) DO NOTHING
                    RETURNING company_id
                    """,
                    (hh_id, company_name)
                )

                result = cur.fetchone()

                if result:
                    company_id = result[0]
                else:
                    cur.execute(
                        "SELECT company_id FROM companies WHERE hh_id = %s",
                        (hh_id,)
                    )
                    company_id = cur.fetchone()[0]

                # получаем вакансии
                vacancies_data = self.api.get_vacancies(hh_id)

                for vacancy_data in vacancies_data:
                    salary_from, salary_to = self.api.parse_salary(
                        vacancy_data.get("salary")
                    )

                    vacancy = Vacancy(
                        title=vacancy_data.get("name"),
                        salary_from=salary_from,
                        salary_to=salary_to,
                        url=vacancy_data.get("alternate_url")
                    )

                    cur.execute(
                        """
                        INSERT INTO vacancies
                        (company_id, title, salary_from, salary_to, url)
                        VALUES (%s, %s, %s, %s, %s)
                        """,
                        (
                            company_id,
                            vacancy.title,
                            vacancy.salary_from,
                            vacancy.salary_to,
                            vacancy.url
                        )
                    )

            conn.commit()

        conn.close()
