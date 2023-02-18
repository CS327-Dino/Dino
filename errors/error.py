class DinoError:
    message: str
    line: int
    triggered: bool

    def __init__(self, message="", line=-1) -> None:
        self.message = message
        self.line = line
        self.triggered = False


def report_error(error: DinoError):
    print("Error on line", error.line, ":", error.message)
    error.triggered = True

def report_runtime_error(error: DinoError):
    print("Runtime Error on line", error.line, ":", error.message)
    exit()

