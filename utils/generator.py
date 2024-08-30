from mimesis import Person, Locale
from typing import Generator

from utils.entities import IGenerator


class PersonGenerator(IGenerator):
    person = Person(locale=Locale.RU)

    @classmethod
    def generate_random_row(cls) -> tuple:
        """
        Генерирует одну строчку сгенерированных случайных данных.

        :return: Одна строка из случайных данных в виде кортежа.
        """

        return (
            cls.person.first_name(),
            cls.person.last_name(),
            cls.person.gender(),
            cls.person.weight(),
            cls.person.username(),
            cls.person.email(),
            cls.person.password(),
            cls.person.birthdate(),
            cls.person.height(),
            cls.person.nationality()
        )
    # Обоснуй за классметод -иначе не принимается
    @classmethod
    def generate_random_to_generator(cls, number_of_lines: int) -> Generator:
        """
        Генерирует случайные данные в размере указанных строк.

        :param number_of_lines: Количество строк.
        :return: Объект генератора из множества строк(кортежей) случайных данных.
        """

        result = (
            (
                cls.person.first_name(),
                cls.person.last_name(),
                cls.person.gender(),
                cls.person.weight(),
                cls.person.username(),
                cls.person.email(),
                cls.person.password(),
                cls.person.birthdate(),
                cls.person.height(),
                cls.person.nationality()
            )
            for _ in range(number_of_lines)
        )
        return result

    @classmethod
    def generate_random_to_list(cls, number_of_lines: int) -> list:
        """
        Генерирует случайные данные в размере указанных строк.

        :param number_of_lines: Количество строк.
        :return: Список из множества строк(кортежей) случайных данных.
        """
        # Извращенец - зачем внутри функции  однострочник - тебе строк жалко?
        result = [
            (
                cls.person.first_name(),
                cls.person.last_name(),
                cls.person.gender(),
                cls.person.weight(),
                cls.person.username(),
                cls.person.email(),
                cls.person.password(),
                cls.person.birthdate(),
                cls.person.height(),
                cls.person.nationality()
            )
            for _ in range(number_of_lines)
        ]
        # А чего тут не сэкономил?
        return result
