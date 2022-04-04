from typing import Union

class RationalNumber(object):
    
    __slot__ = ['numerator', 'denominator', 'sign']
    
    def __init__(self, numerator: int = 0, denominator: int = 1, sign: int = 1) -> None:
        self.numerator = numerator
        self.denominator = denominator
        self.sign = sign

        if denominator == 0:
            raise ArithmeticError('The denominator cannot be zero.')  # 避免在运算时才报错，防患于未然；暂不使用 property 控制值非零
        if sign not in [1, -1]:
            raise ArithmeticError(f'Cannot recognize the sign: {sign}.')  # 符号只有 1 代表的正数和 -1 代表的负数

        gcd = self._gcd(numerator, denominator)  # 化简
        self.numerator //= gcd
        self.denominator //= gcd
    
    @staticmethod  # 这样就不需要传 self，且有多个对象时，这个函数只创建一次且不能修改
    def _gcd(first: int, second: int) -> int:  # 非递归的_gcd
        if first < second:
            first, second = second, first  # 必须前大后小
        
        while second != 0:
            first, second = second, first % second  # 辗转相除
        
        return first
    
    def __add__(self, other: 'RationalNumber') -> 'RationalNumber':
        result = self.__class__()  # 初始化一个合理的返回值
        
        if self.denominator == other.denominator:
            result.denominator = self.denominator
            result.numerator = self.sign * self.numerator + other.sign * other.numerator
        
        else:
            gcd = self._gcd(self.denominator, other.denominator)
            result.denominator = self.denominator * other.denominator  # 模拟通分
            result.numerator = (
                self.sign * self.numerator * other.denominator 
                + other.sign * other.numerator * self.denominator
            )  # 模拟通分中的分子交叉相乘
    
        if result.numerator < 0:
            result.sign = -1  # 根据结果定符号
            result.numerator = abs(result.numerator)  # 求绝对值
        
        gcd = self._gcd(result.denominator, result.numerator)
        result.denominator //= gcd
        result.numerator //= gcd
        
        return result

    def __sub__(self, other: 'RationalNumber') -> 'RationalNumber':
        return self.__add__(self.__class__(other.numerator, other.denominator, -other.sign))  # 加上相反数

    def __mul__(self, other: 'RationalNumber') -> 'RationalNumber':
        result = self.__class__()
        
        result.denominator = self.denominator * other.denominator  # 分母相乘
        result.numerator = self.numerator * other.numerator  # 分子相乘
        result.sign = self.sign * other.sign  # 界定符号
        
        gcd = self._gcd(result.denominator, result.numerator)  # 模拟约分
        result.denominator //= gcd
        result.numerator //= gcd

        return result
    
    def __truediv__(self, other: 'RationalNumber') -> 'RationalNumber':
        return self.__mul__(self.__class__(other.denominator, other.numerator, other.sign))  # 乘上倒数
    
    def __eq__(self, other: Union['RationalNumber', int, float]) -> bool:
        if isinstance(other, int):  # 如果是整数
            return False if self.denominator != 1 else self.sign * self.numerator == other
        if isinstance(other, float):
            return self.sign * self.numerator / self.denominator == other  # 此处可能会有一点点精度问题

        return self - other == 0  # 比较相当于两数做差取符号，下同

    def __lt__(self, other: Union['RationalNumber', int, float]) -> bool:
        if isinstance(other, self.__class__):
            return self - other < 0

        return self.numerator / self.denominator * self.sign < other

    def __gt__(self, other: Union['RationalNumber', int, float]) -> bool:
        if isinstance(other, self.__class__):
            return self - other > 0

        return self.numerator / self.denominator * self.sign > other
    
    def __ne__(self, other: Union['RationalNumber', int, float]) -> bool:
        return not self.__eq__(other)  # 不相等相当于不+相等
    
    def __le__(self, other: Union['RationalNumber', int, float]) -> bool:
        return self.__lt__(other) or self.__eq__(other)

    def __ge__(self, other: Union['RationalNumber', int, float]) -> bool:
        return self.__gt__(other) or self.__eq__(other)
    
    def __str__(self) -> str:
        if self.numerator == 0:
            return '0'
            
        result = ''
        if self.sign == -1:
            result += '-'

        return f'{result}{self.numerator} / {self.denominator}'

class IrrationalNumber(object):
    
    __slot__ = ['lower_bound', 'upper_bound']
    
    def __init__(self, lower_bound: float = -0.00000000, upper_bound: float = 0.00000000) -> None:  # 所有默认值默认采用小数后八位精度，初始值为0
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        
        if self.lower_bound > self.upper_bound:
            raise ArithmeticError('Lower bound larger than upper bound.')  # 不正确的上下界会导致不正确的比较运算
    
    def __add__(self, other: 'IrrationalNumber') -> 'IrrationalNumber':
        return self.__class__(self.lower_bound + other.lower_bound, self.upper_bound + other.upper_bound)

    def __sub__(self, other: 'IrrationalNumber') -> 'IrrationalNumber':
        return self.__class__(self.lower_bound - other.lower_bound, self.upper_bound - other.upper_bound)

    def __mul__(self, other: 'IrrationalNumber') -> 'IrrationalNumber':
        return self.__class__(self.lower_bound * other.lower_bound, self.upper_bound * other.upper_bound)

    def __truediv__(self, other: 'IrrationalNumber') -> 'IrrationalNumber':
        return self.__class__(self.lower_bound / other.lower_bound, self.upper_bound / other.upper_bound)

    def __eq__(self, other: 'IrrationalNumber') -> bool:  # 由于不可预知的精度问题，以下运算不保证正确
        return self.lower_bound == other.lower_bound and self.upper_bound == other.upper_bound

    def __lt__(self, other: Union['IrrationalNumber', int, float]) -> bool:
        if isinstance(other, self.__class__):
            return self.lower_bound < other.lower_bound

        return self.upper_bound < other

    def __gt__(self, other: Union['IrrationalNumber', int, float]) -> bool:
        if isinstance(other, self.__class__):
            return self.upper_bound > other.upper_bound

        return self.lower_bound > other

    def __str__(self) -> str:
        return f'{self.lower_bound} ~ {self.upper_bound}'

RN = RationalNumber
IR = IrrationalNumber

__all__ = ['RN', 'RationalNumber', 'IR', 'IrrationalNumber']
