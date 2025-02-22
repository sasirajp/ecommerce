
class OrderNotFoundException(Exception):
    def __init__(self, message="Order Not Found Exception"):
        self.message = message
        super().__init__(self.message)


class OrderCreationException(Exception):
    def __init__(self, message="Order Creation Failed"):
        self.message = message
        super().__init__(self.message)
