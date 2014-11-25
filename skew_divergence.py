#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys

def skew_divergence(read_file):

    dependency_word_dic = {}
    string = ""
    string_list = []
    line_features_list = []
    phrase_temp_dic = {}

    for line in open(read_file, "r"):

        line = line.strip()
        if line[0:7] == "* 0 -1D":
            pass

        elif line[0:2] == "* ":
            if string != "" and line_features_list != []:
                phrase_temp_dic[string] = [line_features_list[1], line_features_list[2][0:-1]]
                string_list.append(string)
                string = ""
            line_features_list = line.split(" ")

        elif line[0:3] == "EOS":
            if string != "" and line_features_list != []:
                phrase_temp_dic[string] = [line_features_list[1], line_features_list[2][0:-1]]
                string_list.append(string)
                for string in string_list:
                    if "受賞者" in string:
                        for key, value_list in phrase_temp_dic.items():
                            if phrase_temp_dic[string][1] == value_list[0]:
                                print key
            phrase_temp_dic = {}
            string_list = []
            string = ""
            line_features_list = []

        else:
            string = string + line.split("\t")[0]

if __name__ == "__main__":
    skew_divergence(sys.argv[1])