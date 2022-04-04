from itertools import product
from turtle import left
from typing import Set

class BasicSurrealNumber(object):
    
    __slot__ = ['left', 'right']
    
    def __init__(self, left: Set['BasicSurrealNumber'] = None, right: Set['BasicSurrealNumber'] = None) -> None:
        if left is None:
            left = set()
        if right is None:
            right = set()
            
        for left_member in left:
            for right_member in right:
                if left_member >= right_member:
                    raise ArithmeticError('Not a valid surreal number: breaking law 1.')  # 根据定义判断合法性

        self.left = left
        self.right = right
    
    def _hash(self) -> str:  # 返回一个递归生成的二进制的字符串，用于哈希
        return ''.join(member._hash() for member in self.left) if self.left else '0' \
               + '1' \
               + ''.join(member._hash() for member in self.right) if self.right else '0'
    
    def __hash__(self) -> int:  # 必须有此方法，否则无法加入集合中
        return int(self._hash(), 2)
    
    def __le__(self, other: 'BasicSurrealNumber') -> bool:
        return (not any(
            left_member >= other for left_member in self.left  # 检查前者的左集合里是否存在大于等于后者的数
        )) and (not any(
            right_member <= self for right_member in other.right  # 检查后者的右集合里是否存在小于等于前者的数
        ))  # 以上是语法糖，理解作用即可
    
    def __ge__(self, other: 'BasicSurrealNumber') -> bool:  # 这两个运算符号是等效的
        return other <= self
    
    def __str__(self) -> str:
        left_part = ', '.join(str(member) for member in self.left)
        right_part = ', '.join(str(member) for member in self.right)

        if not left_part and not right_part:
            return '.'
        if not left_part:
            return f'{{ |{right_part}}}'
        if not right_part:
            return f'{{{left_part}| }}'

        return f'{{{left_part}|{right_part}}}'

class SurrealNumber(BasicSurrealNumber):  # 为了避免类过于复杂，将比较运算符和算术运算符分离
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __add__(self, other: 'SurrealNumber') -> 'SurrealNumber':
        left_result = {other + left_member for left_member in self.left}  # 这里是用于存储最终返回值的集合
        right_result = {other + right_member for right_member in self.right}
        left_updater = {self + left_member for left_member in other.left}  # 这里是用于求并集的集合
        right_updater = {self + right_member for right_member in other.right} 
        
        left_result = left_result.union(left_updater)  # 下面两行是求并集的操作
        right_result = right_result.union(right_updater)

        return self.__class__(left=left_result, right=right_result)

    def __invert__(self) -> 'SurrealNumber':
        return self.__class__(
            left={-right_member for right_member in self.right},
            right={-left_member for left_member in self.left}
        )

BSN = BasicSurrealNumber
SN = SurrealNumber

__all__ = ['BSN', 'BasicSurrealNumber', 'SN', 'SurrealNumber']
