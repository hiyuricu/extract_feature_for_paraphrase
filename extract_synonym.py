#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import defaultdict
import sys, string, re, MeCab

abbreviation_dic = defaultdict(lambda: 0)

#入力として一文(。がくると改行されている文)一行となっているテキストが引数にあると想定している
def main():
    output_abbreviation(sys.argv[1])
    for key, value in sentence_wakati().items():
        print "%s,%s" % (key, value)

#略語と略語を含む文を出力する関数
def output_abbreviation(read_file):
    wf = open('abbreviation_and_sentence.txt',"w")
    for line in open(read_file,"r"):
        line = line.strip()
        for abb in re.finditer(r'(.+?)\((.+?)\)', line):
            wf.write("%s\t%s\n" % (abb.group(1), abb.group(2)))

        #大文字の括弧表現に対応している
        for abb in re.finditer(r'(.+?)（(.+?)）', line):
            wf.write("%s\t%s\n" % (abb.group(1), abb.group(2)))

    wf.close()

#文章を分かち書きする関数
def sentence_wakati():
    tagger = MeCab.Tagger('-Ochasen')
    for line in open('abbreviation_and_sentence.txt',"r"):
        perfect_sentence = ""
        tango_list = []
        temp_list = line.strip().split()
        #完全文候補の文が空でないかどうか見ている
        if len(temp_list) == 2:
            # print "----------------------------------------------------------------------------------------"
            # print line
            node = tagger.parseToNode(temp_list[0])
            while node:
                tango = "%s,%s" % (node.surface, node.feature.split(",")[0])
                tango_list.append(tango)
                node = node.next
            tango_list.reverse()
            for tango_comma in tango_list[1:-1]:
                # print tango_comma
                if tango_comma.strip().split(",")[0] == "」":
                    pass
                elif tango_comma.strip().split(",")[1] != "名詞" and tango_comma.strip().split(",")[1] != "接頭詞":
                    break
                else:
                    perfect_sentence = tango_comma.strip().split(",")[0] + perfect_sentence
        if perfect_sentence != "":
            key_string = "%s,%s" % (perfect_sentence, temp_list[1])
            # print key_string
            abbreviation_dic[key_string] += 1

    return abbreviation_dic

if __name__ == "__main__":
    main()
