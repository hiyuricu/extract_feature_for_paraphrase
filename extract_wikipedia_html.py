#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2, time, sys, jctconv, pickle

#wikipediaのhtmlをクロールします
i = 0
f = open("synonym_dict.txt")
f2 = open("synonym_dict2.txt", "w")
synonym_dict = pickle.load(f)

for abb_pair_list in open(sys.argv[1], "r"):
    i += 1
    #入力するcsvファイルによってtarget_titleが何番目のフィールドを参照するか変わるので毎回添字をかえる必要がある
    target_title_decode = abb_pair_list.strip().split(",")[0].decode("utf-8")
    target_title_encode = jctconv.z2h(target_title_decode, kana=False, digit=True, ascii=True).encode("utf-8")
    if not target_title_encode in synonym_dict:
        print i
        url_text = "http://ja.wikipedia.org/wiki/%s" % target_title_encode
        try:
            url_html = urllib2.urlopen(url_text).read()
            synonym_dict[target_title_encode] = url_html
            time.sleep(10.0)
        except:
            time.sleep(10.0)
            continue

pickle.dump(synonym_dict, f2)
f.close()
f2.close()