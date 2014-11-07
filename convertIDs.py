#!/usr/bin/env python
# coding: utf-8
#
# Author: Peinan ZHANG
# Created at: 2014-10-22

import sys

def readLine(line):
  featureDict = {}
  items = line.strip().split('\t')
  featureDict[0] = items[0]
  for item in items[1:]:
    featureID, content = item.split(':')
    featureDict[int(featureID)] = int(content)

  return featureDict


def convertWrite(featureDict, convertIDs):
  writeLine = ''
  for k, v in sorted(featureDict.items()):
    if k == 8:
      writeLine += '%d:%d\t' % (v + 100, 1)
    elif k == 9:
      writeLine += '%d:%d\t' % (v + 1000, 1)
    elif k == 11:
      writeLine += '%d:%d\t' % (v + 10000, 1)
    elif k == 0:
      writeLine += '%s\t' % v
    else:
      writeLine += '%d:%d\t' % (k, v)
  sys.stdout.write(writeLine[:-1] + '\n')


if __name__ == '__main__':
  convertIDs = [8, 9, 11]

  # convert feature file
  for line in open(sys.argv[1]):
    convertWrite(readLine(line), convertIDs)
  # convert id files
  for ID in convertIDs:
    idFilename = 'ID%s.txt' % ID
    idFilename_prc = idFilename + '.prc'
    with open(idFilename_prc, 'w') as idfile:
      for line in open(idFilename):
        id_before, content = line.split('\t')
        if ID == 8:
          idfile.write('%d\t%s' % (int(id_before) + 100, content))
        elif ID == 9:
          idfile.write('%d\t%s' % (int(id_before) + 1000, content))
        elif ID == 11:
          idfile.write('%d\t%s' % (int(id_before) + 10000, content))
