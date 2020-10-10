import operator
from fractions import Fraction


#  自定义一个表达式为表达式为负数的类
class NegativeError(Exception):
    def __init__(self):
        super(NegativeError, self).__init__()


class Calculation:
    def eval(op, a, b):                     # 当只有一个操作符的计算
        answer = 0
        if op == "+":
            answer = operator.add(a, b)
        elif op == "-":
            if operator.lt(a, b):           # a是否小于b
                raise NegativeError()       # 当被减数大于减数的时候，抛出异常
            else:
                answer = operator.sub(a, b)
        elif op == "*":
            answer = operator.mul(a, b)
        elif op == "/":
            if b == 0:
                raise ZeroDivisionError
            answer = operator.truediv(a, b)
            if isinstance(answer, float):    # 当答案为浮点数，转换为分数
                answer = operator.truediv(Fraction(a), Fraction(b))
        return answer


    def score(user_ans, ans_list):         # 正确率的计算
        correct = list()
        wrong = list()
        length = len(user_ans)
        for i, u, ans in zip(range(1, length + 1), user_ans, ans_list):
            if u == ans:
                correct.append(i)
            else:
                wrong.append(i)
        return correct, wrong
