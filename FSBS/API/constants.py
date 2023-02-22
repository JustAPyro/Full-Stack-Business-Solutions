
class PermissionKind():
    def __new__(cls, value, *args):
            obj = int.__new__(cls, value)
            obj._value_ = value
            obj._pretty, = args
            return obj

    BUSINESS_CREATE = 1
    BUSINESS_VIEW = 2
    BUSINESS_DELETE = 3
    BUSINESS_EDIT = 4