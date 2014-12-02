#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys

def extract_sentence():

    keywords_list = []
    for ans, X, Y in open(sys.argv(1), "r"):
        keywords_list.append(X)
        keywords_list.append(Y)
    extracted_sentence_list = []

    for line in sys.stdin:
        for keyword in keywords_list:
            if keyword in line:
                extracted_sentence_list.append(line)
                break

    return extracted_sentence_list

if __name__ == "__main__":
    for line in extract_sentence():
        print line
