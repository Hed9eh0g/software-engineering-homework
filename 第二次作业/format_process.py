from fractions import Fraction


class Convert:

    def stanard_fraction(answer):     # 分数的处理，化为真分数
        if (answer > 1 or answer < -1) and answer.denominator != 1:
            a_numerator = answer.numerator % answer.denominator      # 分子为模分母求余
            a_denominator = answer.denominator                       # 分母
            a_right = Fraction(a_numerator, a_denominator)
            a_left = answer.numerator // answer.denominator          # 取整数部分
            result = str(a_left) + '\'' + str(a_right)
        else:
            result = str(answer)
        return result

    def standard_output(formula):      # 标准化输出时的格式
        output = str()
        for item in formula:
            if isinstance(item, Fraction):
                output += Convert.stanard_fraction(item)
            elif isinstance(item, int):
                output += str(item)
            elif item == '+':
                output += ' + '
            elif item == '-':
                output += ' - '
            elif item == '*':
                output += ' x '
            elif item == '/':
                output += ' ÷ '
            else:
                output += item
        output += ' ＝ '
        return output

    def get_after_formula(formula):     # 将中缀表达式转换为后缀表达式
        op_priority = {'(': 0, ')': 0, '+': 1, '-': 1, '*': 2, '/': 2}
        postfix_formula = list()  # 输出
        op_list = list()      # 充当栈
        for item in formula:
            if isinstance(item, int) or isinstance(item, Fraction):
                # 如果为数字直接输出
                postfix_formula.append(item)
            elif item == '(':
                # 输入时把左括号看坐最低优先级的，直接入栈
                op_list.append(item)
            elif item == ')':
                # 如果为右括号,优先级别最高，将里面的所有操作符输出
                while op_list[-1] != '(':
                    postfix_formula.append(op_list.pop())
                op_list.pop()  #
            else:
                # 如果为操作符,比较该操作符和栈顶的操作符优先级作比较
                # 如果优先级大于栈顶元素压栈,否则将op_list中优先级大于或等于该操作符的元素输出
                # 最后压栈
                while len(op_list) > 0 and op_priority[op_list[-1]] >= op_priority[item]:
                    postfix_formula.append(op_list.pop())
                op_list.append(item)

        while op_list:
            # 将剩余的op_list出栈
            postfix_formula.append(op_list.pop())

        return postfix_formula

