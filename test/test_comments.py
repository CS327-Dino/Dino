import unittest
from evaluation.eval import *
from errors.error import *
from tokenizing.token_scanning import *
from parser.parser import *
from evaluation.eval import *
from evaluation.resolve import *


class TestFunctions(unittest.TestCase):
    def test_comments_1(self):
        error = DinoError()
        code = "func add(a, b) return (a + b); end add(2, 3); ?"
        scanned_code = Scanner(code, error)
        token_list = scanned_code.generate_tokens()
        parser = Parser(token_list, error)
        expression = parser.parse()
        resolved = resolution(expression)
        output = evaluate(resolved)

        # Should return 5 as 2 + 3 = 5 as no comments
        self.assertEqual(output, 5)

    def test_comments_2(self):
        error = DinoError()
        code = '''func e() return "Nothing"; end ? e();
        assign a = "Hello";
        ? a;'''
        scanned_code = Scanner(code, error)
        token_list = scanned_code.generate_tokens()
        parser = Parser(token_list, error)
        expression = parser.parse()
        resolved = resolution(expression)
        output = evaluate(resolved)
        # Should return '' as the final expression is commented
        self.assertEqual(output, None)

    def test_comments_3(self):
        error = DinoError()
        code = '''func even_fibo(n) 
                    assign a = 1;
                    assign b = 2;
                    assign sum = 0;
                    assign temp = 0;
                    ?: loop(temp < n) 
                        temp = b;
                        if (temp % 2 == 0) 
                            sum = sum + temp; 
                        end
                        temp = a + b;
                        a = b;
                        b = temp; 
                    end :? 
                    return sum;
                end

                even_fibo(4000000);'''
        scanned_code = Scanner(code, error)
        token_list = scanned_code.generate_tokens()
        parser = Parser(token_list, error)
        expression = parser.parse()
        resolved = resolution(expression)
        output = evaluate(resolved)

        # Should return 0 as the loop inside the function is multi line commented
        self.assertEqual(output, 0)

    def test_comments_4(self):
        error = DinoError()
        code = '''func fact(n)
                    assign f = 1;
                    if (n>1)
                            ? f = n*fact(n-1);
                    end
                    return f;
            end

            assign n = 5;
            fact(n);'''
        scanned_code = Scanner(code, error)
        token_list = scanned_code.generate_tokens()
        parser = Parser(token_list, error)
        expression = parser.parse()
        resolved = resolution(expression)
        output = evaluate(resolved)

        # Should return 1 as the recursive part is commented using a single line comment
        self.assertEqual(output, 1)

    def test_comments_5(self):
        error = DinoError()
        code = '''assign a1 = 5;
        assign b1 = 6;
        assign c1 = a1 ?:+ b:?;
        c1; 
        '''
        scanned_code = Scanner(code, error)
        token_list = scanned_code.generate_tokens()
        parser = Parser(token_list, error)
        expression = parser.parse()
        resolved = resolution(expression)
        output = evaluate(resolved)

        # Using multi line comment to comment out a part of a line :)
        self.assertEqual(output, 5)

    def test_comments_6(self):
        error = DinoError()
        code = '''?func f1(a , b)
                ?        return (a + b);
                ?end

                ?func f2(a, b , c)
                ?    return (f1(a, b) + c);
                ?end

                ?func f3(a, b, c, d)
                ?    return (f2(a, b, c) + d);
                ?end

                ?f3(1, 2, 3, 4);'''
        scanned_code = Scanner(code, error)
        token_list = scanned_code.generate_tokens()
        parser = Parser(token_list, error)
        expression = parser.parse()
        resolved = resolution(expression)
        output = evaluate(resolved)

        # Using ? to comment out multiple lines at once
        self.assertEqual(output, None)

    def test_comments_7(self):
        error = DinoError()
        code = '''func expr(a , b)
                    func mul(a,b)
                            return a*b;
                    end

                    return (a ?: + b:? + mul(a,b));
            end

            expr(2,3);'''
        scanned_code = Scanner(code, error)
        token_list = scanned_code.generate_tokens()
        parser = Parser(token_list, error)
        expression = parser.parse()
        resolved = resolution(expression)
        output = evaluate(resolved)

        # Should return 8 as 2 + 2*3 = 8
        # We have commented out a part of the expression
        self.assertEqual(output, 8)

    def test_comments_8(self):
        error = DinoError()
        code = '''assign str1 = "Hel?lo";
        assign str2 = "Wo?:r:?ld";
        assign str3 = str1 + str2;
        str3;'''
        scanned_code = Scanner(code, error)
        token_list = scanned_code.generate_tokens()
        parser = Parser(token_list, error)
        expression = parser.parse()
        resolved = resolution(expression)
        output = evaluate(resolved)

        # Should return "Hel?loWo?:r:?ld" as the comments are used in a string and hence they should be ignored
        self.assertEqual(output, 'Hel?loWo?:r:?ld')
