#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys
from collections import defaultdict

def skew_divergence(read_file):

    string = ""
    line_features_list = []
    phrase_dic = {}

    for line in open(read_file, "r"):

        line = line.strip()

        if line[0:7] == "* 0 -1D":
            pass

        elif line[0:2] == "* ":
            if string != "" and line_features_list != []:
                print string
                phrase_dic[string] = [line_features_list[1], line_features_list[2][0:-1]]
                string = ""
            line_features_list = line.split(" ")

        elif line[0:3] == "EOS":
            if string != "" and line_features_list != []:
                print string
                print 
                phrase_dic[string] = [line_features_list[1], line_features_list[2][0:-1]]
            # phrase_dic = {}
            string = ""
            line_features_list = []

        else:
            string = string + line.split("\t")[0]

    return phrase_dic

if __name__ == "__main__":
    for k,v in skew_divergence(sys.argv[1]).items():
        print k,v,v[0]