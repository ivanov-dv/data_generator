import os

import utils.messages as msg
import utils.validator as validator

from config import logger, INPUT_DIR
from utils.models import WorkFormat, FileFormat, PackerFormat, PackerType


class UserData:

    def __init__(
            self,
            work_format: WorkFormat = None,
            number_of_lines: int = None,
            data_file_format: FileFormat = None,
            files_for_packer: list = None,
            packer_format: PackerFormat = None,
            packer_type: PackerType = None,
            max_size_mb: int = None
    ):
        self.work_format = work_format
        self.number_of_lines = number_of_lines
        self.data_file_format = data_file_format
        self.files_for_packer = files_for_packer
        self.packer_format = packer_format
        self.packer_type = packer_type
        self.max_size_mb = max_size_mb

    def _get_packer_format_for_generator(self):
        """Helper method to getting the packer format for generator"""
        while True:
            text = ('Выберите формат архива, если требуется архивация.\n'
                    'Формат 7z поддерживает разбивку по максимальному размеру тома:')
            packer_format = input(msg.choice(text, PackerFormat)).strip()
            if not validator.validate_input_data(packer_format, PackerFormat):
                print(msg.incorrect_input(PackerFormat))
            self.packer_format = PackerFormat(packer_format)
            return

    def _get_packer_format_for_packer(self):
        """Helper method to get the packer format for packer"""
        while True:
            text = 'Выберите формат архива:'
            packer_format = input(msg.choice(text, PackerFormat, end=-1)).strip()
            if not validator.validate_input_data(packer_format, PackerFormat):
                print(msg.incorrect_input(PackerFormat, end=-1))
            self.packer_format = PackerFormat(packer_format)
            return

    def _check_input_dir(self):
        """Helper method to check the input dir"""
        while True:
            input(f'\nПоместите файлы для архивации в папку "{INPUT_DIR}" и нажмите Enter.')
            files = os.listdir(f'./{INPUT_DIR}')
            if not files:
                print(f'Не найдено ни одного файла в папке "{INPUT_DIR}".\n')
            else:
                self.files_for_packer = files
                return

    @staticmethod
    def welcome():
        """Welcome message"""
        print(
            'Welcome to the Packer!\n'
            'Программа для генерации случайных данных пользователя.\n'
        )

    def get_work_format(self):
        """Get the work format"""
        while True:
            work_format = input(msg.choice('Выберите, что хотите сделать:', WorkFormat)).strip()
            if not validator.validate_input_data(work_format, WorkFormat):
                print(msg.incorrect_input(WorkFormat))
            else:
                self.work_format = WorkFormat(work_format)
                return

    def get_number_of_lines(self):
        """Get the number of lines for generator"""
        while True:
            number_of_lines = input('\nВведите количество строк для генерации\n> ').strip()
            if not (number_of_lines.isdigit() and 1 <= int(number_of_lines) <= 2000000):
                print('Неверный ввод. Введите положительное целое число от 1 до 2_000_000 лишних символов.\n')
            else:
                self.number_of_lines = int(number_of_lines)
                return

    def get_data_file_format(self):
        """Get the data file format"""
        while True:
            data_file_format = input(msg.choice('Выберите формат файла:', FileFormat)).strip()
            if not validator.validate_input_data(data_file_format, FileFormat):
                print(msg.incorrect_input(FileFormat))
            else:
                self.data_file_format = FileFormat(data_file_format)
                return

    def get_packer_format(self):
        """Get the packer format"""
        mapping = {
            WorkFormat.GENERATOR: self._get_packer_format_for_generator,
            WorkFormat.PACKER: self._get_packer_format_for_packer,
        }
        action = mapping.get(self.work_format)
        if not action:
            logger.error(
                f'get_packer_format - Некорректный формат работы программы. Config_data - {self.__dict__}')
            print('Некорректный формат работы программы.')
        action()

    def get_files_for_packer(self):
        """Get list of files for packer"""
        while True:
            self._check_input_dir()
            for file in self.files_for_packer:
                file_path = os.path.join(f'./{INPUT_DIR}', file)
                if os.path.isdir(file_path):
                    logger.debug(f'get_files_for_packer - В папке "{INPUT_DIR}" '
                                 f'обнаружен вложенный каталог "{file}".')
                    print(f'В папке "{INPUT_DIR}" обнаружен вложенный каталог "{file}". Удалите его.')
                else:
                    print(f'Перечисленные ниже файлы будут заархивированы:\n {'\n'.join(self.files_for_packer)}\n')
                    return

    def get_packer_type(self):
        """Get the packer type"""
        while True:
            if self.packer_format == PackerFormat.NO_PACKER or self.packer_format == PackerFormat.ZIP:
                return

            text = 'Выберите тип архивации:'
            packer_type = input(msg.choice(text, PackerType)).strip()
            if not validator.validate_input_data(packer_type, PackerType):
                print(msg.incorrect_input(PackerType))
            else:
                self.packer_type = PackerType(packer_type)
                return

    def get_max_size(self):
        """Get the max file size in MB"""
        while True:
            max_size_mb = input('\nВведите максимальный размер файла архива (в МБ)\n> ').strip()
            if not (max_size_mb.isdigit() and 1 <= int(max_size_mb) <= 50):
                logger.debug(f'get_max_size_mb - Неверный ввод. Значение - {max_size_mb}.')
                print('Неверный ввод. Пожалуйста, введите целое число от 1 до 50.\n')
            else:
                self.max_size_mb = int(max_size_mb)
                return
