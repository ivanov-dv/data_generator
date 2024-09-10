import abc
import io
import multivolumefile
import os
import py7zr
import zipfile

from config import logger, OUTPUT_DIR, INPUT_DIR, INNER_FILENAME


class IPacker(abc.ABC):
    """Packer interface."""

    def __init__(
            self,
            data: io.BytesIO | list,
            archive_filename: str,
            max_size_mb: int = None,
            inner_filename: str = INNER_FILENAME,
            inner_file_format: str = '',
            source_dir: str = INPUT_DIR,
            path_output_files: str = OUTPUT_DIR
    ):
        self.data = data
        self.archive_filename = archive_filename
        self.inner_filename = f"{inner_filename}{inner_file_format}"
        self.max_size_mb = max_size_mb
        self.source_dir = source_dir
        self.path_output_files = path_output_files

    @abc.abstractmethod
    def create_archive(self, delete_after=False) -> None:
        """
        Create archive from filelist or buffer and save to the file.
        :param delete_after: Flag for deleting source files after packaging.
        """

    def create_one_archive_from_parts(self, delete_after=False) -> None:
        """
        Creates multiple volumes if the archive exceeds the specified size.
        After which, it combines them into one archive.
        :param delete_after: Delete temp 7z files after packaging.
        """


class PackerZip(IPacker):
    def create_archive(self, delete_after=False) -> None:
        if isinstance(self.data, io.BytesIO):
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                zip_file.writestr(self.inner_filename, self.data.getvalue())
            zip_buffer.seek(0)
            with open(f'{OUTPUT_DIR}/{self.archive_filename}.zip', 'wb') as f:
                f.write(zip_buffer.getvalue())
        elif isinstance(self.data, list):
            with zipfile.ZipFile(f'{OUTPUT_DIR}/{self.archive_filename}.zip', 'w', zipfile.ZIP_DEFLATED) as zip_file:
                for file_path in self.data:
                    zip_file.write(f'{self.source_dir}/{file_path}', file_path)
                    if delete_after:
                        os.remove(f'{self.source_dir}/{file_path}')
        else:
            logger.error(f'{self.__class__.__qualname__} - аргумент data должен быть list или io.BytesIO')
            raise ValueError('Аргумент data должен быть list или io.BytesIO')

    def create_one_archive_from_parts(self, delete_after=False) -> None:
        """Method not available for zip archive"""
        logger.error(f'{self.__class__.__qualname__} - Method not available for zip archive')
        raise TypeError('Method not available for zip archive')


class Packer7z(IPacker):
    def _create_partition(
            self,
            partition_archive_filename: str,
            max_size_mb: int,
        ) -> None:
        """
        Helper method for 7z. Creates archive volumes from buffer.

        :partition_archive_filename: Filename for partition archive.
        :param max_size_mb: Maximum volume size.
        """
        with multivolumefile.open(
            f'{OUTPUT_DIR}/{partition_archive_filename}', mode='wb', volume=max_size_mb * 1024 * 1024
        ) as target_archive:
            with py7zr.SevenZipFile(target_archive, 'w') as archive:
                if isinstance(self.data, io.BytesIO):
                    archive.writestr(self.data.getvalue(), self.inner_filename)
                elif isinstance(self.data, list):
                    archive.writeall(INPUT_DIR, '')
                elif isinstance(self.data, str):
                    archive.write(self.data, '')
                else:
                    logger.error(f'{self.__class__.__qualname__} - Argument data must be list or io.BytesIO')
                    raise ValueError('Argument data must be list or io.BytesIO')

    def create_archive(self, delete_after=False) -> None:
        if isinstance(self.data, io.BytesIO):
            with py7zr.SevenZipFile(file=f'{OUTPUT_DIR}/{self.archive_filename}.7z', mode='w') as archive:
                archive.writestr(self.data.getvalue(), self.inner_filename)
        elif isinstance(self.data, list):
            with py7zr.SevenZipFile(f'{OUTPUT_DIR}/{self.archive_filename}.7z', 'w') as archive:
                for file_path in self.data:
                    archive.write(f'{self.source_dir}/{file_path}', file_path)
                    if delete_after:
                        os.remove(f'{self.source_dir}/{file_path}')
        else:
            logger.error(f'{self.__class__.__qualname__} - аргумент data должен быть list или io.BytesIO')
            raise ValueError('Аргумент data должен быть list или io.BytesIO')

    def create_one_archive_from_parts(self, delete_after=False) -> None:
        part_archive_filename = 'temp.7z'
        self._create_partition(part_archive_filename, self.max_size_mb)
        self.data = [file for file in os.listdir(self.path_output_files) if file.startswith(part_archive_filename)]
        self.source_dir = OUTPUT_DIR
        self.create_archive(delete_after=delete_after)
