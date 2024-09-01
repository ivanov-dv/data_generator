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
        Create archive from buffer and save to the file.

        :param buffer: Object io.BytesIO.
        :param archive_filename: Archive file name with extension.
        :param inner_filename: Inner filename with extension.
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
        Create archive from filelist and save to the file.

        :param source_dir: Path to the target files.
        :param target_files: List of target files.
        :param archive_name: Archive file name with extension.
        :param delete_after: Flag for deleting source files after packaging.
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
        Helper method for 7z. Creates archive volumes from buffer.

        :param buffer: Object io.BytesIO.
        :param archive_filename: Archive file name with extension.
        :param inner_filename: Inner filename with extension.
        :param max_size_mb: Maximum volume size.
        """

        with multivolumefile.open(
                f'{archive_filename}', mode='wb', volume=max_size_mb * 1024 * 1024
        ) as target_archive:
            with py7zr.SevenZipFile(target_archive, 'w') as archive:
                archive.writestr(buffer.getvalue(), inner_filename)

    @staticmethod
    def _create_partition_from_files(archive_filename: str, max_size_mb: int) -> None:
        """
        Helper method for 7z. Creates archive volumes from files.

        :param archive_filename: Archive file name with extension.
        :param max_size_mb: Maximum volume size.
        """

        with multivolumefile.open(
                archive_filename, mode='wb', volume=int(max_size_mb * 1024 * 1024)
        ) as target_archive:
            with py7zr.SevenZipFile(target_archive, 'w') as archive:
                archive.writeall(INPUT_DIR, '')

    @staticmethod
    def create_from_buffer(buffer: io.BytesIO, archive_filename: str, inner_filename: str) -> None:
        """
        Create archive from buffer and save to file.

        :param buffer: Object io.BytesIO.
        :param archive_filename: Archive file name with extension.
        :param inner_filename: Inner filename with extension.
        """

        with py7zr.SevenZipFile(file=f'{OUTPUT_DIR}/{archive_filename}', mode='w') as archive:
            archive.writestr(buffer.getvalue(), inner_filename)

    @staticmethod
    def create_from_files(source_dir: str, target_files: list, archive_name: str, delete_after=False) -> None:
        """
        Create archive from filelist and save to the file.

        :param source_dir: Path to the target files.
        :param target_files: List of target files.
        :param archive_name: Archive file name with extension.
        :param delete_after: Flag for deleting source files after packaging.
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
        Creates multiple volumes if the archive exceeds the specified size.
        After which, it combines them into one archive.

        :param path: Path to the output files.
        :param data: Object io.BytesIO or list of files.
        :param archive_filename: Archive file name with extension.
        :param max_size_mb: Maximum volume size.
        :param inner_filename: Inner filename with extension, if it uses buffer.
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
