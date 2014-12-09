#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys
from collections import defaultdict
import math

#まず全ての係り関係がわかっている辞書を作る。その辞書のキーにXやYがあるかどうかみてあったらXとYの頻度をその辞書からとってくるようにする
#その辞書のkeyは係っている文節の行頭の品詞連続(名詞連続とか)、valueには辞書が入っている。またそのvalueになっている辞書のkeyは係られている文節の行頭の品詞連続(名詞連続とか)、valueには係られている文節の行頭の品詞連続の頻度になっている
def extract_skew_divergence(cabocha_processed_file):

    dependency_word_dic = defaultdict(lambda: defaultdict(int))
    phrase_temp_dic = {} #keyがown_number、valueはbeginning_of_line_sentenceとdependency_numberのリストにする
    own_number = 0
    dependency_number = 0
    beginning_of_line_flag = 0
    beginning_of_line_sentence = ""
    temporary_beginning_of_line_sentence = ""
    temporary_a_part_of_speech_info = ""

    for line in open(cabocha_processed_file, "r"):

        line = line.strip()
        if line[0:7] == "* 0 -1D":
            pass

        elif line[0:2] == "* ":
            if beginning_of_line_sentence != "":
                phrase_temp_dic[own_number] = [beginning_of_line_sentence, dependency_number]
            own_number = line.split()[1]
            if line.split()[2][0] == "-":
                dependency_number = "null"
            else:
                dependency_number = line.split()[2][:-1]

            #ここで初期化を行っている
            beginning_of_line_flag = 1
            temporary_beginning_of_line_sentence = ""
            beginning_of_line_sentence = ""

        elif line[0:3] == "EOS":
            if beginning_of_line_sentence != "":
                phrase_temp_dic[own_number] = [beginning_of_line_sentence, dependency_number]

                #ここでphrase_temp_dicからdependency_word_dicを作る
                for key, value_list in phrase_temp_dic.items():
                    if value_list[1] != "null":
                        # print key, value_list[1]
                        # phrase_temp_dic[value_list[1]][0]は係り先の単語を示している
                        dependency_word_dic[value_list[0]][phrase_temp_dic[value_list[1]][0]] += 1
                        dependency_word_dic[value_list[0]]["all"] += 1

            beginning_of_line_sentence = ""

        else:
            if beginning_of_line_flag == 1 and temporary_beginning_of_line_sentence == "":#行頭の時
                temporary_beginning_of_line_sentence = line.split()[0]
                temporary_a_part_of_speech_info = line.split()[1].split(",")[0]
                beginning_of_line_sentence = temporary_beginning_of_line_sentence
            elif beginning_of_line_flag == 1 and temporary_beginning_of_line_sentence != "":#行頭から品詞が継続しているか見る所
                if temporary_a_part_of_speech_info == line.split()[1].split(",")[0]:
                    temporary_beginning_of_line_sentence = temporary_beginning_of_line_sentence + line.split()[0]
                    beginning_of_line_sentence = temporary_beginning_of_line_sentence
                else:#行頭から品詞が継続していなかった後の場合
                    beginning_of_line_sentence = temporary_beginning_of_line_sentence
                    beginning_of_line_flag = 0

    #dependency_word_dicは辞書でvalueに辞書を持ち、その辞書のvalueはintになっているdefaultdictです
    return dependency_word_dic

if __name__ == "__main__":
    dependency_word_dic = extract_skew_divergence(sys.argv[1])
    for line in open(sys.argv[2], "r"):
        ans, X, Y = line.strip().split(',')
        all_skew_divergence = 0
        if X in dependency_word_dic:
            print "-------------------------------------------------------------------"
            print X
            #dependency_wordがP(i)やQ(i)のi(係られている単語)のことである
            for dependency_word, dependency_word_value in dependency_word_dic[X].items():
                print dependency_word,dependency_word_value
                if dependency_word != "all":
                    Pi = float(dependency_word_dic[X][dependency_word]) / float(dependency_word_dic[X]["all"])
                    print "Pi:%s" % Pi
                    if Y in dependency_word_dic and dependency_word in dependency_word_dic[Y]:
                        Qi = float(dependency_word_dic[Y][dependency_word]) / float(dependency_word_dic[Y]["all"])
                    else:
                        Qi = 0
                    one_of_skew_divergence = Pi * math.log(Pi / (0.99 * Qi + 0.01 * Pi))
                    print one_of_skew_divergence
                    all_skew_divergence += one_of_skew_divergence
            print all_skew_divergence
        # print "10:%s" % all_skew_divergence


















































