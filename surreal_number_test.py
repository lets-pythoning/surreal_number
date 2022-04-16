from unittest import TestCase, TestSuite, TextTestRunner

from surreal_number import BSN, SN, SNC

class BasicSurrealNumberTest(TestCase):

    def setUp(self) -> None:
        self.alpha = alpha = BSN()
        self.beta = beta = BSN(left=set(), right={alpha})
        self.gamma = gamma = BSN(left={alpha}, right=set())
        self.delta = BSN(left={beta}, right={gamma})

    def test_construct(self) -> None:
        alpha = self.alpha
        with self.assertRaises(ArithmeticError):
            BSN(left=[alpha], right=[alpha])  # 测试构造函数对不正确数据的鲁棒性
    
    def test_output(self) -> None:
        alpha = self.alpha
        beta = self.beta
        gamma = self.gamma
        delta = self.delta
        
        self.assertEqual(str(alpha), '.')
        self.assertEqual(str(beta), '{ |.}')
        self.assertEqual(str(gamma), '{.| }')
        self.assertEqual(str(delta), '{{ |.}|{.| }}')
    
    def test_compare(self) -> None:
        alpha = self.alpha
        beta = self.beta
        gamma = self.gamma
        
        self.assertTrue(beta <= alpha)  # 以下表达的是原博客中的第一个例子的前半句话
        self.assertTrue(alpha <= gamma)
        self.assertTrue(beta <= gamma)
        
        self.assertTrue(alpha >= beta)  # 以下表达的是原博客中的第一个例子的后半句话
        self.assertTrue(gamma >= alpha)
        self.assertTrue(gamma >= beta)
        
        self.assertFalse(alpha <= beta)  # 以下表达的是原博客中的第二个例子的前半句话
        self.assertFalse(gamma <= alpha)
        self.assertFalse(gamma <= beta)
        
        self.assertFalse(beta >= alpha)  # 以下表达的是原博客中的第二个例子的后半句话
        self.assertFalse(alpha >= gamma)
        self.assertFalse(beta >= gamma)

class SurrealNumberTest(TestCase):
    
    def setUp(self) -> None:
        self.addTypeEqualityFunc(SN, self.is_equal)  # 绑定比较函数
        
        self.alpha = alpha = SN()
        self.beta = beta = SN(left=set(), right={alpha})
        self.gamma = gamma = SN(left={alpha}, right=set())
        self.delta = SN(left={beta}, right={gamma})
    
    @staticmethod
    def is_equal(first: 'SN', second: 'SN', msg: str = None) -> bool:  # 临时比较函数，不是真的相等，就是比较两个元素的实质而非特性
        if len(first.left) != len(second.left):
            return False
        
        first_left = {str(left_member) for left_member in first.left}
        second_left = {str(left_member) for left_member in second.left}
        for first_member in first_left:
            if first_member not in second_left:
                return False
        
        if len(first.right) != len(second.right):
            return False

        first_right = {str(right_member) for right_member in first.right}
        second_right = {str(right_member) for right_member in second.right}
        for first_member in first_right:
            if first_member not in second_right:
                return False
    
    def test_additive_associativity(self) -> None:
        alpha = self.alpha
        beta = self.beta
        gamma = self.gamma
        delta = self.delta
        
        self.assertEqual(beta + delta, delta + beta)  # 以下表达的是原博客加法的第一个例子，加法交换律
        self.assertEqual((beta + gamma) + delta, beta + (gamma + delta))  # 加法结合律
        
        self.assertTrue(beta <= alpha)  # 以下表达的是原博客加法的第二个例子，不等式公理
        self.assertTrue(alpha <= gamma)
        self.assertTrue(alpha + beta <= alpha + gamma)
        
        self.assertTrue(gamma >= beta)
        self.assertTrue(
            (gamma + delta <= beta + alpha and delta <= alpha) 
            or (gamma + delta >= beta + alpha and delta >= alpha)
        )  # 根据第二个例子，两种情况必有一种情况成立
    
    def test_multiply(self) -> None:
        alpha = self.alpha
        beta = self.beta
        gamma = self.gamma
        delta = self.delta
        
        self.assertEqual(alpha * delta, alpha)  # 原博客乘法的第一个例子，0 乘以任何数都等于 0
        self.assertEqual(gamma * delta, delta)  # 1 乘以任何数都等于它本身
        
        self.assertTrue(beta <= alpha)  # 原博客乘法的第二个例子，不等式的另一个公理
        self.assertTrue(beta <= gamma)
        self.assertTrue(beta * delta <= gamma * delta)

class SurrealNumberClassTest(TestCase):
    
    def setUp(self) -> None:
        ...
    
    def test_initialize(self) -> None:
        ...
    
    def test_add_member(self) -> None:
        ...
    
    def test_merge(self) -> None:
        ...
    
    def test_add(self) -> None:
        ...

if __name__ == '__main__':
    suite = TestSuite()
    
    suite.addTest(BasicSurrealNumberTest('test_construct'))
    suite.addTest(BasicSurrealNumberTest('test_output'))
    suite.addTest(BasicSurrealNumberTest('test_compare'))
    
    suite.addTest(SurrealNumberTest('test_additive_associativity'))
    
    runner = TextTestRunner()
    runner.run(suite)
