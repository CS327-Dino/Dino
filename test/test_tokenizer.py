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

    def test_tokenizer_functions(self):

        '''func sum(a , b) echo(a+b); end'''

        t1 = Token(TokenType.FUNC, "func", None, 1)
        t2 = Token(TokenType.IDENTIFIER, "sum", None, 1)
        t3 = Token(TokenType.LEFT_PAREN, "(", None, 1)
        t4 = Token(TokenType.IDENTIFIER, "a", None, 1)
        t5 = Token(TokenType.COMMA, ",", None, 1)
        t6 = Token(TokenType.IDENTIFIER, "b", None, 1)
        t7 = Token(TokenType.RIGHT_PAREN, ")", None, 1)
        t8 = Token(TokenType.ECHO, "echo", None, 1)
        t9 = Token(TokenType.LEFT_PAREN, "(", None, 1)
        t10 = Token(TokenType.IDENTIFIER, "a", None, 1)
        t11 = Token(TokenType.PLUS, "+", None, 1)
        t12 = Token(TokenType.IDENTIFIER, "b", None, 1)
        t13 = Token(TokenType.RIGHT_PAREN, ")", None, 1)
        t14 = Token(TokenType.SEMICOLON, ";", None, 1)
        t15 = Token(TokenType.END, "end", None,1)
        t16 = Token(TokenType.EOF, "", None, 2)
        
        token_list_manual = []
        token_list_manual.append(t1)
        token_list_manual.append(t2)
        token_list_manual.append(t3)
        token_list_manual.append(t4)
        token_list_manual.append(t5)
        token_list_manual.append(t6)
        token_list_manual.append(t7)
        token_list_manual.append(t8)
        token_list_manual.append(t9)
        token_list_manual.append(t10)
        token_list_manual.append(t11)
        token_list_manual.append(t12)
        token_list_manual.append(t13)
        token_list_manual.append(t14)
        token_list_manual.append(t15)
        token_list_manual.append(t16)

        error = DinoError()
        scan = Scanner(
            ' func sum(a , b) echo(a+b); end ', error)
        tlist = scan.generate_tokens()

        for i in range(len(tlist)-1):
            self.assertEqual(tlist[i].ttype, token_list_manual[i].ttype)
            self.assertEqual(tlist[i].text, token_list_manual[i].text)
            self.assertEqual(tlist[i].literal,
                             token_list_manual[i].literal)
            self.assertEqual(tlist[i].line, token_list_manual[i].line)

    def test_tokenizer_if(self):

        t1 = Token(TokenType.IF, "if", None, 1)
        t2 = Token(TokenType.LEFT_PAREN, "(", None, 1)
        t3 = Token(TokenType.IDENTIFIER, "a", None, 1)
        t4 = Token(TokenType.GREATER, ">", None, 1)
        t5 = Token(TokenType.IDENTIFIER, "b", None, 1)
        t6 = Token(TokenType.RIGHT_PAREN, ")", None, 1)
        t7 = Token(TokenType.ECHO, "echo", None, 1)
        t8 = Token(TokenType.LEFT_PAREN, "(", None, 1)
        t9 = Token(TokenType.IDENTIFIER, "a", None, 1)
        t10 = Token(TokenType.RIGHT_PAREN, ")", None, 1)
        t11 = Token(TokenType.SEMICOLON, ";", None, 1)
        t12 = Token(TokenType.END, "end", None, 1)
        t13 = Token(TokenType.EOF, "", None, 2)

        token_list_manual = []
        token_list_manual.append(t1)
        token_list_manual.append(t2)
        token_list_manual.append(t3)
        token_list_manual.append(t4)
        token_list_manual.append(t5)
        token_list_manual.append(t6)
        token_list_manual.append(t7)
        token_list_manual.append(t8)
        token_list_manual.append(t9)
        token_list_manual.append(t10)
        token_list_manual.append(t11)
        token_list_manual.append(t12)

        error = DinoError()
        scan = Scanner(
            ' if(a > b) echo(a); end ', error)
        tlist = scan.generate_tokens()
        print("Length = , " ,len(tlist))
        for i in range(len(tlist)-1):
            self.assertEqual(tlist[i].ttype, token_list_manual[i].ttype)
            self.assertEqual(tlist[i].text, token_list_manual[i].text)
            self.assertEqual(tlist[i].literal,
                             token_list_manual[i].literal)
            self.assertEqual(tlist[i].line, token_list_manual[i].line)

    def test_tokenizer_lambda(self):

        '''lambda a=2 in a+1 end;'''

        t1 = Token(TokenType.LAMBDA, "lambda", None, 1)
        t2 = Token(TokenType.IDENTIFIER, "a", None, 1)
        t3 = Token(TokenType.EQUAL, "=", None, 1)
        t4 = Token(TokenType.INTEGER, "2", 2, 1)
        t5 = Token(TokenType.IN, "in", None, 1)
        t6 = Token(TokenType.IDENTIFIER, "a", None, 1)
        t7 = Token(TokenType.PLUS, "+", None, 1)
        t8 = Token(TokenType.INTEGER, "1", 1, 1)
        t9 = Token(TokenType.END, "end", None, 1)
        t10 = Token(TokenType.SEMICOLON, ";", None, 1)
        t11 = Token(TokenType.EOF, "", None, 2)

        token_list_manual = []
        token_list_manual.append(t1)
        token_list_manual.append(t2)
        token_list_manual.append(t3)
        token_list_manual.append(t4)
        token_list_manual.append(t5)
        token_list_manual.append(t6)
        token_list_manual.append(t7)
        token_list_manual.append(t8)
        token_list_manual.append(t9)
        token_list_manual.append(t10)
        token_list_manual.append(t11)

        error = DinoError()
        scan = Scanner(
            ' lambda a=2 in a+1 end; ', error)
        tlist = scan.generate_tokens()

        for i in range(len(tlist)-1):
            self.assertEqual(tlist[i].ttype, token_list_manual[i].ttype)
            self.assertEqual(tlist[i].text, token_list_manual[i].text)
            self.assertEqual(tlist[i].literal,
                             token_list_manual[i].literal)
            self.assertEqual(tlist[i].line, token_list_manual[i].line)

    def test_tokenizer_loop(self):

        '''loop(i<1) a = a + 1 end;'''

        t1 = Token(TokenType.LOOP, "loop", None, 1)
        t2 = Token(TokenType.LEFT_PAREN, "(", None, 1)
        t3 = Token(TokenType.IDENTIFIER, "i", None, 1)
        t4 = Token(TokenType.LESS, "<", None, 1)
        t5 = Token(TokenType.INTEGER, "1", 1, 1)
        t6 = Token(TokenType.RIGHT_PAREN, ")", None, 1)
        t7 = Token(TokenType.IDENTIFIER, "a", None, 1)
        t8 = Token(TokenType.EQUAL, "=", None, 1)
        t9 = Token(TokenType.IDENTIFIER, "a", None, 1)
        t10 = Token(TokenType.PLUS, "+", None, 1)
        t11 = Token(TokenType.INTEGER, "1", 1, 1)
        t12 = Token(TokenType.END, "end", None, 1)
        t13 = Token(TokenType.SEMICOLON, ";", None, 1)
        t14 = Token(TokenType.EOF, "", None, 2)

        token_list_manual = []
        token_list_manual.append(t1)
        token_list_manual.append(t2)
        token_list_manual.append(t3)
        token_list_manual.append(t4)
        token_list_manual.append(t5)
        token_list_manual.append(t6)
        token_list_manual.append(t7)
        token_list_manual.append(t8)
        token_list_manual.append(t9)
        token_list_manual.append(t10)
        token_list_manual.append(t11)
        token_list_manual.append(t12)
        token_list_manual.append(t13)
        token_list_manual.append(t14)

        error = DinoError()
        scan = Scanner(
            ' loop(i<1) a = a + 1 end; ', error)
        tlist = scan.generate_tokens()

        for i in range(len(tlist)-1):
            self.assertEqual(tlist[i].ttype, token_list_manual[i].ttype)
            self.assertEqual(tlist[i].text, token_list_manual[i].text)
            self.assertEqual(tlist[i].literal,
                             token_list_manual[i].literal)
            self.assertEqual(tlist[i].line, token_list_manual[i].line)

    def test_tokenizer_assign(self):

        '''const assign a=1; '''

        t1 = Token(TokenType.CONST, "const", None, 1)
        t2 = Token(TokenType.ASSIGN, "assign", None, 1)
        t3 = Token(TokenType.IDENTIFIER, "a", None, 1)
        t4 = Token(TokenType.EQUAL, "=", None, 1)
        t5 = Token(TokenType.INTEGER, "1", 1, 1)
        t6 = Token(TokenType.SEMICOLON, ";", None, 1)
        t7 = Token(TokenType.EOF, "", None, 2)

        token_list_manual = []

        token_list_manual.append(t1)
        token_list_manual.append(t2)
        token_list_manual.append(t3)
        token_list_manual.append(t4)
        token_list_manual.append(t5)
        token_list_manual.append(t6)
        token_list_manual.append(t7)

        error = DinoError()
        scan = Scanner(
            ' const assign a=1; ', error)
        tlist = scan.generate_tokens()

        for i in range(len(tlist)-1):
            self.assertEqual(tlist[i].ttype, token_list_manual[i].ttype)
            self.assertEqual(tlist[i].text, token_list_manual[i].text)
            self.assertEqual(tlist[i].literal,
                             token_list_manual[i].literal)
            self.assertEqual(tlist[i].line, token_list_manual[i].line)