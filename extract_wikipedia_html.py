#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2, time, sys, jctconv, os.path

#wikipediaのhtmlをクロールします
f1 = open("error_url", "w")
i = 0

for abb_pair_list in open(sys.argv[1], "r"):
    i += 1
    #入力するcsvファイルによってtarget_titleが何番目のフィールドを参照するか変わるので毎回添字をかえる必要がある
    target_title = abb_pair_list.strip().split(",")[0].decode("utf-8")
    target_title2 = jctconv.z2h(target_title, kana=False, digit=True, ascii=True)
    target_title3 = target_title2.encode("utf-8")
    write_text = "wikipedia_html_synonym/%s.txt" % target_title
    if not os.path.exists(write_text):
        print i
        f = open(write_text, "w")
        url_text = "http://ja.wikipedia.org/wiki/%s" % target_title3
        try:
            url = urllib2.urlopen(url_text).read()
        except:
            f1.write(url_text)
            continue
        f.write(url)
        f.close()
        time.sleep(10.0)

f1.close()


f2 = open("error_url2", "w")
i = 0

for abb_pair_list in open(sys.argv[1], "r"):
    i += 1
    #入力するcsvファイルによってtarget_titleが何番目のフィールドを参照するか変わるので毎回添字をかえる必要がある
    target_title = abb_pair_list.strip().split(",")[1].decode("utf-8")
    target_title2 = jctconv.z2h(target_title, kana=False, digit=True, ascii=True)
    target_title3 = target_title2.encode("utf-8")
    write_text = "wikipedia_html_synonym/%s.txt" % target_title
    if not os.path.exists(write_text):
        print i
        f = open(write_text, "w")
        url_text = "http://ja.wikipedia.org/wiki/%s" % target_title3
        try:
            url = urllib2.urlopen(url_text).read()
        except:
            f1.write(url_text)
            continue
        f.write(url)
        f.close()
        time.sleep(10.0)

f2.close()


