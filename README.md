# Проект по работе с БД и API hh.ru

## 📌 Описание проекта

Данный проект представляет собой консольное Python-приложение, которое получает данные о работодателях и их вакансиях с сайта hh.ru с использованием публичного API, сохраняет их в базу данных PostgreSQL и предоставляет интерфейс для работы с этими данными.

Проект реализован в рамках курсовой работы и демонстрирует навыки работы с:
- REST API
- PostgreSQL
- SQL-запросами (JOIN, AVG, LIKE)
- ООП и принципами SOLID

---

## 🛠 Стек технологий

- Python 3.10+
- PostgreSQL
- requests
- psycopg2
- python-dotenv

---

## 📁 Структура проекта

hh_project/
│
├── src/
│ ├── api/
│ │ └── hh_api.py
│ ├── database/
│ │ ├── db_creator.py
│ │ ├── data_loader.py
│ │ └── db_manager.py
│ ├── models/
│ │ └── vacancy.py
│ ├── utils/
│ │ └── config.py
│ └── main.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md


