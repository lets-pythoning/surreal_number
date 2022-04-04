from fractions import Fraction
from random import randint
from unittest import TestCase, main

from real_number import RN

class RationalNumberTest(TestCase):
    
    def test_construct(self) -> None:
        num = RN(100, 10, -1)
        self.assertEqual(num.denominator, 1)
        self.assertEqual(num.numerator, 10)
        
        with self.assertRaises(ArithmeticError):
            invalid_num = RN(114514, 0)
        
        with self.assertRaises(ArithmeticError):
            invalid_num = RN(114514, 114514, 0)
            
        num = RN(13, 17)
        self.assertEqual(num.denominator, 17)
        self.assertEqual(num.numerator, 13)
    
    def test_output(self) -> None:
        num = RN(114514, 13, -1)
        self.assertEqual(str(num), '-114514 / 13')
        
        num = RN(0, 114514, -1)
        self.assertEqual(str(num), '0')
    
    def test_compute(self) -> None:
        for _ in range(100):
            a = RN(randint(10, 1000), randint(10, 1000))
            a_copy = Fraction(a.numerator, a.denominator)
            b = RN(randint(10, 1000), randint(10, 1000))
            b_copy = Fraction(b.numerator, b.denominator)
            
            self.assertEqual((a + b).denominator, (a_copy + b_copy).denominator)
            self.assertEqual((a + b).numerator, abs((a_copy + b_copy).numerator))
            self.assertEqual((a - b).denominator, (a_copy - b_copy).denominator)
            self.assertEqual((a - b).numerator, abs((a_copy - b_copy).numerator))
            self.assertEqual((a * b).denominator, (a_copy * b_copy).denominator)
            self.assertEqual((a * b).numerator, abs((a_copy * b_copy).numerator))
            self.assertEqual((a / b).denominator, (a_copy / b_copy).denominator)
            self.assertEqual((a / b).numerator, abs((a_copy / b_copy).numerator))

    def test_compare(self) -> None:
        self.assertTrue(RN(0, 1, -1) == RN(0, 1))
        self.assertTrue(RN(114514, 114514 * 2, -1) == RN(1, 2, -1))
        self.assertTrue(RN(114514 * 2, 1, -1) < RN(114514, 1, -1) < 1)
        self.assertTrue(RN(111, 100) > RN(11000, 10000))
        self.assertTrue(RN(111, 100) >= RN(11000, 10000))
        self.assertTrue(RN(111, 100, -1) < RN(11000, 10000, -1))
        self.assertTrue(RN(111, 100, -1) <= RN(11000, 10000, -1))

if __name__ == '__main__':
    main()
