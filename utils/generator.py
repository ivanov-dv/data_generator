import abc

from mimesis import Person, Locale
from typing import Generator


class IGenerator(abc.ABC):
    """
    Random data generator interface.
    """

    @abc.abstractmethod
    def generate_random_row(self) -> tuple:
        # raise NotImplementedError не использую, так как это реализовано в @abc.abstractmethod
        """
        Generates one line of generated random data.
        :return: One line of random data as a tuple.
        """

    @abc.abstractmethod
    def generate_random_to_generator(self, number_of_lines: int) -> Generator:
        """
        Generates random data in the size of the specified rows.
        :param number_of_lines: Number of lines
        :return: Object generator from tuples of random data.
        """

    @abc.abstractmethod
    def generate_random_to_list(self, number_of_lines: int) -> list:
        """
        Generates random data in the size of the specified rows.
        :param number_of_lines: Number of lines.
        :return: List of random rows.
        """


class PersonGenerator(IGenerator):

    def __init__(self, locale: Locale = Locale.RU):
        self.person = Person(locale=locale)

    def generate_random_row(self) -> tuple:
        return (
            self.person.first_name(),
            self.person.last_name(),
            self.person.gender(),
            self.person.weight(),
            self.person.username(),
            self.person.email(),
            self.person.password(),
            self.person.birthdate(),
            self.person.height(),
            self.person.nationality()
        )

    def generate_random_to_generator(self, number_of_lines: int) -> Generator:
        return (
            (
                self.person.first_name(),
                self.person.last_name(),
                self.person.gender(),
                self.person.weight(),
                self.person.username(),
                self.person.email(),
                self.person.password(),
                self.person.birthdate(),
                self.person.height(),
                self.person.nationality()
            )
            for _ in range(number_of_lines)
        )

    def generate_random_to_list(self, number_of_lines: int) -> list:
        # По-моему, так лаконичнее + list comprehension работает быстрее цикла for,
        # а строк генерировать нужно много.
        return [
            (
                self.person.first_name(),
                self.person.last_name(),
                self.person.gender(),
                self.person.weight(),
                self.person.username(),
                self.person.email(),
                self.person.password(),
                self.person.birthdate(),
                self.person.height(),
                self.person.nationality()
            )
            for _ in range(number_of_lines)
        ]
