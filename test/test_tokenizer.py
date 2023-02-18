import unittest
from evaluation.eval import *
from errors.error import *
from tokenizing.token_scanning import *


class TestTokenizer(unittest.TestCase):
    def test_tokenizer(self):

        t1 = Token(TokenType.DOT, ".", None, 1)
        t2 = Token(TokenType.PLUS, "+", None, 1)
        t3 = Token(TokenType.MINUS, "-", None, 1)
        t4 = Token(TokenType.SLASH, "/", None, 1)
        t5 = Token(TokenType.STAR, "*", None, 1)
        t6 = Token(TokenType.STAR, "\n", None, 2)

        token_list_manual = []
        token_list_manual.append(t1)
        token_list_manual.append(t2)
        token_list_manual.append(t3)
        token_list_manual.append(t4)
        token_list_manual.append(t5)
        token_list_manual.append(t6)

        error = DinoError()
        scan = Scanner(". + -/ *", error)
        tlist = scan.generate_tokens()

        self.assertEqual(tlist, token_list_manual)
