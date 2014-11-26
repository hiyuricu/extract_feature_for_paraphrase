#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys
from collections import defaultdict

def skew_divergence(read_file, X_list, Y_list):

    dependency_word_dic = defaultdict(dict)
    string = ""
    string_list = []
    line_features_temp_list = []
    phrase_temp_dic = {}

    for line in open(read_file, "r"):

        line = line.strip()
        if line[0:7] == "* 0 -1D":
            pass

        elif line[0:2] == "* ":
            if string != "" and line_features_temp_list != []:
                phrase_temp_dic[string] = [line_features_temp_list[1], line_features_temp_list[2][0:-1]]
                string_list.append(string)
                string = ""
            line_features_temp_list = line.split(" ")

        elif line[0:3] == "EOS":
            if string != "" and line_features_temp_list != []:
                phrase_temp_dic[string] = [line_features_temp_list[1], line_features_temp_list[2][0:-1]]
                string_list.append(string)
                for string in string_list:
                    for X in open(X_list, "r"):
                        if X in string:
                            for key, value_list in phrase_temp_dic.items():
                                if phrase_temp_dic[string][1] == value_list[0]:
                                    if key in dependency_word_dic[X]:
                                        dependency_word_dic[X][key] += 1
                                    else:
                                        dependency_word_dic[X][key] = 1

                    for Y in open(Y_list, "r"):
                        if Y in string:
                            for key, value_list in phrase_temp_dic.items():
                                if phrase_temp_dic[string][1] == value_list[0]:
                                    if key in dependency_word_dic[Y]:
                                        dependency_word_dic[Y][key] += 1
                                    else:
                                        dependency_word_dic[Y][key] = 1
            phrase_temp_dic = {}
            string_list = []
            string = ""
            line_features_temp_list = []

        else:
            string = string + line.split("\t")[0]

    return dependency_word_dic

if __name__ == "__main__":
    for k,dic in skew_divergence(sys.argv[1], sys.argv[2], sys.argv[3]).items():
        print k
        for k2,v in dic.items():
            print k2,v



