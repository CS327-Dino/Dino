import unittest
from evaluation.eval import *
from errors.error import *
from tokenizing.token_scanning import *


class TestTokenizer(unittest.TestCase):
    def test_tokenizer_single(self):

        t1 = Token(TokenType.DOT, ".", None, 1)
        t2 = Token(TokenType.PLUS, "+", None, 1)
        t3 = Token(TokenType.MINUS, "-", None, 1)
        t4 = Token(TokenType.SLASH, "/", None, 1)
        t5 = Token(TokenType.STAR, "*", None, 1)
        t6 = Token(TokenType.EOF, "", None, 2)

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

        for i in range(len(tlist)-1):
            self.assertEqual(tlist[i].ttype, token_list_manual[i].ttype)
            self.assertEqual(tlist[i].text, token_list_manual[i].text)
            self.assertEqual(tlist[i].literal, token_list_manual[i].literal)
            self.assertEqual(tlist[i].line, token_list_manual[i].line)

    def test_tokenizer_double(self):

        t1 = Token(TokenType.EQUAL_EQUAL, "==", None, 1)
        t2 = Token(TokenType.EQUAL, "=", None, 1)
        t3 = Token(TokenType.BANG_EQUAL, "!=", None, 1)
        t4 = Token(TokenType.LESS_EQUAL, "<=", None, 1)
        t5 = Token(TokenType.GREATER, ">", None, 1)
        t6 = Token(TokenType.EOF, "", None, 2)

        token_list_manual = []
        token_list_manual.append(t1)
        token_list_manual.append(t2)
        token_list_manual.append(t3)
        token_list_manual.append(t4)
        token_list_manual.append(t5)
        token_list_manual.append(t6)

        error = DinoError()
        scan = Scanner("=== != <=>", error)
        tlist = scan.generate_tokens()

        for i in range(len(tlist)-1):
            self.assertEqual(tlist[i].ttype, token_list_manual[i].ttype)
            self.assertEqual(tlist[i].text, token_list_manual[i].text)
            self.assertEqual(tlist[i].literal, token_list_manual[i].literal)
            self.assertEqual(tlist[i].line, token_list_manual[i].line)

    def test_tokenizer_strings(self):

        t1 = Token(TokenType.STRING, "Hello", "Hello", 1)
        t2 = Token(TokenType.STRING, "World", "World", 1)
        t3 = Token(TokenType.EOF, "", None, 2)

        token_list_manual = []
        token_list_manual.append(t1)
        token_list_manual.append(t2)
        token_list_manual.append(t3)

        error = DinoError()
        scan = Scanner(' "Hello" "World" ', error)
        tlist = scan.generate_tokens()

        for i in range(len(tlist)-1):
            self.assertEqual(tlist[i].ttype, token_list_manual[i].ttype)
            self.assertEqual(tlist[i].text, token_list_manual[i].text)
            self.assertEqual(tlist[i].literal,
                             token_list_manual[i].literal)
            self.assertEqual(tlist[i].line, token_list_manual[i].line)

    def test_tokenizer_numbers_identifiers(self):

        t1 = Token(TokenType.INTEGER, "420", 420, 1)
        t2 = Token(TokenType.IDENTIFIER, "Var_Name_Not_String", None, 1)
        t3 = Token(TokenType.STRING, "String_Not_Var_Name",
                   "String_Not_Var_Name", 1)
        t4 = Token(TokenType.EOF, "", None, 2)

        token_list_manual = []
        token_list_manual.append(t1)
        token_list_manual.append(t2)
        token_list_manual.append(t3)
        token_list_manual.append(t4)

        error = DinoError()
        scan = Scanner(
            ' 420 Var_Name_Not_String "String_Not_Var_Name" ', error)
        tlist = scan.generate_tokens()

        for i in range(len(tlist)-1):
            self.assertEqual(tlist[i].ttype, token_list_manual[i].ttype)
            self.assertEqual(tlist[i].text, token_list_manual[i].text)
            self.assertEqual(tlist[i].literal,
                             token_list_manual[i].literal)
            self.assertEqual(tlist[i].line, token_list_manual[i].line)

    def test_tokenizer_comments(self):

        t1 = Token(TokenType.INTEGER, "112", 112, 1)
        t2 = Token(TokenType.STAR, "*", None, 1)
        t3 = Token(TokenType.LEFT_PAREN, "(",
                   None, 1)
        t4 = Token(TokenType.EOF, "", None, 2)

        token_list_manual = []
        token_list_manual.append(t1)
        token_list_manual.append(t2)
        token_list_manual.append(t3)
        token_list_manual.append(t4)

        error = DinoError()
        scan = Scanner(
            ' 112 *( ?: Hello World :? ', error)
        tlist = scan.generate_tokens()

        for i in range(len(tlist)-1):
            self.assertEqual(tlist[i].ttype, token_list_manual[i].ttype)
            self.assertEqual(tlist[i].text, token_list_manual[i].text)
            self.assertEqual(tlist[i].literal,
                             token_list_manual[i].literal)
            self.assertEqual(tlist[i].line, token_list_manual[i].line)
