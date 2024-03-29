#!/usr/bin/env python
# coding: utf-8
# Author: Peinan ZHANG
# Created at: 2014-10-12

import sys, re
import math
from collections import defaultdict

X_value_dic_for_co_occur = defaultdict(int)
Y_value_dic_for_co_occur = defaultdict(int)
XY_value_dic_for_co_occur = defaultdict(int)

def mkFeatures(X, Y, featureIDs, refFileLines, N):
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
    elif 4 <= ID <= 5:
      feature_of[ID] = mkFeature_of[ID](X, Y, N)
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


def sqrChiOfXY(X, Y, N):
    n11 = 0
    n12 = 0
    n21 = 0
    n22 = 0
    kay_square = 0
    if X + Y in XY_value_dic_for_co_occur:
        n11 = XY_value_dic_for_co_occur[X + Y]
    if X in X_value_dic_for_co_occur:
        n12 = X_value_dic_for_co_occur[X] - n11
    if Y in Y_value_dic_for_co_occur:
        n21 = Y_value_dic_for_co_occur[Y] - n11
    n22 = N - n11 - n12 - n21
    kay_square = N * (n11 * n22 - n12 * n21) * (n11 * n22 - n12 * n21) / ((n11 + n12) * (n21 + n22) * (n11 + n21) * (n12 + n22))
    return kay_square

def logliklyhoodOfXY(X, Y, N):
    n11 = 0
    n12 = 0
    n21 = 0
    n22 = 0
    log_likelihood_ratio = 0
    if X + Y in XY_value_dic_for_co_occur:
        n11 = XY_value_dic_for_co_occur[X + Y]
    if X in X_value_dic_for_co_occur:
        n12 = X_value_dic_for_co_occur[X] - n11
    if Y in Y_value_dic_for_co_occur:
        n21 = Y_value_dic_for_co_occur[Y] - n11
    n22 = N - n11 - n12 - n21

    #対数尤度比を出すための式をそれぞれ書き出していく
    if n11 == 0:
        element11 = 0
    else:    
        element11 = n11 * (math.log(float(n11) / N, 2) - math.log(float(n11 + n12) * (n11 + n21) / (N * N), 2))
    
    if n12 == 0:
        element12 = 0
    else:    
        element12 = n12 * (math.log(float(n12) / N, 2) - math.log(float(n11 + n12) * (n12 + n22) / (N * N), 2))
    
    if n21 == 0:
        element21 = 0
    else:    
        element21 = n21 * (math.log(float(n21) / N, 2) - math.log(float(n21 + n22) * (n11 + n21) / (N * N), 2))
    
    if n22 == 0:
        element22 = 0
    else:    
        element22 = n22 * (math.log(float(n22) / N, 2) - math.log(float(n21 + n22) * (n12 + n22) / (N * N), 2))
    
    log_likelihood_ratio = 2 + 2 * (element11 + element12 + element21 + element22)
    return log_likelihood_ratio

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


#論文の日本語新聞記事からの略語抽出の素性の一つである言い換え発生率の素性を作るコードである
#paraphrase_csv_fileはcsv_file,newspaper_fileはtxt_fileを想定している
#この素性は本文ファイル(newspaper_file)に依存しているので、新聞記事から抽出した言い換えペアは新聞記事で、wikipediaから抽出した言い換えペアはwikipediaで対応させなければならないかもしれない
#for文を二重に回しているので修正したい
def chanceParaOfXY(X, Y, refFileLines):
  paraphrase = u"%s（%s）" % (X, Y)

  bunbo = 0
  bunshi = 0
  discover_paraphrase_flag = 0
  expression_X = 0
  expression_Y = 0
  expression_Y_flag = 0
  for line in refFileLines:
      #空白行があれば文書が変わったことを示すので分子の値を計算してからそれぞれのパラメータとフラグを初期化する
      if line == "\n":
          if discover_paraphrase_flag == 1 and expression_Y - expression_X > 0 and expression_Y_flag == 0:
              bunshi += 1
          discover_paraphrase_flag = 0
          expression_X = 0
          expression_Y = 0
          expression_Y_flag = 0
      #言い換え表現が出てくる後の文において表現Xと表現Yが何回出現するかどうか見ている。
      #文章単位で表現の数を数えている可能性(一文に2つ以上表現XやYが現れても＋1しかされない可能性)があるのでコードを変える必要があるかもしれない
      elif discover_paraphrase_flag == 1:
          if re.search(X, line):
              expression_X += 1
          if re.search(Y, line):
              expression_Y += 1
      #言い換え表現があれば言い換え表現フラグをたてて分母を1プラスする
      elif re.search(paraphrase, line):
          if not discover_paraphrase_flag == 1:
              bunbo += 1
              discover_paraphrase_flag = 1
      #言い換え表現が出てくる前の文において表現Yが出現するかどうか見ている。出てきたらフラグをたてる。
      elif discover_paraphrase_flag == 0:
          if re.search(Y, line):
              expression_Y_flag = 1

  if not bunbo == 0:
      #0以上1以下の値になるはずである
      return float(bunshi) / bunbo
  else:
            return 0


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

  #featureIDsは実際に作る素性を選択している
  #featureIDs = [1, 2, 3, 4, 5, 6, 8, 9, 11, 12]
  featureIDs = [12]
  list_8  = []
  list_9  = []
  list_10 = []
  list_11 = []

  #Nは言い換えの数を表す。対数尤度比による共起度の素性を出すときのパラメータに使う
  N = 0
  for line in open(sys.argv[1]):
    N += 1
    ans, X, Y = line.strip().decode('utf-8').split(',')
    X_value_dic_for_co_occur[X] += 1
    Y_value_dic_for_co_occur[Y] += 1
    XY_value_dic_for_co_occur[X + Y] += 1

  for line in open(sys.argv[1]): # CSV file: ans, X, Y
    # print line
    ans, X, Y = line.strip().decode('utf-8').split(',')
    feature_of = mkFeatures(X, Y, featureIDs, refFileLines, N)

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
