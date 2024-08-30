import enum


class FileFormat(enum.Enum):
    XLSX = '1'
    CSV = '2'
    TXT = '3'


class PackerFormat(enum.Enum):
    ZIP = '1'
    FORMAT_7Z = '2'
    NO_PACKER = '3'

    @classmethod
    def field_name(cls, value):
        field_names = {
            '1': 'zip',
            '2': '7z',
            '3': 'Архивация не требуется'
        }
        return field_names[value.value]


class PackerType(enum.Enum):
    ONE_FILE = '1'
    PART_FILES = '2'

    @classmethod
    def field_name(cls, value):
        field_names = {
            '1': 'Архивировать в один файл',
            '2': 'Указать максимальный размер архива. При превышении архив будет разбит на части (формат .7z).'
        }
        return field_names[value.value]


class WorkFormat(enum.Enum):
    GENERATOR = '1'
    PACKER = '2'

    @classmethod
    def field_name(cls, value):
        field_names = {
            '1': 'Сгенерировать случайные данные в файл или архив',
            '2': 'Заархивировать файл или файлы.'
        }
        return field_names[value.value]
