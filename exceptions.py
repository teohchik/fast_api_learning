class ExpenseException(Exception):
    detail = "Unexpected error"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ObjectNotFoundException(ExpenseException):
    detail = "Object not found"

class IntegrityViolationException(ExpenseException):
    detail = "Integrity constraint violated"