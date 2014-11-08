#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys,string,re

def main(read_file,write_file):
    wf = open(write_file,"w")
    for line in open(read_file,"r"):
        line = line.strip()
        if re.search('＼Ｓ１＼', line):
            wf.write("\n")
        elif re.search('^＼Ｔ２＼　(.+)', line):
        	#もうちょっとうまい書き方があると思う
        	wf.write("%s\n" % (re.search('^＼Ｔ２＼　(.+)', line).group(1)))
        elif re.search('^＼Ｔ２＼(.+)', line):
        	wf.write("%s\n" % (re.search('^＼Ｔ２＼(.+)', line).group(1)))
    wf.close()
    wf = open("mai98a_for_iikaehasseiritu.txt","w")
    for line in open(write_file,"r"):
        line = line.strip()
        if re.search('(.+。).', line):
            wf.write("%s\n" % (re.search('(.+。).', line).group(1)))
    wf.close()

if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2])
