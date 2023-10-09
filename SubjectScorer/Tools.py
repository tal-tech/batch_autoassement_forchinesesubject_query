#!/usr/bin/env python
# coding=utf-8
import numpy as np
import os
import re
from Thesaurus import Thesaurus

class Tools():

    def Init(self, cLogger):
        self.cLogger = cLogger
        return 0

    def IsChn(self, c):
        return '\u4e00' <= c <= '\u9fa5'

    def HasChn(self, c):
        for i in c:
            if u'\u4e00' <= i <= u'\u9fff':
                return True
        return False

    def NormCosin(self, vec1, vec2):
        """ bigger better"""
        v1 = np.array(vec1)
        v2 = np.array(vec2)
        num = sum(v1 * v2)
        denom = np.linalg.norm(v1) * np.linalg.norm(v2)
        if denom == 0:
            return 0.0
        cos = num / denom  # 余弦值
        sim = 0.5 + 0.5 * cos  # 归一化
        return sim


    def NormEuclidean(self, vec1, vec2):
        """bigger better"""
        A = np.array(vec1)
        B = np.array(vec2)
        dist = np.linalg.norm(A - B)
        sim = 1.0 / (1.0 + dist)  # 归一化
        return sim


    #关键词加载
    def LoadKeyWords(self, params):
        """
        关键词1-k扩展词1-k扩展词2：周围词1-v扩展词1-v扩展词2 / 周围词2 | 关键词2 | 关键词3 ### 关键词2-1...
        :return:
        """
        if len(params) != 2:
            self.cLogger.error("LoadKeyWords's param num is not equal to 2")
            return -1, []
        key_words, cThesaurus = params
        self.cLogger.info("key_words str is: %s" % (key_words))
        vKeyArounds = [] #存储多套 关键词、周围词
        vKeyTaos = key_words.split("###")
        i = 0
        for sKeyAround in vKeyTaos: #对于每套关键词
            mKeyAround = {}
            vK, vA = [], []
            vKeyOnes = sKeyAround.split("|")
            for sKA in vKeyOnes: #对于每个关键词
                if "：" in sKA:#包含周围词
                    sKOne, sAOne = sKA.split("：") #对每个关键词：关键词、周围词
                    vKOne = [x.strip() for x in sKOne.split("-") if x.strip() != ""]
                    vAOne = [x.strip() for x in list(re.split("-|/", sAOne)) if x.strip() != ""]
                    vKSimWords = []
                    for sWord in vKOne:
                        setWords = cThesaurus.FindThesaurusAll(sWord)
                        vKSimWords.extend(setWords)
                    vASimWords = []
                    for sWord in vAOne:
                        setWords = cThesaurus.FindThesaurusAll(sWord)
                        vASimWords.extend(setWords)

                    vK.extend(vKOne)
                    vK.extend(vKSimWords)
                    vA.extend(vAOne)
                    vA.extend(vASimWords)
                else:#不包含周围词
                    vKOne = [x.strip() for x in sKA.split("-") if x.strip() != ""]
                    vKSimWords = []
                    for sWord in vKOne:
                        setWords = cThesaurus.FindThesaurusAll(sWord)
                        vKSimWords.extend(setWords)
                    vK.extend(vKOne)
                    vK.extend(vKSimWords)
            vK = list(set(vK))
            vA = list(set(vA))
            for k in vK:
                mKeyAround[k] = vA
            vKeyArounds.append(mKeyAround)

            self.cLogger.info("the %d center around words, all: %d!" % (i, len(vKeyTaos)))
            for k, v in mKeyAround.items():
                self.cLogger.info("loaded center word:%s" % k)
                self.cLogger.info("loaded around words:%s" % "|".join(v))
            i += 1
        return 0, vKeyArounds

    # 关键词抽取
    def ExtractKeywords(self, params):
        """
        vTags->technical&emotion&a&v&i&n&ns&nh&nd&ni&nl&nt   z d r
        """
        key_around_distance = 50
        (words, postags, cThesaurus, spec_words, emotion_words, vTags, word_vecs, distance) = params
        if len(params) != 8:
            self.cLogger.error("ExtractKeywords params is not equal to 8")
            return -1, {}
        key_words = []  # (index, words[i], thesarus_words)
        if len(words) != len(postags):
            self.cLogger.error("words num:%d not equal to postags:%d" % (len(words), len(postags)))
            return -1, {}
        for i in range(len(words)):
            if len(words[i]) == 0 or not self.IsChn(words[i]):
                continue
            simi_words = []
            setThesauWords = cThesaurus.FindThesaurusAll(words[i])
            # log
            sSetThesaurus = "|".join(setThesauWords)
            self.cLogger.info("keyword:%s -> thesarus words: %s" % (words[i], sSetThesaurus))
            
            simi_words.extend(setThesauWords)

            if words[i] in spec_words or words[i] in emotion_words or postags[i] in vTags:
                if words[i].strip() != "":

                    itm = (i, words[i], simi_words)
                    key_words.append(itm)
        #
        mKeyAround = {}  # keyword-> around words
        for itm in key_words:
            (index, keyword, simi_keywords) = itm
            arounds = []
            # from index to left
            distance = 0
            if len(keyword) < 2 and not self.IsChn(keyword):
                continue
            for l in range(index - 1, -1, -1):
                if distance > key_around_distance:
                    break

                distance += 1
                if self.IsAround(words[l], postags[l]) and len(words[l]) > 1 and words[l] != keyword:
                    self.cLogger.info("%s's left arounds:%s" % (keyword, words[l]))

                    simi_words = []
                    setLeftWords = cThesaurus.FindThesaurusAll(words[l])
                    simi_words.extend(setLeftWords)
                    self.cLogger.info("left words: %s -> thesaurus words: %s" % (words[l], "|".join(setLeftWords)))

                    arounds.extend(simi_words)
                    arounds.append(words[l])
            distance = 0
            for r in range(index + 1, len(words), 1):
                if distance > key_around_distance:
                    break
                if words[r] == keyword:
                    continue
                distance += 1
                if self.IsAround(words[r], postags[r]) and len(words[r]) > 1and words[r] != keyword:
                    self.cLogger.info("%s's right arounds:%s" % (keyword, words[r]))
                    simi_words = []
                    setRightWords = cThesaurus.FindThesaurusAll(words[r])
                    simi_words.extend(setRightWords)
                    self.cLogger.info("right words: %s -> thesaurus words: %s" % (words[r], "|".join(setRightWords)))
                    arounds.extend(simi_words)
                    arounds.append(words[r])
            tmp = arounds
            arounds = sorted(set(arounds),key=tmp.index)
            arounds = [x for x in arounds if x != keyword and x != ""]
            keywords = [keyword] + simi_keywords
            tmp1 = keywords
            keywords = sorted(set(keywords),key=tmp1.index)
            tmp2 = arounds
            arounds = sorted(set(arounds),key=tmp2.index)

            for kw in keywords:
                if kw == "":
                    continue
                mKeyAround[kw] = arounds
        for k, v in mKeyAround.items():
            self.cLogger.info("extracted center word:%s" % k)
            self.cLogger.info("extracted around words:%s" % "|".join(v))
        return 0, mKeyAround


    def IsAround(self, cand_word, cand_pos):
        vUsePos = ["a", "v", "i", "n", "ns", "nh", "nd", "ni", "nl", "nt", "nz", "r", "z", "d"]
        #    vTags->technical&emotion&a&v&i&n&ns&nh&nd&ni&nl&nt   z d r
        if cand_pos in vUsePos and len(cand_word) > 1:  # 至少一个字，c++这里是3(utf-8)
            return True
        return False


    def RemoveDuplicates(self, point_segs, point_tags):
        """对每个采分点建立该采分点对应的其他采分点的字符的集合"""
        if len(point_segs) != len(point_tags):
            self.cLogger.error("point_seg num not equal to point_tag num!")
            return -1, []
        for i in range(len(point_segs)):
            #print(i)
            if len(point_segs[i]) != len(point_tags[i]):
                self.cLogger.error("the :%d th point_segs's length=%d not equal to :%d th point_tags's length=%d" % (i, i, len(point_segs[i], len(point_tags[i]))))
                self.cLogger.error("point_segs[%d]: %s" % (i, " ".join(point_segs[i])))
                self.cLogger.error("point_tags[%d]: %s" % (i, " ".join(point_tags[i])))
                return -1, []
        mCharSets = {}
        for i, p in enumerate(point_segs):
            vOtherPoints = point_segs[:i] + point_segs[i + 1:]
            vOther = []
            for p in vOtherPoints:
                vOther.extend(p)
            mCharSets[i] = set(vOther)
        vRemovedPoints, vRemovedTags = [], []
        for i in range(len(point_segs)):
            vSegs, vTags = [], []
            for j in range(len(point_segs[i])):
                if point_segs[i][j] not in mCharSets[i]:
                    vSegs.append(point_segs[i][j])
                    vTags.append(point_tags[i][j])
            #tmp = [point_segs[i][j] for j in range(len(point_segs[i])) if point_tags[i][j] not in mCharSets[i]]
            vRemovedPoints.append(vSegs)
            vRemovedTags.append(vTags)
            if len(vSegs) != len(vTags):
                self.cLogger.error("RemoveDuplicates error for :%d th point segs and tags" % (i))
                self.cLogger.error("removed point_segs[%d]: %s" % (i, " ".join(vSegs)))
                self.cLogger.error("removed point_tags[%d]: %s" % (i, " ".join(vTags)))
                return -1, []
        return 0, [vRemovedPoints, vRemovedTags]
