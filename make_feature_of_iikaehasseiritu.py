#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys,string,re

#論文の日本語新聞記事からの略語抽出の素性の一つである言い換え発生率の素性を作るコードである
#paraphrase_csv_fileはcsv_file,newspaper_fileはtxt_fileを想定している
#この素性は本文ファイル(newspaper_file)に依存しているので、新聞記事から抽出した言い換えペアは新聞記事で、wikipediaから抽出した言い換えペアはwikipediaで対応させなければならないかもしれない
#for文を二重に回しているので修正したい
def main(paraphrase_csv_file,newspaper_file):
    wf = open("feature_of_iikaehasseiritu.txt","w")
    for line in open(paraphrase_csv_file,"r"):
        line = line.strip()
        csv_list = line.split(",")
        #毎日新聞においては括弧は全角で扱われている
        paraphrase = "%s（%s）" % (csv_list[1], csv_list[2])

        bunbo = 0
        bunshi = 0
        discover_paraphrase_flag = 0
        expression_X = 0
        expression_Y = 0
        expression_Y_flag = 0
        print paraphrase
        for line in open(newspaper_file,"r"):
            #空白行があれば文書が変わったことを示すので分子の値を計算してからそれぞれのパラメータとフラグを初期化する
            if line == "":
                if discover_paraphrase_flag == 1 and expression_Y - expression_X > 0 and expression_Y_flag == 0:
                    bunshi += 1
                discover_paraphrase_flag = 0
                expression_X = 0
                expression_Y = 0
                expression_Y_flag = 0
            #言い換え表現が出てくる後の文において表現Xと表現Yが何回出現するかどうか見ている。
            #文章単位で表現の数を数えている可能性(一文に2つ以上表現XやYが現れても＋1しかされない可能性)があるのでコードを変える必要があるかもしれない
            elif discover_paraphrase_flag == 1:
                if re.search(csv_list[1], line):
                    expression_X += 1
                if re.search(csv_list[2], line):
                    expression_Y += 1
            #言い換え表現があれば言い換え表現フラグをたてて分母を1プラスする
            elif re.search(paraphrase, line):
                if not discover_paraphrase_flag == 1:
                    bunbo += 1
                    discover_paraphrase_flag = 1
            #言い換え表現が出てくる前の文において表現Yが出現するかどうか見ている。出てきたらフラグをたてる。
            elif discover_paraphrase_flag == 0:
                if re.search(csv_list[2], line):
                    expression_Y_flag = 1

        if not bunbo == 0:
            #0以上1以下の値になるはずである
            print float(bunshi) / bunbo
        else:
            print 0
    wf.close()

if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2])