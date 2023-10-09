import joblib

class RF():
    def Init(self, params):
        cLogger, cFileLoader, cTool = params
        self.m_cModel = cFileLoader.m_cRFModel_
        self.m_setEmotWords_ = cFileLoader.m_setEmotWords_
        self.m_mWordVectors_ = cFileLoader.m_mWordVectors_
        self.m_setSpecWords_ = cFileLoader.m_setSpecWords_
        self.m_mSimDict_ = cFileLoader.m_mSimDict_
        self.cTool = cTool
        self.cLogger = cLogger
        return 0
    def GetX(self, right_text, user_text, right_segs, right_tags, user_segs, user_tags):
        X = []
        # self.cLogger.debug("right text: %s" % right_text)
        # self.cLogger.debug("user text: %s" % user_text)
        # self.cLogger.debug("right_segs: %s" %  " ".join(right_segs))
        # self.cLogger.debug("user_segs: %s" % " ".join(user_segs))

        sRightSeg, sUserSeg = " ".join(right_segs), " ".join(user_segs)
        # 0
        X.extend(self.CharEqualFeature(sRightSeg, sUserSeg))
        # 1
        X.extend(self.WordEqualFeature(right_segs, user_segs))
        # 2
        X.extend(self.SpecialWordsFeature(right_segs, user_segs))
        # 3 4 5 6 7
        X.extend(self.WordSimFeature(right_segs, user_segs, self.cTool.NormCosin))
        # 8 9 10 11 12
        X.extend(self.WordSimFeature(right_segs, user_segs, self.cTool.NormEuclidean))
        # 13
        X.extend(self.SentSimFeature(right_segs, user_segs, self.cTool.NormCosin))
        # 14
        X.extend(self.SentSimFeature(right_segs, user_segs, self.cTool.NormEuclidean))
        # 15
        X.extend(self.EmotionWordsFeature(right_segs, user_segs))
        # 16
        X.extend(self.SimNetFeature(right_segs, user_segs))
        if len(X) != 17:
            self.cLogger.error("rf features not equal to 17")
            return -1, X
        # log
        # self.cLogger.debug("rf input :")
        # for i in range(len(X)):
        #     self.cLogger.debug("X[%d]: %f" % (i, X[i]))
        return 0, X

    def SpecialWordsFeature(self, right_segs, user_segs):
        """get technical/emotion word feature from comparing user and right"""
        count = 0
        for seg in user_segs:
            if seg in self.m_setSpecWords_ and seg in right_segs:
                count += 1
        if len(right_segs) == 0:
            return [0.0]
        return [float(count) / len(right_segs)]


    def EmotionWordsFeature(self, right_segs, user_segs):
        """get technical/emotion word feature from comparing user and right"""
        count = 0
        for seg in user_segs:
            if seg in self.m_setEmotWords_ and seg in right_segs:
                count += 1
        if len(right_segs) == 0:
            return [0.0]
        return [float(count) / len(right_segs)]


    def WordEqualFeature(self, right_segs, user_segs):# to be altered , to judge if seg is chn
        """the equal rate of user text and right text"""
        count = 0
        for seg in user_segs:
            if seg in right_segs:
                count += 1
        if not right_segs:
            return [0.0]
        return [count / len(right_segs) * 1.0]


    def CharEqualFeature(self, right_text, user_text):
        all_len, equal = 0, 0
        for c in right_text:
            if self.cTool.IsChn(c):
                all_len += 1
        for c in user_text:
            if self.cTool.IsChn(c) and c in right_text:
                equal += 1
        if not all_len:
            return [0.0]
        return [equal / all_len * 1.0]


    def WordSimFeature(self, right_segs, user_segs, distance):
        """
        cal 5 higgest vector distance of word pairs between right and user
        :param right_segs:
        :param user_segs:
        :return: the most sim rate of three pairs word
        """
        user_vecs = []
        right_vecs = []
        right_words = []
        user_words = []
        for seg in user_segs:
            if seg.isspace():
                continue
            if seg in self.m_mWordVectors_:
                vSegVec = self.m_mWordVectors_[seg]
                # vSegVec = m_mWordVectors_[seg]
                user_vecs.append(vSegVec)
                user_words.append(seg)
        for seg in right_segs:
            if seg.isspace():
                continue
            if seg in self.m_mWordVectors_:
                vSegVec = self.m_mWordVectors_[seg]
                # vSegVec = m_mWordVectors_[seg]
                right_vecs.append(vSegVec)
                right_words.append(seg)
        sims = []
        for i in range(len(user_vecs)):
            for j in range(len(right_vecs)):
                tmp = distance(user_vecs[i], right_vecs[j])
                sims.append(tmp)
                # self.cLogger.info("user:%s, right:%s, sim:%f" % (user_words[i], right_words[j], tmp))
        sims.sort(reverse=True)
        # 不足5对，补0
        if len(sims) < 5:
            for i in range(5 - len(sims)):
                sims.append(0.0)
        return sims[0:5]


    def SentSimFeature(self, right_segs, user_segs, distance):
        """euclidean  cosin"""
        dim = len(list(self.m_mWordVectors_.values())[0])
        vUserSentVec = [0 for _ in range(dim)]
        vRightSentVec = [0 for _ in range(dim)]
        vSegVec = [0 for _ in range(dim)]
        for seg in user_segs:
            if seg.isspace():
                continue
            if seg in self.m_mWordVectors_:
                vSegVec = self.m_mWordVectors_[seg]
                vUserSentVec = [vUserSentVec[k] + vSegVec[k] for k in range(len(vUserSentVec))]
        for seg in right_segs:
            if seg.isspace():
                continue
            if seg in self.m_mWordVectors_:
                vSegVec = self.m_mWordVectors_[seg]
                vRightSentVec = [vRightSentVec[k] + vSegVec[k] for k in range(len(vRightSentVec))]
        score = distance(vRightSentVec, vUserSentVec)
        return [score]


    def SimNetFeature(self, right_segs, user_segs):
        key = (" ".join(right_segs), " ".join(user_segs))
        if key in self.m_mSimDict_:
            return [float(self.m_mSimDict_[key])]
        return [0.0]