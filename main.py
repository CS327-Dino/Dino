import sys
import fileinput
from errors.error import*


def main():
    # Here we will start our program
    if len(sys.argv) > 2:
        print("Hello")
    elif len(sys.argv) == 2:
        scan_file(sys.argv[1])
    else:
        open_prompt()


def scan_file(file_name):
    print(file_name)
    f = open(file_name, "rb")
    data = f.read()
    error = DinoError()
    run(data.decode("utf-8"), error)
    if(error.triggered):
        sys.exit()


def open_prompt():
    print("Welcome to the Dino Prompt : \n")
    error = DinoError()
    for line in fileinput.input():
        run(line, error)
        error.triggered = False


def run(code: str, error: DinoError):
    print(code)


main()
