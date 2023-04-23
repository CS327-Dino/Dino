import sys
import fileinput
import argparse
from errors.error import *
from tokenizing.token_scanning import *
from parser.parser import *
from evaluation.eval import *
from evaluation.resolve import *
from evaluation.typecheck import *
from evaluation.bytecode import *
import time
sys.setrecursionlimit(10000)

bytecode = Bytecode()
bytecode = Bytecode()


def scan_file(file_name):
    f = open(file_name, "rb")
    start_time = time.time()
    data = f.read()
    error = DinoError()
    run(data.decode("utf-8"), error)
    if parsed_args.time:
        print("--- %s seconds ---" % (time.time() - start_time))

    if (error.triggered):
        report_error(error)
        # sys.exit()


def open_prompt():
    print("Welcome to the Dino Prompt : \n")
    error = DinoError()
    typeenv = Scope()
    env = Scope()
    while True:
        try:
            code = input(">>> ")
            if code == "abort();":
                print("Closing Prompt")
                break
            run(code, error, typeenv, True)
        except:
            print("Please Enter a valid expression")
        error.triggered = False


def run(code: str, error: DinoError, env: Scope = Scope() ,typeenv: Scope = Scope(), prompt: bool = False):
    try:
        scanned_code = Scanner(code, error)
        token_list = scanned_code.generate_tokens()
        parser = Parser(token_list, error)
        expression = parser.parse()
    except Exception as e:
        print(e)
        error.triggered = True

    if error.triggered:
        if parsed_args.verbose:
            print("-----------------------------------------------")
        return

    if parsed_args.verbose:
        print("------------------Parsed Expr------------------")
        print(expression)

    resolved = resolution(expression)

    if parsed_args.verbose:
        print("------------------Resolved Expr----------------")
        print(resolved)
        print("-----------------------------------------------")

    # typecheck(resolved, typeenv, error)
    # if error.triggered:
    #     return

    output = evaluate(resolved)
    # output = evaluate(resolved)

    # bytecode.bytecode_generator(resolved)
    # if parsed_args.bytecode:
    #     print("------------------Bytecode --------------------")
    #     for i,j in enumerate(bytecode.code):
    #         print(i, end="\t")
    #         print(j)

    #     print("-----------------------------------------------")
    # vm = VM(bytecode.code) 
    # output = vm.run() 

    if prompt:
        if output is not None:
            print(output)
        # print(output)


args = argparse.ArgumentParser()
args.add_argument("file", nargs="?", help="file to run")
args.add_argument("-v", "--verbose", action="store_true", help="verbose mode")
args.add_argument("-byt", "--bytecode", action="store_true",
                  help="Get Bytecode mode")
args.add_argument("-t", "--time", action="store_true", help="time mode")
parsed_args = args.parse_args()

if parsed_args.file:
    scan_file(parsed_args.file)
else:
    open_prompt()