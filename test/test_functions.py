import unittest
from evaluation.eval import *
from errors.error import *
from tokenizing.token_scanning import *
from parser.parser import *
from evaluation.eval import *
from evaluation.resolve import *


class TestFunctions(unittest.TestCase):
    def test_functions_1(self):
        error = DinoError()
        code = "func add(a, b) return (a + b); end add(2, 3);"
        scanned_code = Scanner(code, error)
        token_list = scanned_code.generate_tokens()
        parser = Parser(token_list, error)
        expression = parser.parse()
        resolved = resolution(expression)
        output = evaluate(resolved)

        # Should return 5 as 2 + 3 = 5
        self.assertEqual(output, 5)

    def test_functions_2(self):
        error = DinoError()
        code = 'func e() return "Nothing"; end e();'
        scanned_code = Scanner(code, error)
        token_list = scanned_code.generate_tokens()
        parser = Parser(token_list, error)
        expression = parser.parse()
        resolved = resolution(expression)
        output = evaluate(resolved)

        # Should return "Nothing" as that is what the function returns
        self.assertEqual(output, StrLiteral(value='Nothing', line=1))

    def test_functions_3(self):
        error = DinoError()
        code = '''func even_fibo(n) 
                    assign a = 1;
                    assign b = 2;
                    assign sum = 0;
                    assign temp = 0;
                    loop(temp < n) 
                        temp = b;
                        if (temp % 2 == 0) 
                            sum = sum + temp; 
                        end
                        temp = a + b;
                        a = b;
                        b = temp; 
                    end 
                    return sum;
                end

                even_fibo(4000000);'''
        scanned_code = Scanner(code, error)
        token_list = scanned_code.generate_tokens()
        parser = Parser(token_list, error)
        expression = parser.parse()
        resolved = resolution(expression)
        output = evaluate(resolved)

        # Should return 4613732 as the sum of even fibonacci numbers below 4 million
        self.assertEqual(output, 4613732)

    def test_functions_4(self):
        error = DinoError()
        code = '''func fact(n)
                    assign f = 1;
                    if (n>1)
                            f = n*fact(n-1);
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

        # Should return 120 as 5! = 120
        self.assertEqual(output, 120)

    def test_functions_5(self):
        error = DinoError()
        code = 'func g() return "Nothing"; end '
        scanned_code = Scanner(code, error)
        token_list = scanned_code.generate_tokens()
        parser = Parser(token_list, error)
        expression = parser.parse()
        resolved = resolution(expression)
        output = evaluate(resolved)

        # Should return nothing as the function is not called
        self.assertEqual(output, None)

    def test_functions_6(self):
        error = DinoError()
        code = '''func f1(a , b)
                        return (a + b);
                end

                func f2(a, b , c)
                    return (f1(a, b) + c);
                end

                func f3(a, b, c, d)
                    return (f2(a, b, c) + d);
                end

                f3(1, 2, 3, 4);'''
        scanned_code = Scanner(code, error)
        token_list = scanned_code.generate_tokens()
        parser = Parser(token_list, error)
        expression = parser.parse()
        resolved = resolution(expression)
        output = evaluate(resolved)

        # Should return 10 as 1 + 2 + 3 + 4 = 10
        # Here we use functions inside functions
        self.assertEqual(output, 10)

    def test_functions_7(self):
        error = DinoError()
        code = '''func expr(a , b)
                    func mul(a,b)
                            return a*b;
                    end

                    return (a + b + mul(a,b));
            end

            expr(2,3);'''
        scanned_code = Scanner(code, error)
        token_list = scanned_code.generate_tokens()
        parser = Parser(token_list, error)
        expression = parser.parse()
        resolved = resolution(expression)
        output = evaluate(resolved)

        # Should   return 11 as 2 + 3 + 2*3 = 11
        # Here we create a function inside a function
        self.assertEqual(output, 11)
