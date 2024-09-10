import enum


def validate_input_data(value: str, enum_class: enum.Enum, start=None, end=None) -> bool:
    """Validate input data."""
    list_values = list(enum_class.__dict__['_value2member_map_'].keys())[start:end]
    return True if value in list_values else False
