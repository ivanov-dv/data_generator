import enum
import os
import time

from typing import Generator

from config import INPUT_DIR, OUTPUT_DIR, OUTPUT_FILENAME, logger
from utils.entities import IGenerator, IPacker, IFileCreator
from utils.models import FileFormat, PackerFormat, WorkFormat, PackerType


class Terminal:
    def __init__(self, person_generator: IGenerator, packer_zip: IPacker, packer_7z: IPacker,
                 file_creator: IFileCreator):
        self.person_generator = person_generator
        self.packer_zip = packer_zip
        self.packer_7z = packer_7z
        self.file_creator = file_creator
        self.config_data = {}

    @staticmethod
    def _check_input_range(value: str, enum_class: enum.Enum, start=None, end=None) -> bool:
        """
        Check input value in enum range.

        :param value: Input value.
        :param enum_class: Enum class.
        :param start: Start enum index for checking.
        :param end: End enum index for checking.
        :return: True, if value in enum range, False otherwise.
        """

        list_values = list(enum_class.__dict__['_value2member_map_'].keys())[start:end]
        if value not in list_values:
            print(
                f'\nНеверный ввод. Пожалуйста, введите число от '
                f'{min(list_values)} '
                f'до {max(list_values)}.'
            )
            return False
        return True

    @staticmethod
    def _show_choice_print(text: str, enum_class: enum.Enum, start: int = None, end: int = None) -> str:
        """
        Create text for output message and list of choices based on Enum class.

        :param text: Output text.
        :param enum_class: Enum class.
        :param start: Start enum index for showing choices.
        :param end: End enum index for showing choices.
        :return: Output text with choices list.
        """
        if hasattr(enum_class, 'field_name'):
            choice_list = [f'{text.value} - {text.field_name(text)}' for text in enum_class][start:end]
        else:
            choice_list = [f'{text.value} - {text.name}' for text in enum_class][start:end]
        return f'\n{text}\n' + '\n'.join(choice_list) + '\n> '

    def _create_file_without_packer(self, data: Generator | list) -> None:
        """
        Helper method for creating a file without a packer after receiving all user input parameters.

        :param data: Generator object or list. Random data.
        """
        file_format = self.config_data['file_format']
        if file_format == FileFormat.XLSX:
            self.file_creator.create_excel(data, file_name=f'{OUTPUT_FILENAME}.xlsx')
        elif file_format == FileFormat.CSV:
            self.file_creator.create_csv(data, file_name=f'{OUTPUT_FILENAME}.csv')
        elif file_format == FileFormat.TXT:
            self.file_creator.create_txt(data, file_name=f'{OUTPUT_FILENAME}.txt')

    def _create_zip_file(self, data: Generator | list) -> None:
        """
        Helper method for creating zip archive after receiving all user input parameters.

        :param data: Generator object or list. Random data.
        """
        file_format = self.config_data['file_format']
        if file_format == FileFormat.XLSX:
            buffer = self.file_creator.create_excel(data)
            self.packer_zip.create_from_buffer(buffer, archive_filename=f'{OUTPUT_FILENAME}.zip',
                                               inner_filename=f'{OUTPUT_FILENAME}.xlsx')
        elif file_format == FileFormat.CSV:
            buffer = self.file_creator.create_csv(data)
            self.packer_zip.create_from_buffer(buffer, archive_filename=f'{OUTPUT_FILENAME}.zip',
                                               inner_filename=f'{OUTPUT_FILENAME}.csv')
        elif file_format == FileFormat.TXT:
            buffer = self.file_creator.create_txt(data)
            self.packer_zip.create_from_buffer(buffer, archive_filename=f'{OUTPUT_FILENAME}.zip',
                                               inner_filename=f'{OUTPUT_FILENAME}.txt')

    def _create_7z_file(self, data: Generator | list) -> None:
        """
        Helper method for creating 7z archive after receiving all user input parameters.

        :param data: Generator object or list. Random data.
        """

        file_format = self.config_data['file_format']
        if file_format == FileFormat.XLSX:
            buffer = self.file_creator.create_excel(data)
            if self.config_data['packer_type'] == PackerType.ONE_FILE:
                self.packer_7z.create_from_buffer(buffer, archive_filename=f'{OUTPUT_FILENAME}.7z',
                                                  inner_filename=f'{OUTPUT_FILENAME}.xlsx')
            elif self.config_data['packer_type'] == PackerType.PART_FILES:
                self.packer_7z.create_one_file_from_parts(OUTPUT_DIR, buffer, f'{OUTPUT_FILENAME}.7z',
                                                          self.config_data['max_size_mb'], f'{OUTPUT_FILENAME}.xlsx')
        elif file_format == FileFormat.CSV:
            buffer = self.file_creator.create_csv(data)
            if self.config_data['packer_type'] == PackerType.ONE_FILE:
                self.packer_7z.create_from_buffer(buffer, archive_filename=f'{OUTPUT_FILENAME}.7z',
                                                  inner_filename=f'{OUTPUT_FILENAME}.csv')
            elif self.config_data['packer_type'] == PackerType.PART_FILES:
                self.packer_7z.create_one_file_from_parts(OUTPUT_DIR, buffer, f'{OUTPUT_FILENAME}.7z',
                                                          self.config_data['max_size_mb'], 'output.csv')
        elif file_format == FileFormat.TXT:
            buffer = self.file_creator.create_txt(data)
            if self.config_data['packer_type'] == PackerType.ONE_FILE:
                self.packer_7z.create_from_buffer(buffer, archive_filename=f'{OUTPUT_FILENAME}.7z',
                                                  inner_filename=f'{OUTPUT_FILENAME}.txt')
            elif self.config_data['packer_type'] == PackerType.PART_FILES:
                self.packer_7z.create_one_file_from_parts(OUTPUT_DIR, buffer, f'{OUTPUT_FILENAME}.7z',
                                                          self.config_data['max_size_mb'], 'output.txt')
        else:
            err = 'Неизвестный формат файла. Попробуйте заново'
            logger.error(f'_create_7z_file - {err}')
            print(err)
            self.start()

    @staticmethod
    def show_welcome_print() -> None:
        """
        Welcome message.
        """

        print(
            'Welcome to the Packer!\n'
            'Программа для генерации случайных данных пользователя.\n'
        )

    def get_work_format(self):
        """
        Get the program work format.
        """
        text = self._show_choice_print('Выберите, что хотите сделать:', WorkFormat)
        work_format = input(text).strip()
        if not self._check_input_range(work_format, WorkFormat):
            return self.get_work_format()
        self.config_data['work_format'] = WorkFormat(work_format)
        return WorkFormat(work_format)

    def get_number_of_lines(self) -> int:
        """
        Get number of lines for generating and writing to config_data.

        :return: Number of lines.
        """
        number_of_lines = input('\nВведите количество строк для генерации\n> ').strip()
        if not number_of_lines.isdigit() and 1 <= int(number_of_lines) <= 2000000:
            print('Неверный ввод. Пожалуйста, введите положительное целое число от 1 до 2_000_000 лишних символов.\n')
            self.get_number_of_lines()
        self.config_data['number_of_lines'] = int(number_of_lines)
        return int(number_of_lines)

    def get_data_file_format(self):
        """
        Get output file format and write to config_data.

        :return: Object FileFormat.
        """

        text = self._show_choice_print('Выберите формат файла:', FileFormat)
        file_format = input(text).strip()
        if not self._check_input_range(file_format, FileFormat):
            return self.get_data_file_format()
        self.config_data['file_format'] = FileFormat(file_format)
        return FileFormat(file_format)

    def get_packer_format(self) -> PackerFormat:
        """
        Get packer format and write to config_data.

        :return: Object PackerFormat.
        """

        work_format = self.config_data['work_format']
        if work_format == WorkFormat.PACKER:
            text = self._show_choice_print('Выберите формат архива:', PackerFormat, end=-1)
            packer_format = input(text).strip()
            if not self._check_input_range(packer_format, PackerFormat, end=-1):
                return self.get_packer_format()
        elif work_format == WorkFormat.GENERATOR:
            phrase = ('Выберите формат архива, если требуется архивация.\n'
                      'Формат 7z поддерживает разбивку по максимальному размеру тома:')
            text = self._show_choice_print(phrase, PackerFormat)
            packer_format = input(text).strip()
            if not self._check_input_range(packer_format, PackerFormat):
                return self.get_packer_format()
        else:
            logger.error(f'get_packer_format - Некорректный формат работы программы. Config_data - {self.config_data}')
            print('Некорректный формат работы программы.')
            return self.get_packer_format()
        self.config_data['packer_format'] = PackerFormat(packer_format)
        return PackerFormat(packer_format)

    def get_files_for_packer(self) -> list:
        """
        Get a list of files for packing from the "input" directory and write to config_data.

        :return: List of files in "input" directory.
        """

        input(f'\nПоместите файлы для архивации в папку "{INPUT_DIR}" и нажмите Enter')
        files = os.listdir(f'./{INPUT_DIR}')
        if not files:
            print(f'Не найдено ни одного файла в папке "{INPUT_DIR}".\n')
            return self.get_files_for_packer()
        for file in files:
            file_path = os.path.join(f'./{INPUT_DIR}', file)
            if os.path.isdir(file_path):
                logger.debug(f'get_files_for_packer - В папке "{INPUT_DIR}" обнаружен вложенный каталог "{file}".')
                print(f'В папке "{INPUT_DIR}" обнаружен вложенный каталог "{file}". Удалите его.')
                return self.get_files_for_packer()
        self.config_data['files_for_packer'] = files
        print('Перечисленные ниже файлы будут заархивированы:\n' + '\n'.join(files) + '\n')
        return files

    def get_packer_type(self) -> PackerType:
        """
        Get packer type and write to config data.

        :return: Object PackerType.
        """

        text = self._show_choice_print('Выберите тип архивации:', PackerType)
        packer_type = input(text).strip()
        if not self._check_input_range(packer_type, PackerType):
            return self.get_packer_type()
        self.config_data['packer_type'] = PackerType(packer_type)
        return PackerType(packer_type)

    def get_max_size_mb(self) -> float:
        """
        Get max size MB for packing (1-50) and write to config_data.

        :return: Max size MB for packing (1-50).
        """

        max_size_mb = input('\nВведите максимальный размер файла архива (в МБ)\n> ').strip()
        if not (max_size_mb.isdigit() and 1 <= int(max_size_mb) <= 50):
            logger.debug(f'get_max_size_mb - Неверный ввод. Значение - {max_size_mb}.')
            print('Неверный ввод. Пожалуйста, введите целое число от 1 до 50.\n')
            return self.get_max_size_mb()
        self.config_data['max_size_mb'] = int(max_size_mb)
        return int(max_size_mb)

    def get_generator_parameters(self) -> None:
        """
        Get generator parameters for generate random data.
        """

        self.get_number_of_lines()
        self.get_data_file_format()
        packer_format = self.get_packer_format()
        if packer_format == PackerFormat.FORMAT_7Z:
            if self.get_packer_type() == PackerType.PART_FILES:
                self.get_max_size_mb()

    def get_packer_parameters(self) -> None:
        """
        Get packer parameters for packing user files and write to config_data.
        """

        self.get_files_for_packer()
        packer_type = self.get_packer_type()
        if packer_type == PackerType.ONE_FILE:
            self.get_packer_format()
        elif packer_type == PackerType.PART_FILES:
            self.config_data['packer_format'] = PackerFormat.FORMAT_7Z
            self.get_max_size_mb()

    # 2 варианта генерации для сравнения скорости - генератор и списковые включения.
    # Генератор оказался чуть быстрее и занимает меньше оперативной памяти.
    def generate_data_to_generator(self) -> Generator:
        """
        Create object of generator random data.

        :return: Generator object.
        """

        try:
            return self.person_generator.generate_random_to_generator(self.config_data['number_of_lines'])
        except Exception as e:
            logger.error(f'generate_data_to_generator - {e}. Config_data - {self.config_data}')
            print('Ошибка при создании генератора случайных данных.')
            self.start()

    def generate_data_to_list(self) -> list:
        """
        Create list of random data.

        :return: List of random data.
        """
        try:
            return self.person_generator.generate_random_to_list(self.config_data['number_of_lines'])
        except Exception as e:
            logger.error(f'generate_data_to_list - {e}. Config_data - {self.config_data}')
            print('Ошибка при создании списка случайных данных.')
            self.start()

    def create_file(self, data: Generator | list) -> None:
        """
        Create file with random data and write to xlsx, csv or txt.

        :param data: Data (generator or list).
        """

        packer_format = self.config_data['packer_format']

        if packer_format == PackerFormat.NO_PACKER:
            self._create_file_without_packer(data)
        elif packer_format == PackerFormat.ZIP:
            self._create_zip_file(data)
        elif packer_format == PackerFormat.FORMAT_7Z:
            self._create_7z_file(data)
        else:
            err = 'Неизвестный способ архивирования. Попробуйте заново.'
            print(err)
            logger.error(f'create_file - {err} Config_data - {self.config_data}')
            self.start()
        print('Файл создан.')

    def package_files(self) -> None:
        """
        Package user files.
        """

        print('Создание архива')
        if self.config_data['packer_type'] == PackerType.ONE_FILE:
            if self.config_data['packer_format'] == PackerFormat.FORMAT_7Z:
                self.packer_7z.create_from_files(INPUT_DIR, self.config_data['files_for_packer'],
                                                 f'{OUTPUT_FILENAME}.7z')
            elif self.config_data['packer_format'] == PackerFormat.ZIP:
                self.packer_zip.create_from_files(INPUT_DIR, self.config_data['files_for_packer'],
                                                  f'{OUTPUT_FILENAME}.zip')
            else:
                err = 'Неизвестный способ архивирования. Попробуйте заново.'
                print(err)
                logger.error(f'package_files - {err} Config_data - {self.config_data}')
                self.start()
        if self.config_data['packer_type'] == PackerType.PART_FILES:
            self.packer_7z.create_one_file_from_parts(OUTPUT_DIR, self.config_data['files_for_packer'],
                                                      f'{OUTPUT_FILENAME}.7z', self.config_data['max_size_mb'])

    def start(self) -> None:
        """
        Start program with terminal interface.
        """
        try:
            work_format = self.get_work_format()
            if work_format == WorkFormat.GENERATOR:
                self.get_generator_parameters()
                st = time.time()
                data = self.generate_data_to_generator()
                self.create_file(data)
                print('Время выполнения', time.time() - st)
            elif work_format == WorkFormat.PACKER:
                self.get_packer_parameters()
                st = time.time()
                self.package_files()
                print('Время выполнения', time.time() - st)
            else:
                err = 'Некорректный формат работы программы.'
                print(err)
                logger.error(f'{err} Config_data - {self.config_data}')
                self.start()
        except Exception as e:
            logger.error(f'start - {e}. Config_data - {self.config_data}')
            print('В процессе выполнения программы возникла ошибка. Попробуйте заново.')
            self.start()
