#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys

#10分割されたそれぞれの文のリストを10個分つくって、それをテストデータとして分ける
#shufしたtextを入力にする
def cross_validation():

    value = 0
    line_list = []

    for line in open(sys.argv[1], "r"):
        value += 1
        line_list.append(line)

    quotient = value / 10
    remainder = value - quotient * 10

    #テストデータを作っています
    for i in range(10):
        text_name = "mainichi98_99_feature/mainichi9899_12_feature/splits/split.%s" % (i + 1)
        with open(text_name, "w") as pf:
            for j in range(i * quotient, (i + 1) * quotient):
                pf.write(line_list[j])

            if remainder - i - 1 > -1:
                pf.write(line_list[value - i - 1])


if __name__ == "__main__":
    cross_validation()


