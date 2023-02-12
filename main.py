import sys
import fileinput
from errors.error import*
from tokenizing.token_scanning import *
from parser.parser import *
from evaluation.eval import *

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
        report_error(error)
        sys.exit()


def open_prompt():
    print("Welcome to the Dino Prompt : \n")
    error = DinoError()
    for line in fileinput.input():
        run(line, error)
        if error.triggered == True:
            report_error(error)
        error.triggered = False


def run(code: str, error: DinoError):
    scanned_code = Scanner(code, error)
    token_list = scanned_code.generate_tokens()
    # print(token_list)
    parser = Parser(token_list)
    expression = parser.parse()
    print(expression)
    # for expr in expression:
    print(evaluate(expression))


main()
