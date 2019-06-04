#!/usr/bin/python
# -*- coding: UTF-8 -*-

#global temp
temp = ""  # 临时字段
state = 0  # 状态转换图的状态

# 单词符号和种别对照表
ItemDict = {"begin": 1, "end": 2, "integer": 3, "if": 4, "then": 5, "else": 6, "function": 7, "read": 8, "write": 9, "=": 12, "<>": 13, "<=": 14, "<": 15, ">=": 16, ">": 17, "-": 18, "*": 19, ":=": 20, "(": 21, ")": 22, ";": 23}
Token = 10
Constants = 11
target = ""  # 需要生成的文件对应的字符串
file_name = "test.txt"  # 读入程序
error_file_name = file_name.split('.')[0]+".err"
target_file_name = file_name.split('.')[0]+".dyd"

def print_binary_function(print_word, num):
    """写target字符串 
    为 .dyd格式
    即： 单词符号(16)+一个空格+种别(2)"""
    global target
    target += ((16-len(print_word))*' '+print_word+' '+str(num)+'\n')


def init_file():
    """创建需要输出的文件"""
    error_file = open(error_file_name, "w")
    error_file.close()
    target_file = open(target_file_name, "w")
    target_file.close()


def error_write(type):
    if type == 0:
        error_info = "出现了无法识别的字符"
    elif type == 1 :
        error_info = "请注意，:后必须跟="
    error_file = open(error_file_name, "w")
    error_file.write(error_info)
    error_file.close()


def end_word():
    """终结并记录temp中的字段及其类别"""
    global temp
    if temp != "":
        if state == 1:
            # 若当前状态为字母
            if ItemDict.get(temp):
                print_binary_function(temp, ItemDict.get(temp))
            else:
                print_binary_function(temp, Token)
        elif state == 3:
            # 若当前状态为数字
            print_binary_function(temp, Constants)
        else:
            # 若当前状态为其他状态
            if ItemDict.get(temp):
                print_binary_function(temp, ItemDict.get(temp))
            else:
                error_write(1)
        temp = ""


init_file()
with open(file_name, "r") as file:
    for line in file:
        for word in line:
            # 下面这些操作参考《编译原理_实验作业》PPT第14,15页内容，其state值即为PPT圆圈中的值
            if word == ' ':
                if state != 0:
                    # 若当前读入字符为空白，且当前状态不为0，即上一个字符为有效字符，则终止temp，且将状态改为0
                    end_word()
                    state = 0
            elif 'z' >= word >= 'A':
                # 若当前读入为字母，且
                if state != 0 and state != 1:
                    end_word()
                temp += word
                state = 1
            elif '9' >= word >= '0':
                if state != 3:
                    end_word()
                temp += word
                state = 3
            elif word == '=':
                if state not in [0, 10, 14, 17]:
                    end_word()
                    temp += word
                    state = 5
                else:
                    temp += word
                    end_word()
                    state = 0
            elif word == '-':
                end_word()
                temp += word
                state = 6
            elif word == '*':
                end_word()
                temp += word
                state = 7
            elif word == '(':
                end_word()
                temp += word
                state = 8
            elif word == ')':
                end_word()
                temp += word
                state = 9
            elif word == '<':
                end_word()
                temp += word
                state = 10
            elif word == '>':
                if state != 10:
                    end_word()
                    state = 14
                else:
                    temp += word
                    state = 12
            elif word == ':':
                end_word()
                temp += word
                state = 17
            elif word == ';':
                end_word()
                temp += word
                state = 20
            elif word == '\n':
                end_word()
                state = 0
                print_binary_function("EOLN", 24)  # 行结束标志
            else:
                # 若还不能匹配，则记录对应的错误
                error_write(0)
    end_word()
    print_binary_function("EOF", 25)  # 文件结束标志
    with open(target_file_name, "w") as target_file:
        # 保存target到最顶的文件夹
        target_file.write(target)



