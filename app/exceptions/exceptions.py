class UserInfoException(Exception):
    ...


class UserInfoNotFoundError(UserInfoException):
    def __init__(self):
        self.status_code = 404
        self.detail = "User don't found"


class UserInfoAlreadyExist(UserInfoException):
    def __init__(self):
        self.status_code = 404
        self.detail = "User already exist"
