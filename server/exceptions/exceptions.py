class Unauthorized(Exception):
    def __str__(self):
        return "Unauthorized"


class OperationUnavailable(Exception):
    def __str__(self):
        return "Unavailable operation"


class UserRegister(Exception):
    def __str__(self):
        return "User already registered"
