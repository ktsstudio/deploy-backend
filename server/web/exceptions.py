class Error(Exception):
    status = 500
    code = "internal_error"
    description = "Internal Error"


class AlreadyExists(Error):
    status = 400
    code = "already_exists"
    description = "Already exists"


class InvalidCredentials(Error):
    status = 400
    code = "invalid_credentials"
    description = "Username or password mismatch"


class NotFound(Error):
    status = 404
    code = "not found"
    description = "Entity not found"


class NotAuthorized(Error):
    status = 401
    code = "not_authorized"
    description = "Not Authorized"
