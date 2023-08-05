class InvalidArgumentsError(Exception):
    def __init__(self, message: str):
        self.message = f"invalid arguments for Docker client: {message}"
