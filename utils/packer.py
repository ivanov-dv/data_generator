import io
import multivolumefile
import os
import py7zr
import zipfile

from config import logger, OUTPUT_DIR, INPUT_DIR
from utils.entities import IPacker


class PackerZip(IPacker):
    @staticmethod
    def create_from_buffer(buffer: io.BytesIO, archive_filename: str, inner_filename: str) -> None:
        """
        Создает архив из буфера и сохраняет в указанный файл.

        :param buffer: Объект буфера io.BytesIO.
        :param archive_filename: Имя файла архива с расширением.
        :param inner_filename: Имя вложенного файла с расширением.
        """
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.writestr(inner_filename, buffer.getvalue())
        zip_buffer.seek(0)
        with open(f'{OUTPUT_DIR}/{archive_filename}', 'wb') as f:
            f.write(zip_buffer.getvalue())

    @staticmethod
    def create_from_files(source_dir: str, target_files: list, archive_name: str, delete_after=False) -> None:
        """
        Создает архив из списка файлов и сохраняет в указанный файл.

        :param source_dir: Путь к папке, где находятся целевые файлы.
        :param target_files: Список путей к файлам.
        :param archive_name: Имя файла архива с расширением.
        :param delete_after: Флаг для удаления исходных файлов после упаковки.
        """

        with zipfile.ZipFile(f'{OUTPUT_DIR}/{archive_name}', 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for file_path in target_files:
                zip_file.write(f'{source_dir}/{file_path}', file_path)
                if delete_after:
                    os.remove(f'{source_dir}/{file_path}')


class Packer7z(IPacker):
    @staticmethod
    def _create_partition_from_buffer(buffer: io.BytesIO, archive_filename: str, inner_filename: str,
                                      max_size_mb: int) -> None:
        """
        Вспомогательный метод для 7z. Создает тома архива, не превышающие заданного размера.

        :param buffer: Объект буфера io.BytesIO.
        :param archive_filename: Имя файла архива с расширением.
        :param inner_filename: Имя вложенного файла с расширением.
        :param max_size_mb: Максимальный размер тома архива, в байтах.
        """

        with multivolumefile.open(
                f'{archive_filename}', mode='wb', volume=max_size_mb * 1024 * 1024
        ) as target_archive:
            with py7zr.SevenZipFile(target_archive, 'w') as archive:
                archive.writestr(buffer.getvalue(), inner_filename)

    @staticmethod
    def _create_partition_from_files(archive_filename: str, max_size_mb: int) -> None:
        """
        Вспомогательный метод для 7z. Создает тома архива, не превышающие заданного размера.

        :param archive_filename: Имя файла архива с расширением.
        :param max_size_mb: Максимальный размер тома архива, в байтах.
        """

        with multivolumefile.open(
                archive_filename, mode='wb', volume=int(max_size_mb * 1024 * 1024)
        ) as target_archive:
            with py7zr.SevenZipFile(target_archive, 'w') as archive:
                archive.writeall(INPUT_DIR, '')

    @staticmethod
    def create_from_buffer(buffer: io.BytesIO, archive_filename: str, inner_filename: str) -> None:
        """
        Создает архив из буфера и сохраняет в указанный файл.

        :param buffer: Объект буфера io.BytesIO.
        :param archive_filename: Имя файла архива с расширением.
        :param inner_filename: Имя вложенного файла с расширением.
        """

        with py7zr.SevenZipFile(file=f'{OUTPUT_DIR}/{archive_filename}', mode='w') as archive:
            archive.writestr(buffer.getvalue(), inner_filename)

    @staticmethod
    def create_from_files(source_dir: str, target_files: list, archive_name: str, delete_after=False) -> None:
        """
        Создает архив из списка файлов и сохраняет в указанный файл.

        :param source_dir: Путь к папке, где находятся целевые файлы.
        :param target_files: Список путей к файлам.
        :param archive_name: Имя файла архива с расширением.
        :param delete_after: Флаг для удаления исходных файлов после упаковки.
        """

        with py7zr.SevenZipFile(f'{OUTPUT_DIR}/{archive_name}', 'w') as archive:
            for file_path in target_files:
                archive.write(f'{source_dir}/{file_path}', file_path)
                if delete_after:
                    os.remove(f'{source_dir}/{file_path}')

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

        if isinstance(data, io.BytesIO):
            cls._create_partition_from_buffer(data, f'{path}/temp.7z', inner_filename, max_size_mb)
            files = [file for file in os.listdir(path) if file.startswith('temp.7z')]
            cls.create_from_files(path, files, archive_filename, delete_after=True)

        elif isinstance(data, list):
            cls._create_partition_from_files(f'{path}/temp.7z', max_size_mb)
            files = [file for file in os.listdir(path) if file.startswith('temp.7z')]
            print(files)
            cls.create_from_files(path, files, archive_filename, delete_after=True)

        else:
            logger.error('create_one_file_from_parts - аргумент data должен быть list или io.BytesIO')
            raise ValueError('Аргумент data должен быть list или io.BytesIO')
