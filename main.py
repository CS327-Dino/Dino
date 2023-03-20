import sys
import fileinput
import argparse
from errors.error import *
from tokenizing.token_scanning import *
from parser.parser import *
from evaluation.eval import *
from evaluation.resolve import *
from evaluation.typecheck import *
import time


def scan_file(file_name):
    f = open(file_name, "rb")
    start_time = time.time()
    data = f.read()
    error = DinoError()
    run(data.decode("utf-8"), error)
    if parsed_args.time:
        print("--- %s seconds ---" % (time.time() - start_time))

    # if (error.triggered):
    #     report_error(error)
    #     sys.exit()


def open_prompt():
    print("Welcome to the Dino Prompt : \n")
    error = DinoError()
    typeenv = Scope()
    while True:
        run(input(">>> "), error, typeenv, True)
        # if error.triggered == True:
        #     report_error(error)
        error.triggered = False


def run(code: str, error: DinoError, typeenv: Scope = Scope(), prompt: bool = False):
    scanned_code = Scanner(code, error)
    token_list = scanned_code.generate_tokens()
    parser = Parser(token_list, error)
    expression = parser.parse()

    if parsed_args.verbose:
        print("------------------Parsed Expr------------------")
        print(expression)

    if error.triggered:
        if parsed_args.verbose:
            print("-----------------------------------------------")
        return

    resolved = resolution(expression)
    if parsed_args.verbose:
        print("------------------Resolved Expr----------------")
        print(resolved)
        print("-----------------------------------------------")

    # typecheck(resolved, typeenv, error)
    # if error.triggered:
    #     return

    output = evaluate(resolved)
    if prompt:
        print(output)


args = argparse.ArgumentParser()
args.add_argument("file", nargs="?", help="file to run")
args.add_argument("-v", "--verbose", action="store_true", help="verbose mode")
args.add_argument("-t", "--time", action="store_true", help="time mode")
parsed_args = args.parse_args()
# print(parsed_args)

if parsed_args.file:
    scan_file(parsed_args.file)
else:
    open_prompt()
