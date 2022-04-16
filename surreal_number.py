from itertools import product
from typing import Set, Union

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

        if not left_part:
            return f'{{ |{right_part}}}' if right_part else '.'
        if not right_part:
            return f'{{{left_part}| }}'

        return f'{{{left_part}|{right_part}}}'

class SurrealNumber(BasicSurrealNumber):  # 为了避免类过于复杂，将比较运算符和算术运算符分离
    
    def __add__(self, other: 'SurrealNumber') -> 'SurrealNumber':
        left_result = {other + left_member for left_member in self.left}  # 这里是用于存储最终返回值的集合
        right_result = {other + right_member for right_member in self.right}
        left_updater = {self + left_member for left_member in other.left}  # 这里是用于求并集的集合
        right_updater = {self + right_member for right_member in other.right} 
        
        left_result = left_result.union(left_updater)  # 下面两行是求并集的操作
        right_result = right_result.union(right_updater)

        return self.__class__(left=left_result, right=right_result)

    def __neg__(self) -> 'SurrealNumber':
        return self.__class__(
            left={-right_member for right_member in self.right},
            right={-left_member for left_member in self.left}
        )
    
    def __sub__(self, other: 'SurrealNumber') -> 'SurrealNumber':
        return self + (-other)

    @staticmethod
    def _mul_handler(
        x: 'SurrealNumber',
        y: 'SurrealNumber',
        x_list: Set['SurrealNumber'],
        y_list: Set['SurrealNumber']
    ) -> Set['SurrealNumber']:
        
        return {
            x_member * y
            + y_member * x
            - x_member * y_member
            for x_member, y_member in product(x_list, y_list)
        }

    def __mul__(self, other: 'SurrealNumber') -> 'SurrealNumber':  # 操作逻辑与上方的 __add__ 基本相同
        left_result = self._mul_handler(self, other, self.left, other.left)
        right_result = self._mul_handler(self, other, self.right, other.right)
        left_updater = self._mul_handler(self, other, self.left, other.right)
        right_updater = self._mul_handler(self, other, self.right, other.left)
        
        left_result = left_result.union(left_updater)
        right_result = right_result.union(right_updater)

        return self.__class__(left=left_result, right=right_result)

class SurrealNumberClass(object):
    
    __slot__ = ['representation', 'left', 'right']
    
    def __init__(self, group: Union['SurrealNumber', 'SurrealNumberClass', Set['SurrealNumber']]) -> None:
        self.group = set()
        self.representation = None
        if isinstance(group, set):
            while group.len():
                self.add_member(group.pop())
        
        elif isinstance(group, SurrealNumber):
            self.group.add(group)
            self.representation = group
        
        else:
            self.representation = group.representation
            self.merge(group)
    
    def add_member(self, member: 'SurrealNumber') -> None:
        if self.representation is None:
            self.representation = member
            self.group.add(member)

        elif self.representation >= member and self.representation <= member:
            self.group.add(member)
            if len(member.left) + len(member.right) < len(self.representation.left) + len(self.representation.right):
                self.representation = member
                
    def merge(self, other: 'SurrealNumberClass') -> None:
        if self.representation <= other.representation and self.representation >= other.representation:
            self.group.update(other.group)
            other.group = self.group.copy()
        
        if len(other.representation.left) + len(other.representation.right) < len(self.representation.left) + len(self.representation.right):
            self.representation = other.representation
        else:
            other.representation = self.representation
    
    def __add__(self, other: 'SurrealNumberClass') -> 'SurrealNumberClass':  # 对数集做运算的结果是对数集中每个数做运算
        result = self.__class__
        for self_member, other_member in product(self.group, other.group):
            result.add_member(self_member + other_member)
        
        return result

BSN = BasicSurrealNumber
SN = SurrealNumber
SNC = SurrealNumberClass

__all__ = ['BSN', 'BasicSurrealNumber', 'SN', 'SurrealNumber']
