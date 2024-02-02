import typing as t


class UserValidationExeptionsOptions(t.TypedDict):
    user_not_found_text: str
    invalid_password_text: str