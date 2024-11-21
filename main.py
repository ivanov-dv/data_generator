import os

from mimesis import Locale

from config import DIR_NAMES, OUTPUT_FILENAME
from utils.file_creator import ExcelFileCreator, CsvFileCreator, TxtFileCreator
from utils.generator import PersonGenerator
from utils.models import FileFormat, PackerFormat, WorkFormat, PackerType
from utils.packer import PackerZip, Packer7z
from utils.userdata import UserData

FILE_CREATOR_MAPPING = {
    FileFormat.XLSX: ExcelFileCreator,
    FileFormat.CSV: CsvFileCreator,
    FileFormat.TXT: TxtFileCreator
}
PACKER_MAPPING = {
    PackerFormat.ZIP: PackerZip,
    PackerFormat.FORMAT_7Z: Packer7z,
    PackerFormat.NO_PACKER: None
}
FILE_FORMAT_MAPPING = {
    FileFormat.XLSX: '.xlsx',
    FileFormat.CSV: '.csv',
    FileFormat.TXT: '.txt',
    None: ''
}


def main():
    for dir_name in DIR_NAMES:
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)

    person_generator = PersonGenerator(locale=Locale.RU)
    user_data = UserData()

    while True:
        user_data.welcome()

        user_data.get_work_format()
        if user_data.work_format == WorkFormat.GENERATOR:
            user_data.get_number_of_lines()
            user_data.get_data_file_format()
        elif user_data.work_format == WorkFormat.PACKER:
            user_data.get_files_for_packer()

        user_data.get_packer_format()

        user_data.get_packer_type()
        if user_data.packer_type == PackerType.PART_FILES:
            user_data.get_max_size()

        if user_data.work_format == WorkFormat.GENERATOR:
            data = person_generator.generate_random_to_generator(
                user_data.number_of_lines
            )
        else:
            data = user_data.files_for_packer

        data_file = FILE_CREATOR_MAPPING.get(user_data.data_file_format)

        if user_data.packer_format == PackerFormat.NO_PACKER:
            data_file(data, OUTPUT_FILENAME).create()
            return

        archive = PACKER_MAPPING.get(user_data.packer_format)
        inner_file_format = FILE_FORMAT_MAPPING.get(user_data.data_file_format)
        if user_data.packer_type == PackerType.PART_FILES:
            if user_data.work_format == WorkFormat.GENERATOR:
                data = data_file(data).create()
            archive(
                data=data,
                archive_filename=OUTPUT_FILENAME,
                max_size_mb=user_data.max_size_mb,
                inner_file_format=inner_file_format
            ).create_one_archive_from_parts(delete_after=True)
        else:
            if user_data.work_format == WorkFormat.GENERATOR:
                data_for_packer = data_file(data).create()
            else:
                data_for_packer = user_data.files_for_packer
            print(data_for_packer)
            archive(
                data_for_packer,
                OUTPUT_FILENAME,
                inner_file_format=inner_file_format
            ).create_archive()
        return


if __name__ == '__main__':
    main()
