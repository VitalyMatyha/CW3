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

from src.database.data_loader import DataLoader

COMPANIES = {
    "Yandex": 1740,
    "Сбер": 3529,
    "VK": 1547,
    "Tinkoff": 786,
    "Ozon": 2180,
    "Wildberries": 870,
    "Avito": 845,
    "Ростелеком": 274,
    "Газпром": 393,
    "МТС": 377
}

def main() -> None:
    db_creator = DBCreator()
    db_creator.create_database()
    db_creator.create_tables()

    loader = DataLoader()
    loader.load_companies_and_vacancies(COMPANIES)

    print("Данные успешно загружены в БД.")

from src.database.db_manager import DBManager


def user_interface() -> None:
    """Функция взаимодействия с пользователем."""
    db = DBManager()

    while True:
        print(
            "\n1 — Показать компании и количество вакансий\n"
            "2 — Показать все вакансии\n"
            "3 — Показать среднюю зарплату\n"
            "4 — Показать вакансии с зарплатой выше средней\n"
            "5 — Найти вакансии по ключевому слову\n"
            "0 — Выход\n"
        )

        choice = input("Выберите действие: ")

        if choice == "1":
            for company, count in db.get_companies_and_vacancies_count():
                print(f"{company}: {count} вакансий")

        elif choice == "2":
            for row in db.get_all_vacancies():
                print(
                    f"{row[0]} | {row[1]} | "
                    f"ЗП: {row[2]}–{row[3]} | {row[4]}"
                )

        elif choice == "3":
            print(f"Средняя зарплата: {db.get_avg_salary()}")

        elif choice == "4":
            for row in db.get_vacancies_with_higher_salary():
                print(
                    f"{row[0]} | {row[1]} | "
                    f"ЗП: {row[2]}–{row[3]} | {row[4]}"
                )

        elif choice == "5":
            keyword = input("Введите ключевое слово: ")
            for row in db.get_vacancies_with_keyword(keyword):
                print(
                    f"{row[0]} | {row[1]} | "
                    f"ЗП: {row[2]}–{row[3]} | {row[4]}"
                )

        elif choice == "0":
            db.close()
            print("Выход из программы.")
            break

        else:
            print("Неверный ввод. Попробуйте снова.")

user_interface()

