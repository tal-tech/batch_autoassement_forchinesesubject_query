
class Thesaurus():

    def Init(self, params):
        cLogger, cTool, theaurus_path = params
        self.cLogger = cLogger
        self.cTool = cTool

        self.mPos2Words, self.mWord2Pos = {}, {}
        fr = open(theaurus_path, "r", encoding="utf-8")
        vWords, vPos, vWordPos = [], [], []
        for sLine in fr.readlines():
            vWordPos = sLine.split("\t")
            if len(vWordPos) == 1:
                vWords = vWordPos[0].split(" ")
                vPos.append("无词性")
            elif len(vWordPos) == 2:
                vWords = vWordPos[0].split(" ")
                vPos = vWordPos[1].split(" ")
            else:
                continue
            for pos in vPos:
                if pos not in self.mPos2Words:
                   self.mPos2Words[pos] = []
                   self.mPos2Words[pos].append(set(vWords))
                else:
                   self.mPos2Words[pos].append(set(vWords))
            for word in vWords:
                for pos in vPos:
                    if word not in self.mWord2Pos:
                        self.mWord2Pos[word] = {}
                    if pos not in self.mWord2Pos[word]:
                        self.mWord2Pos[word][pos] = []
                    self.mWord2Pos[word][pos].append(len(self.mPos2Words[pos]) - 1)
        fr.close()
        if not len(self.mPos2Words) or not len(self.mWord2Pos):
            self.cLogger.warning("thesaurus file:%s is null!" % theaurus_path)
            return -1
        self.cLogger.info("thesaurus file:%s load success!" % theaurus_path)
        return 0

    def FindThesaurusWithLabel(self, word, pos):
        ret = set()
        if word not in self.mWord2Pos:
            return set([])
        if pos not in self.mPos2Words:
            return set([])
        for index in self.mWord2Pos[word][pos]:# 遍历该词的所有词性
            for w in self.mPos2Words[pos][index]: # 对某一个词性 找该词性对应的词
                if w != word and self.cTool.IsChn(word):
                    ret.add(w)
        # if len(ret) == 0:
        #     self.cLogger.info("word: %s, label: %s has no thesaurus words!" % (word, pos))
        # else:
        #     self.cLogger.info("word: %s, label: %s 's thesaurus words: %s" % (word, pos, "/".join(ret)))
        return ret

    def FindThesaurusAll(self, word):
        ret = set()
        if word not in self.mWord2Pos:
            return set([])
        for key, value in self.mWord2Pos[word].items():
            setCur = set()
            setCur = self.FindThesaurusWithLabel(word, key);
            for it in setCur:
                if it != word and self.cTool.IsChn(word):
                    ret.add(it)
        if len(ret) == 0:
            self.cLogger.info("word: %s 's all thesaurus words: %s" % (word, "/".join(ret)))
        return ret

    def IsThesaurus(self, word1, word2):
        if (word1 not in self.mWord2Pos) or (word2 not in self.mWord2Pos):
            return False
        for key, value in self.mWord2Pos[word1].items():
            setCur = set()
            setCur = self.FindThesaurusWithLabel(word1, key);
            if word2 in setCur:
                return True
        return False
