#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import string
import re
import MeCab
import math
from collections import defaultdict

#素性のリストをappendするリストなので形式はリストのリストとなる
features_list = []
N = 0

X_value_dic_for_co_occur = defaultdict(int)
Y_value_dic_for_co_occur = defaultdict(int)
XY_value_dic_for_co_occur = defaultdict(int)

#csvファイルを読み込むように設計されている
def main(read_file):
    #共起度のための辞書を作成する
    for line in open(read_file,"r"):
        N += 1
        line = line.strip()
        temporary_features_list = line.split(",")
        X_value_dic_for_co_occur[temporary_features_list[1]] += 1
        Y_value_dic_for_co_occur[temporary_features_list[2]] += 1
        XY_value_dic_for_co_occur[temporary_features_list[1] + temporary_features_list[2]] += 1

    character_inclusion(read_file)
    co_occur_value(read_file, N)

    wf = open('feature_for_paraphrase.txt',"w")
    for features in features_list:
            #事例に対する要素の数は一定でないので修正する必要があるかもしれない
            wf.write("%s\t%s\n" % (features[0], features[3]))
    wf.close()

#文字の包含の部分。現状連続した文字が包含されているかどうかしか見ていない(ポケットモンスターがポケモンのように連続していない略語は負となる)
def character_inclusion(read_file):
    for line in open(read_file,"r"):
        line = line.strip()
        temporary_features_list = line.split(",")

        if temporary_features_list[2] in temporary_features_list[1]:
            temporary_features_list.append("1:1")
        else:
            #一事例に対して素性は一つはなければならないので一時的に1:0をappendするようにするが、本来0の素性はappendしない
            temporary_features_list.append("1:0")
        features_list.append(temporary_features_list)

def co_occur_value(read_file, N):
    for line in open(read_file,"r"):
        n11 = 0
        n12 = 0
        n21 = 0
        n22 = 0
        kay_square = 0
        line = line.strip()
        temporary_features_list = line.split(",")
        if temporary_features_list[1] + temporary_features_list[2] in XY_value_dic_for_co_occur:
            n11 = XY_value_dic_for_co_occur[temporary_features_list[1] + temporary_features_list[2]]
        if temporary_features_list[1] in X_value_dic_for_co_occur:
            n12 = X_value_dic_for_co_occur[temporary_features_list[1]] - n11
        if temporary_features_list[2] in Y_value_dic_for_co_occur:
            n21 = Y_value_dic_for_co_occur[temporary_features_list[2]] - n11
        n22 = N - n11 - n12 - n21
        kay_square = 

if __name__ == "__main__":
    main(sys.argv[1])