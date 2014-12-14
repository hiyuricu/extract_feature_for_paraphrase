#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys

def change_field():

    temp_feature = ""

    for line in open(sys.argv[1], "r"):
        feature_list = line.strip().split()
        for feature in feature_list:
            if feature[0:2] == "12":
                temp_feature = "600" + feature[2:]
            elif feature[0:2] == "15":
                temp_feature = "700" + feature[2:]
            else:
                print feature,
        print temp_feature

if __name__ == "__main__":
    change_field()
