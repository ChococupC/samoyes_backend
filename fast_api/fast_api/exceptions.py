class ModelException(Exception):
    def __init__(self, message=""):
        self.message = message
        super().__init__(self.message)


# 没找到
class NotFoundException(ModelException):
    def __init__(self, message="找不到该条数据"):
        self.message = message
        super().__init__(self.message)
