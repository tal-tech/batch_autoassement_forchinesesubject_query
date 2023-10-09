class Antonyms():
    def Init(self, params):
        cLogger, antonyms_dict = params
        self.m_mAntonymsDict_ = antonyms_dict
        if len(self.m_mAntonymsDict_) == 0:
            self.cLogger.warning("antonyms dict is null!")
        self.cLogger = cLogger
        return 0
    def IsAntonymsWords(self, word1, word2):
        if word1 in self.m_mAntonymsDict_ and word2 in self.m_mAntonymsDict_[word1]:
            self.cLogger.info("word1:%s and word2:%s is antonyms" % (word1, word2))
            return True
        if word2 in self.m_mAntonymsDict_ and word1 in self.m_mAntonymsDict_[word2]:
            self.cLogger.info("word2:%s and word1:%s is antonyms" % (word1, word2))
            return True
        return False
    """"""