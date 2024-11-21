import enum


class FileFormat(enum.Enum):
    """
    Enum class for file formats.
    Values are the user's choice in the terminal.
    """

    XLSX = '1'
    CSV = '2'
    TXT = '3'


class PackerFormat(enum.Enum):
    """
    Enum class for packer formats.
    Values are the user's choice in the terminal.
    """

    ZIP = '1'
    FORMAT_7Z = '2'
    NO_PACKER = '3'

    @classmethod
    def field_name(cls, value) -> str:
        """
        Create description for user input.
        :param value: User input.
        """
        field_names = {
            '1': 'zip',
            '2': '7z (поддерживает разбиение на части).',
            '3': 'Архивация не требуется'
        }
        return field_names[value.value]


class PackerType(enum.Enum):
    """
    Enum class for packer types.
    Values are the user's choice in the terminal.
    """

    ONE_FILE = '1'
    PART_FILES = '2'

    @classmethod
    def field_name(cls, value) -> str:
        """
        Create description for user input.
        :param value: User input.
        """
        field_names = {
            '1': 'Архивировать в один файл',
            '2': 'Указать максимальный размер архива.'
        }
        return field_names[value.value]


class WorkFormat(enum.Enum):
    """
    Enum class for work formats.
    Values are the user's choice in the terminal.
    """

    GENERATOR = '1'
    PACKER = '2'

    @classmethod
    def field_name(cls, value) -> str:
        """
        Create description for user input.
        :param value: User input.
        """
        field_names = {
            '1': 'Сгенерировать случайные данные в файл или архив',
            '2': 'Заархивировать файл или файлы.'
        }
        return field_names[value.value]
