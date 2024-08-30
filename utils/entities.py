import abc
import io

from typing import Generator


class IGenerator(abc.ABC):
    """
    Интерфейс генератора случайных данных.
    """

    @classmethod
    def generate_random_row(cls) -> tuple:
        """
        Генерирует одну строчку сгенерированных случайных данных.

        :return: Одна строка из случайных данных в виде кортежа.
        """
        pass

    @classmethod
    def generate_random_to_generator(cls, number_of_lines: int) -> Generator:
        """
        Генерирует случайные данные в размере указанных строк.

        :param number_of_lines: Количество строк.
        :return: Объект генератора из множества строк(кортежей) случайных данных.
        """
        pass

    @classmethod
    def generate_random_to_list(cls, number_of_lines: int) -> list:
        """
        Генерирует случайные данные в размере указанных строк.

        :param number_of_lines: Количество строк.
        :return: Список из множества строк(кортежей) случайных данных.
        """
        pass


class IPacker(abc.ABC):
    """
    Интерфейс упаковщика данных.
    """

    @staticmethod
    def create_from_buffer(buffer: io.BytesIO, archive_filename: str, inner_filename: str) -> None:
        """
        Создает архив из буфера и сохраняет в указанный файл.

        :param buffer: Объект буфера io.BytesIO.
        :param archive_filename: Имя файла архива с расширением.
        :param inner_filename: Имя вложенного файла с расширением.
        """
        pass

    @staticmethod
    def create_from_files(source_dir: str, target_files: list, archive_name: str, delete_after=False) -> None:
        """
        Создает архив из списка файлов и сохраняет в указанный файл.

        :param source_dir: Путь к папке, где находятся целевые файлы.
        :param target_files: Список путей к файлам.
        :param archive_name: Имя файла архива с расширением.
        :param delete_after: Флаг для удаления исходных файлов после упаковки.
        """
        pass

    @classmethod
    def create_one_file_from_parts(cls, path: str, data: io.BytesIO | list, archive_filename: str,
                                   max_size_mb: int, inner_filename: str | None = None) -> None:
        """
        Создает несколько томов, если архив превышает указанный размер.
        После чего, объединяет их в один архив.

        :param path: Путь к папке, где находятся выходные файлы.
        :param data: Объект буфера io.BytesIO или список файлов для архивации.
        :param archive_filename: Имя файла архива с расширением.
        :param max_size_mb: Максимальный размер тома архива, в байтах.
        :param inner_filename: Имя вложенного сгенерированного файла с расширением при использовании буфера.
        """
        pass


class IFileCreator(abc.ABC):
    """
    Интерфейс для создания файлов.
    """

    @staticmethod
    def create_excel(data: list | Generator, file_name: str = None) -> io.BytesIO | None:
        """
        Создает Excel файл и сохраняет в файл или буфер.

        :param data: Данные
        :param file_name: Имя файла. Если None, то сохранение в буфер.
        :return:
        """
        pass

    @staticmethod
    def create_csv(data: list | Generator, file_name: str = None) -> io.BytesIO | None:
        """
        Создает CSV файл и сохраняет в файл или буфер.

        :param data: Данные
        :param file_name: Имя файла. Если None, то сохранение в буфер.
        :return:
        """
        pass

    @staticmethod
    def create_txt(data: list | Generator, file_name: str = None) -> io.BytesIO | None:
        """
        Создает TXT файл и сохраняет в файл или буфер.

        :param data: Данные
        :param file_name: Имя файла. Если None, то сохранение в буфер.
        :return:
        """
        pass
