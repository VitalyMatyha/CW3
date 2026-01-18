from typing import Optional


class Vacancy:
    """Класс для представления вакансии."""

    def __init__(
        self,
        title: str,
        salary_from: Optional[int],
        salary_to: Optional[int],
        url: str
    ) -> None:
        self.title = title
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.url = url
