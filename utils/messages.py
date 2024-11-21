import enum


def welcome() -> str:
    """Welcome message"""
    return (
        'Welcome to the Packer!\n'
        'Программа для генерации случайных данных пользователя.\n'
    )


def choice(
        message: str,
        enum_class: enum.Enum,
        start: int = None,
        end: int = None
) -> str:
    """
    Create a message with choice.

    :param message: The message to display.
    :param enum_class: The enum class.
    :param start: The start index of the choice in enum class.
    :param end: The end index of the choice in enum class.
    :return: Message with choice.
    """
    if hasattr(enum_class, 'field_name'):
        choice_list = (
            [f'{text.value} - {text.field_name(text)}'
             for text in enum_class][start:end]
        )
    else:
        choice_list = (
            [f'{text.value} - {text.name}'
             for text in enum_class][start:end]
        )
    return f'\n{message}\n' + '\n'.join(choice_list) + '\n> '


def incorrect_input(enum_class: enum.Enum, start=None, end=None) -> str:
    """Create message for incorrect input.

    :param enum_class: The enum class.
    :param start: The start index of the choice in enum class.
    :param end: The end index of the choice in enum class.
    :return: Message for incorrect input.
    """
    list_values = list(
        enum_class.__dict__['_value2member_map_'].keys()
    )[start:end]
    return (
        f'\nНеверный ввод. Пожалуйста, введите число от '
        f'{min(list_values)} '
        f'до {max(list_values)}.'
    )
