#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys
from collections import defaultdict
import math

#まず全ての係り関係がわかっている辞書を作る。その辞書のキーにXやYがあるかどうかみてあったらXとYの頻度をその辞書からとってくるようにする
#その辞書のkeyは係っている文節の行頭の漢字連続(カタカナ連続とか)、valueには辞書が入っている。またそのvalueになっている辞書のkeyは係られている文節の行頭の漢字連続(カタカナ連続とか)、valueには係られている文節の行頭の漢字連続の頻度になっている
def extract_skew_divergence(cabocha_processed_file, csv_file):

    dependency_word_dic = defaultdict(dict)
    string = ""
    string_list = []
    line_features_temp_list = []
    phrase_temp_dic = {}

    for csv_line in open(csv_file, "r"):
        ans, X, Y = csv_line.strip().split(',')
        for line in open(cabocha_processed_file, "r"):

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
                        if X in string:
                            for key, value_list in phrase_temp_dic.items():
                                #phrase_temp_dicのvalueには係り受け解析の番号(listの一つ目の要素は0、二つ目は6Dみたいな感じ)が入っているので、
                                #ここで番号が一致しているかどうかみることで単語間の係り受け関係を見ている
                                if phrase_temp_dic[string][1] == value_list[0]:
                                    if key in dependency_word_dic[X]:
                                        dependency_word_dic[X][key] += 1
                                    else:
                                        dependency_word_dic[X][key] = 1

                                    if "all" in dependency_word_dic[X]:
                                        dependency_word_dic[X]["all"] += 1
                                    else:
                                        dependency_word_dic[X]["all"] = 1

                        if Y in string:
                            for key, value_list in phrase_temp_dic.items():
                                if phrase_temp_dic[string][1] == value_list[0]:
                                    if key in dependency_word_dic[Y]:
                                        dependency_word_dic[Y][key] += 1
                                    else:
                                        dependency_word_dic[Y][key] = 1

                                    if "all" in dependency_word_dic[Y]:
                                        dependency_word_dic[Y]["all"] += 1
                                    else:
                                        dependency_word_dic[Y]["all"] = 1

                phrase_temp_dic = {}
                string_list = []
                string = ""
                line_features_temp_list = []

            else:
                string = string + line.split("\t")[0]

    #dependency_word_dicはvalueに辞書を持つdefaultdictです
    return dependency_word_dic

if __name__ == "__main__":
    dependency_word_defaultdict_dic = extract_skew_divergence(sys.argv[1], sys.argv[2])
    for line in open(sys.argv[2], "r"):
        ans, X, Y = line.strip().split(',')
        all_skew_divergence = 0
        for dependency_word, dependency_word_value in dependency_word_defaultdict_dic[X].items():
            if dependency_word in dependency_word_defaultdict_dic[Y]:
                #ここでP(i)とQ(i)を計算する
                Pi = float(dependency_word_defaultdict_dic[X][dependency_word]) / float(dependency_word_defaultdict_dic[X]["all"])
                Qi = float(dependency_word_defaultdict_dic[Y][dependency_word]) / float(dependency_word_defaultdict_dic[Y]["all"])
                if Qi > 0:
                    one_of_skew_divergence = Pi * math.log(Pi / (0.99 * Qi + 0.01 * Pi))
                    all_skew_divergence += one_of_skew_divergence
        print "10:%s" % all_skew_divergence







