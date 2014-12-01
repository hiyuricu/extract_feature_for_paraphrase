#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys
from collections import defaultdict
import math

def extract_NE_feature():

    NE_list = []
    temp_NE = ""

    for line in sys.stdin:
        if line[0:3] == "EOS":
            NE_list.append(temp_NE)

        elif line[0:2] == "* ":
            pass

        else:
            word,word_element_list,NE = line.strip().split("\t")
            if len(NE) > 1:
                temp_NE = NE[2:]
            else:
                temp_NE = NE

    return NE_list

if __name__ == "__main__":
    for NE in extract_NE_feature():
        print NE
