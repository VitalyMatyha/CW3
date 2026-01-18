from typing import List, Dict, Optional
import requests


class HeadHunterAPI:
    """Класс для работы с API hh.ru."""

    BASE_URL = "https://api.hh.ru"

    def get_employer(self, employer_id: int) -> Dict:
        """
        Получает данные о работодателе по его id.

        :param employer_id: ID работодателя в hh.ru
        :return: словарь с данными работодателя
        """
        url = f"{self.BASE_URL}/employers/{employer_id}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def get_vacancies(self, employer_id: int) -> List[Dict]:
        """
        Получает список вакансий работодателя.

        :param employer_id: ID работодателя в hh.ru
        :return: список вакансий
        """
        vacancies = []
        page = 0

        while True:
            params = {
                "employer_id": employer_id,
                "page": page,
                "per_page": 100
            }
            response = requests.get(f"{self.BASE_URL}/vacancies", params=params)
            response.raise_for_status()
            data = response.json()

            vacancies.extend(data.get("items", []))

            if page >= data.get("pages", 0) - 1:
                break

            page += 1

        return vacancies

    @staticmethod
    def parse_salary(salary: Optional[Dict]) -> tuple[Optional[int], Optional[int]]:
        """
        Обрабатывает данные о зарплате.

        :param salary: словарь salary из API hh.ru
        :return: кортеж (salary_from, salary_to)
        """
        if not salary:
            return None, None

        return salary.get("from"), salary.get("to")
