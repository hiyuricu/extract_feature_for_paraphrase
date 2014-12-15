#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys

#10分割されたそれぞれの文のリストを10個分つくって、それをテストデータとして分ける
def cross_validation():

    positive_value = 0
    negative_value = 0
    positive_line_list = []
    negative_line_list = []

    for line in open(sys.argv[1], "r"):

    	if line.strip().split()[0] == "+1":
            positive_value += 1
            positive_line_list.append(line)

    	elif line.strip().split()[0] == "-1" or line.strip().split()[0] == "-1.0":
            negative_value += 1
            negative_line_list.append(line)

    positive_quotient = positive_value / 10
    positive_remainder = positive_value - positive_quotient * 10

    negative_quotient = negative_value / 10
    negative_remainder = negative_value - negative_quotient * 10

    #テストデータを作っています
    for i in range(10):
        text_name = "mainichi98_99_feature/mainichi9899_12_feature/splits/split.%s" % (i + 1)
        with open(text_name, "w") as pf:
            for j in range(i * positive_quotient, (i + 1) * positive_quotient):
                pf.write(positive_line_list[j])
            for j in range(i * negative_quotient, (i + 1) * negative_quotient):
                pf.write(negative_line_list[j])
            if positive_remainder - i - 1 > -1:
                pf.write(positive_line_list[positive_value - i - 1])
            if negative_remainder - i - 1 > -1:
                pf.write(negative_line_list[negative_value - i - 1])


if __name__ == "__main__":
    cross_validation()


