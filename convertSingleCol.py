#!/usr/bin/env python
# coding: utf-8
#
# Author: Peinan ZHANG
# Created at: 2014-12-08

from collections import defaultdict
import sys, pickle

id_of = {}
ids = 1000
for line in open(sys.argv[1]):
  line = line.strip()
  if line in id_of.keys():
    sys.stdout.write('%s:1\n' % (id_of[line]))
  else:
    ids += 1
    id_of[line] = ids
    sys.stdout.write('%s:1\n' % (id_of[line]))

# pickle.dump(id_of, open(sys.argv[2], 'w'))
