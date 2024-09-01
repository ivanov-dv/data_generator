import abc
import io

from typing import Generator


class IGenerator(abc.ABC):
    """
    Random data generator interface.
    """

    @classmethod
    def generate_random_row(cls) -> tuple:
        """
        Generates one line of generated random data.

        :return: One line of random data as a tuple.
        """
        pass

    @classmethod
    def generate_random_to_generator(cls, number_of_lines: int) -> Generator:
        """
        Generates random data in the size of the specified rows.


        :param number_of_lines: Number of lines
        :return: Object generator from tuples of random data.
        """
        pass

    @classmethod
    def generate_random_to_list(cls, number_of_lines: int) -> list:
        """
        Generates random data in the size of the specified rows.

        :param number_of_lines: Number of lines.
        :return: List of random rows.
        """
        pass


class IPacker(abc.ABC):
    """
    Data packer interface.
    """

    @staticmethod
    def create_from_buffer(buffer: io.BytesIO, archive_filename: str, inner_filename: str) -> None:
        """
        Create archive from buffer and save to the file.

        :param buffer: Object io.BytesIO.
        :param archive_filename: Archive file name with extension.
        :param inner_filename: Inner filename with extension.
        """
        pass

    @staticmethod
    def create_from_files(source_dir: str, target_files: list, archive_name: str, delete_after=False) -> None:
        """
        Create archive from filelist and save to the file.

        :param source_dir: Path to the target files.
        :param target_files: List of target files.
        :param archive_name: Archive file name with extension.
        :param delete_after: Flag for deleting source files after packaging.
        """
        pass

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
        pass


class IFileCreator(abc.ABC):
    """
    Interface for creating files.
    """

    @staticmethod
    def create_excel(data: list | Generator, file_name: str = None) -> io.BytesIO | None:
        """
        Create Excel file. Save to the file or buffer.

        :param data: Data (list or generator).
        :param file_name: Filename, If None, save to buffer.
        :return: None or io.BytesIO
        """
        pass

    @staticmethod
    def create_csv(data: list | Generator, file_name: str = None) -> io.BytesIO | None:
        """
        Create CSV file. Save to the file or buffer.

        :param data: Data (list or generator).
        :param file_name: Filename, If None, save to buffer.
        :return: None or io.BytesIO
        """
        pass

    @staticmethod
    def create_txt(data: list | Generator, file_name: str = None) -> io.BytesIO | None:
        """
        Create TXT file. Save to the file or buffer.

        :param data: Data (list or generator).
        :param file_name: Filename, If None, save to buffer.
        :return: None or io.BytesIO
        """
        pass
