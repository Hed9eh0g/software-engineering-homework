import os
import random
from fractions import Fraction
from calc import Calculation
from calc import NegativeError
from file import File
from format_process import Convert

class Node:
    # 节点类
    def __init__(self):
        self.type = 0  # 节点的类别：{初始化：0， 数字：1， 操作符：2， }
        self.operator = None  # 操作符类型
        self.number = None  # 操作结果
        self.left = None  # 左子树
        self.right = None  # 右子树
        self.op_priority = {'+': 1, '-': 1, '*': 2, '/': 2}  # 设置操作符的优先级

    def get_answer(self):   # 计算我们每个子树的计算结果并检测结果
        if self.type == 2:
            self.left.get_answer()
            self.right.get_answer()
            self.number =Calculation.eval(
                self.operator, self.left.number, self.right.number)
        else:
            return

    def get_formula(self):   # 获取我们的中序表达式，在这里根据添加小括号以区别优先级
        formula = list()
        if self.type == 1:
            return [self.number]
        elif self.type == 2:
            if self.left.type == 2 and \
                self.op_priority[str(self.operator)] > self.op_priority[str(self.left.operator)]:
                '''处理左子树'''
                formula.append('(')                                      # 当我们的父母节点的操作符的优先级大于或等于我们的孩子节点的时候，在子树添加小括号
                formula += self.left.get_formula()
                formula.append(')')
            else:
                formula += self.left.get_formula()

            formula.append(self.operator)                                 # 中间节点的处理

            '''当右孩子是操作符时'''
            if self.right.type == 2 and \
                    self.op_priority[str(self.operator)] >= self.op_priority[str(self.right.operator)]:
                formula.append('(')                                        # 当我们的父母节点的操作符优先级大于或等于我们的孩子节点时，在子树添加小括号
                formula += self.right.get_formula()
                formula.append(')')
            else:
                formula += self.right.get_formula()
            return formula


class Tree:
    # 树类
    def __init__(self):
        self.root = Node()
        self.op_list = ["+", "-", "*", "/"]                               # 根节点的符号类型
        self.type = [1, 2]                                           # 节点类型，1表示整数，2表示分数
        self.middle_formula = list()                                      # 中缀表达式
        self.after_formula = list()                                       # 后缀表达式
        self.formula = list()                                             # 格式化后的表达式
        self.answer = list()                                              # 格式标准化的答案


    def create(self, num_range, number):
        num = 0
        while num < number:    # number表示生成表达式的数量
            degree = random.choice([1, 2, 3])  # 随机选择操作符的数量，最多有三个
            empty_node = [self.root]
            for _ in range(degree):
                node = random.choice(empty_node)
                empty_node.remove(node)
                node.operator = random.choice(self.op_list)
                node.type = 2
                node.left = Node()
                node.right = Node()
                empty_node.append(node.left)
                empty_node.append(node.right)

            for node in empty_node:
                node.type = 1
                num_type = random.choice(self.type)   # 随机选择，生成整数还是小数
                if num_type == 1:
                    node.number = random.randint(1, number)
                else:
                    node.number = Fraction(random.randint(1, num_range), random.randint(1, num_range))
            try:
                self.root.get_answer()                                               # 计算答案，检查生成的子表达式
                self.middle_formula = self.root.get_formula()                        # 中缀表达式
                self.after_formula = Convert.get_after_formula(self.middle_formula)  # 将中缀表达式后缀表达式
                output = Convert.standard_output(self.middle_formula)                # 中缀表达式化为输出的标准模式
                if isinstance(self.root.number, Fraction):
                    answer = Convert.stanard_fraction(self.root.number)                # 将答案化为输出的标准模式
                else:
                    answer = self.root.number
                if answer in self.answer:                                             # 重复度查询，只要计算答案一致，都不加入我们的题库，从结果解决问题
                    continue
                else:
                    self.formula.append(output)
                    self.answer.append(answer)
            except NegativeError:                                                      # 异常处理，结果不可为负数
               continue
            except ZeroDivisionError:
                continue
            else:
                num += 1
        return self.formula, self.answer


