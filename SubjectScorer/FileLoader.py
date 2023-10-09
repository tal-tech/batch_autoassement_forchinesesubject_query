import os
import joblib

class FileLoader():

    def Init(self, params):
        if len(params) != 8:
            self.cLogger.error("fileloader params is not equal to 8")
            return -1
        stop_words_path, spec_words_path, sim_dict_path, emot_words_path, antonyms_path, word_vector_path, rf_model_path, cLogger = params
        self.cLogger = cLogger
        if self.LoadStopWords(stop_words_path) != 0:
            self.cLogger.error("load stop words failed: %s" % stop_words_path)
            return -1

        if self.LoadSpecWords(spec_words_path) != 0:
            self.cLogger.error("load spec words failed: %s" % spec_words_path)
            return -1

        if self.LoadSimDict(sim_dict_path) != 0:
            self.cLogger.error("load sim dict failed: %s" % sim_dict_path)
            return -1

        if self.LoadEmotWords(emot_words_path) != 0:
            self.cLogger.error("load emotion words failed: %s" % emot_words_path)
            return -1

        if self.LoadAntonymsDict(antonyms_path) != 0:
            self.cLogger.error("load antonyms dict failed: %s" % antonyms_path)
            return -1

        if self.LoadWordVectors(word_vector_path) != 0:
            self.cLogger.error("load word vectors failed: %s" % word_vector_path)
            return -1
        
        if self.LoadRFModel(rf_model_path) != 0:
            self.cLogger.error("load rf model failed: %s" % rf_model_path)
            return -1
        return 0

    def LineByLineRead(self, f, newline):
        sBug = ""
        while True:
            while newline in sBug:
                nPos = sBug.index(newline)
                yield sBug[:nPos]
                sBug = sBug[nPos + len(newline):]
            sChunk = f.read(200)
            if not sChunk:
                yield sBug
                break
            sBug = sBug + sChunk

    def LoadStopWords(self, stop_words_path):
        self.m_setStopWords_ = set()
        if not os.path.exists(stop_words_path):
            self.cLogger.error("file : %s not exist!" % stop_words_path)
            return -1
        with open(stop_words_path, "r", encoding="utf-8") as fr:
            for sLine in self.LineByLineRead(fr, "\n"):
                self.m_setStopWords_.add(sLine.strip())
        if len(self.m_setStopWords_) == 0:
            self.cLogger.warning("stop words file:%s is null!" % stop_words_path)
        else:
            self.cLogger.info("stop words file:%s load success!" % stop_words_path)
        return 0

    def LoadSpecWords(self, spec_words_path):
        self.m_setSpecWords_ = set()
        if not os.path.exists(spec_words_path):
            self.cLogger.error("file : %s not exist!" % spec_words_path)
            return -1
        with open(spec_words_path, "r", encoding="utf-8") as fr:
            for sLine in self.LineByLineRead(fr, "\n"):
                self.m_setSpecWords_.add(sLine.strip())
        if len(self.m_setSpecWords_) == 0:
            self.cLogger.warning("words file:%s is null!" % spec_words_path)
        else:
            self.cLogger.info("words file:%s load success!" % spec_words_path)
        return 0

    def LoadEmotWords(self, emot_words_path):
        self.m_setEmotWords_ = set()
        if not os.path.exists(emot_words_path):
            self.cLogger.error("file : %s not exist!" % spec_words_path)
            return -1
        with open(emot_words_path, "r", encoding="utf-8") as fr:
            for sLine in self.LineByLineRead(fr, "\n"):
                self.m_setEmotWords_.add(sLine.strip())
        if len(self.m_setEmotWords_) == 0:
            self.cLogger.warning("words file:%s is null!" % emot_words_path)
        else:
            self.cLogger.info("words file:%s load success!" % emot_words_path)
        return 0

    def LoadSimDict(self, sim_dict_path):
        self.m_mSimDict_ = {}
        if not os.path.exists(sim_dict_path):
            self.cLogger.error("file : %s not exist!" % sim_dict_path)
            return -1
        fr = open(sim_dict_path, "r", encoding="utf-8")
        for sLine in self.LineByLineRead(fr, "\n"):
            itms = sLine.split("\t")
            if len(itms) != 3:
                continue
            sRightSeg, sUserSeg, sSimScore = itms[0], itms[1], itms[2]
            if not sSimScore.isdigit():
                continue
            self.m_mSimDict_[(sRightSeg, sUserSeg)] = float(sSimScore)
        fr.close()
        if len(self.m_mSimDict_) == 0:
            self.cLogger.warning("sim dict file: %s is null!" % sim_dict_path)
        else:
            self.cLogger.info("sim dict file: %s load success!" % sim_dict_path)
        return 0

    def LoadAntonymsDict(self, antonyms_path):
        self.m_mAntonymsDict_ = {}
        if not os.path.exists(antonyms_path):
            self.cLogger.error("file : %s not exist!" % antonyms_path)
            return -1
        with open(antonyms_path, "r", encoding="utf-8") as fr:
            for sLine in self.LineByLineRead(fr, "\n"):
                vData = sLine.split(" ")
                if len(vData) < 0 or vData[0] == "":
                    continue
                if vData[0] not in self.m_mAntonymsDict_:
                    setCur = set()
                    setCur.add(vData[1])
                    self.m_mAntonymsDict_[vData[0]] = setCur
                else:
                    self.m_mAntonymsDict_[vData[0]].add(vData[1])
        if len(self.m_mAntonymsDict_) == 0:
            self.cLogger.error("antonyms file: %s is null!" % antonyms_path)
        else:
            self.cLogger.info("antonyms file: %s load success!" % antonyms_path)
        return 0

    def LoadWordVectors(self, word_vec_path):
        if not os.path.exists(word_vec_path):
            self.cLogger.error("file : %s not exist!" % word_vec_path)
            return -1
        fr = open(word_vec_path, "r", encoding="utf-8")
        self.m_mWordVectors_ = {}
        for sLine in fr.readlines():
            sWord, sVectorString = sLine.split("\t")
            vVector = [float(x) for x in sVectorString.split(" ")]
            self.m_mWordVectors_[sWord] = vVector
        fr.close()
        if len(self.m_mWordVectors_) == 0:
            self.cLogger.info("word vectors file: %s is null!" % word_vec_path)
        else:
            self.cLogger.info("word vectors file: %s load success!" % word_vec_path)
        return 0

    def LoadRFModel(self, model_path):
        if not os.path.exists(model_path):
            self.cLogger.error("rf model file: %s not exist!" % model_path)
            return -1
        try:
            self.m_cRFModel_ = joblib.load(model_path)
            self.cLogger.info("rf model file: %s load success!" % model_path)
        except:
            self.cLogger.info("rf model file: %s load failed!" % model_path)
            return -1
        return 0

