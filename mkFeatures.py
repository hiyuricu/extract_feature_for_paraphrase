#!/usr/bin/env python
# coding: utf-8
#
# Author: Peinan ZHANG
# Created at: 2014-10-12

import sys, re

def mkFeatures(X, Y, featureIDs, refFileLines):
  feature_of = {}
  mkFeature_of = {
      1: countOfXY,
      2: countOfX,
      3: countOfY,
      4: sqrChiOfXY,
      5: logliklyhoodOfXY,
      6: containingOfXY,
      7: SDivOfXY,
      8: caboCha2OfXY,
      9: caboCha1OfXY,
      10:caboChaLastOfXY,
      11:strTypeOfXY,
      12:chanceParaOfXY
    }

  for ID in featureIDs:
    if 8 <= ID <= 11:
      feature_of[ID] = mkFeature_of[ID](X, Y, eval('list_' + str(ID)))
    else:
      feature_of[ID] = mkFeature_of[ID](X, Y, refFileLines)
    # print feature_of[ID]

  return feature_of


def countOfXY(X, Y, refFileLines):
  count = 0
  for line in refFileLines:
    count += line.count(u'%s(%s)' % (X, Y))
    count += line.count(u'%s（%s）' % (X, Y))
  
  # print count
  return str(count)


def countOfX(X, Y, refFileLines):
  count = 0
  for line in refFileLines:
    count += line.count(u'%s' % X)
  
  # print count
  return str(count)


def countOfY(X, Y, refFileLines):
  count = 0
  for line in refFileLines:
    count += line.count(u'%s' % Y)

  # print count
  return str(count)


def sqrChiOfXY(X, Y, refFileLines):
  pass


def logliklyhoodOfXY(X, Y, refFileLines):
  pass


def containingOfXY(X, Y, refFileLines):
  for x in X:
    if x not in Y: return '0'
  return '1'


def SDivOfXY(X, Y, refFileLines):
  pass


def caboCha2OfXY(X, Y, list_8):
  result_str = '%s/%s' % (caboChaProc(X, 1), caboChaProc(Y, 1))
  # print '%s/%s' % (caboChaProc(X, 1), caboChaProc(Y, 1))
  return encode_to_id(result_str, list_8)


def caboCha1OfXY(X, Y, list_9):
  result_str = '%s/%s' % (caboChaProc(X, 2), caboChaProc(Y, 2))
  # print '%s/%s' % (caboChaProc(X, 2), caboChaProc(Y, 2))
  return encode_to_id(result_str, list_9)


def caboChaLastOfXY(X, Y, list_10):
  pass


def strTypeOfXY(X, Y, list_11):
  re_kanji = re.compile(ur'[一-龠]')
  re_hira  = re.compile(ur'[ぁ-ゞ]')
  re_kata  = re.compile(ur'[ァ-ヾ]')
  re_alpha = re.compile(ur'[a-zA-Z_ａ-ｚＡ-Ｚ]')
  re_num   = re.compile(r'[0-9]')
  rexp_of = {
      'kanji': re_kanji,
      'hira' : re_hira,
      'kata' : re_kata,
      'alpha': re_alpha,
      'num'  : re_num
      }

  def matchType(text):
    for strType, rexp in rexp_of.items():
      if rexp.match(text[-1]): return strType
    return None

  result_str = '%s/%s' % (matchType(X), matchType(Y))
  # print '%s/%s' % (matchType(X), matchType(Y))
  return encode_to_id(result_str, list_11)


def chanceParaOfXY(X, Y, refFileLines):
  pass


def caboChaProc(text, mode):
  import CaboCha
  c = CaboCha.Parser()
  text = text.encode('utf-8')
  tree = c.parse(text)
  f1_result = tree.toString(CaboCha.FORMAT_LATTICE)
  lastRow   = f1_result.strip().split('\n')[-2]
  fields = lastRow.split('\t')[1].split(',')

  if mode == 1: return fields[1]
  if mode == 2: return fields[0]


def encode_to_id(result_str, idlist):
  # print result_str, idlist
  if result_str not in idlist:
    idlist.append(result_str)
  # print idlist, idlist.index(result_str)
  return str(idlist.index(result_str))


if __name__ == '__main__':
  # load article file
  refFileLines = open(sys.argv[2]).readlines()
  for i in range(len(refFileLines)):
    refFileLines[i] = refFileLines[i].decode('utf-8')

  featureIDs = [1, 2, 3, 6, 8, 9, 11]
  list_8  = []
  list_9  = []
  list_10 = []
  list_11 = []
  for line in open(sys.argv[1]): # CSV file: ans, X, Y
    # print line
    ans, X, Y = line.strip().decode('utf-8').split(',')
    feature_of = mkFeatures(X, Y, featureIDs, refFileLines)

    sys.stdout.write('%s\t' % ans.encode('utf-8'))
    if len(featureIDs) != 1:
      for i in range(len(featureIDs) - 1):
        sys.stdout.write('%d:%s\t' % (featureIDs[i], feature_of[featureIDs[i]]))
    sys.stdout.write('%d:%s\n' % (featureIDs[-1], feature_of[featureIDs[-1]])) 

  with open('ID8.txt', 'w') as id8:
    for id, text in enumerate(list_8):
      id8.write('%d\t%s\n' % (id, text))
  with open('ID9.txt', 'w') as id9:
    for id, text in enumerate(list_9):
      id9.write('%d\t%s\n' % (id, text))
  with open('ID11.txt', 'w') as id11:
    for id, text in enumerate(list_11):
      id11.write('%d\t%s\n' % (id, text))
