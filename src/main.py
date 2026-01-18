import requests

response = requests.get("https://api.hh.ru/employers/1740")
print(response.status_code)

from src.api.hh_api import HeadHunterAPI

if __name__ == "__main__":
    api = HeadHunterAPI()
    employer = api.get_employer(1740)  # Яндекс
    print(employer["name"])

    vacancies = api.get_vacancies(1740)
    print(f"Найдено вакансий: {len(vacancies)}")

from src.database.db_creator import DBCreator


def main() -> None:
    """Точка входа в приложение."""
    db_creator = DBCreator()
    db_creator.create_database()
    db_creator.create_tables()
    print("База данных и таблицы успешно созданы.")


if __name__ == "__main__":
    main()
