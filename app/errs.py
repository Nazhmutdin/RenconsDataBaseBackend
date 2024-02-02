class InvalidPasswordError(Exception):
    def __init__(self, password: str, *args: object) -> None:
        self.password = password
        super().__init__(*args)


    def __str__(self) -> str:
        return f"Invalid password: {self.password}"


class UserNotFoundError(Exception):
    def __init__(self, login: str, *args: object) -> None:
        self.login = login
        super().__init__(*args)


    def __str__(self) -> str:
        return f"User with login {self.login} not found"
