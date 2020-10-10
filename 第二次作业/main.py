import os
import sys
import argparse
from tree import Tree
from file import File
from calc import Calculation


parser = argparse.ArgumentParser()
parser.add_argument('-n', dest='amount', type=int, default=10, help='生成题目的数量')
parser.add_argument('-r', dest='range', type=int, default=10, help='生成题目中的数值，自然数以及真分数分母的范围')
args = parser.parse_args()


if __name__ == '__main__':
    question_path = os.path.join(os.getcwd(), 'Questions.txt')
    answer_path = os.path.join(os.getcwd(), 'Answers.txt')
    score_path = os.path.join(os.getcwd(), 'Score.txt')
    print("Welcome to T1e9u & Hed9eh0g's program!")
    print("Input Hed9eh0g_is_handsome to exit")
    t = Tree()
    student_answers = list()
    generatives, answers = t.create(args.range, args.amount)                      # 题目以及答案的生成
    File.write_file(generatives, answers, question_path, answer_path)             # 题目文件以及答案文件的生成
    for i in range(args.amount):
        print(generatives[i], end='')
        answer = input()
        student_answers.append(answer)
    correct, wrong = Calculation.score(student_answers, answers)                   # 成绩的统计
    File.write_grade_file(score_path, correct, wrong)                              # 保存答题结果