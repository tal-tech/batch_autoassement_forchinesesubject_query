import sys
import os
import json
import joblib
from pyltp import Segmentor, Postagger


from Tools import Tools
from Logger import Logger
from Thesaurus import Thesaurus
from FileLoader import FileLoader
from Antonyms import Antonyms
from JsonInteractor import JsonInteractor
from RF import RF

basePath = os.path.dirname(os.path.realpath(__file__))

class SubjectScorer():
    def __init__(self):
        self.m_nSucCode = 300034020

    def Init(self, paths):
        #logger
        cLogger = Logger()
        if cLogger.Init("warning") != 0:
            self.cLogger = cLogger.m_cLogger
            self.cLogger.error("logger init failed!")
            return -1
        self.cLogger = cLogger.m_cLogger

        # load JsonInteractor
        self.cJsonInteractor = JsonInteractor()
        vParams = [self.cLogger]
        if self.cJsonInteractor.Init(vParams) != 0:
            self.cLogger.error("json interactor init failed!")
            return -1
        self.cLogger.warning("JsonInteractor init success!")

        # check paths
        if len(paths) == 13:
            rf_model_file, word_vec_file, thesarus_file, stop_words_file, spec_words_file, \
            sim_dict_file, emotion_words_file, antonyms_file, LTP_DATA_DIR, ner_model_path, \
            cws_model_path, pos_model_path, lexicon_path = paths
        else:
            self.cLogger.error("file paths lack, not equal to 13")
            return -1
        for sPath in paths:
            if not os.path.exists(sPath):
                self.cLogger.error("file path: %s is not exist!" % sPath)
                return -1
        self.cLogger.warning("all paths check success!")
        # load Tools
        self.cTools = Tools()
        if self.cTools.Init(self.cLogger) != 0:
            self.cLogger.error("Tools class init failed!")
            return -1
        self.cLogger.warning("tools init success!")
        # load FileLoader
        vParams = [stop_words_file, spec_words_file, sim_dict_file, emotion_words_file, antonyms_file, word_vec_file, rf_model_file, self.cLogger]
        self.cFileLoader = FileLoader()
        if len(vParams) != 8:
            self.cLogger.error("fileload class params num is not equal to 8!")
            return -1
        if self.cFileLoader.Init(vParams) != 0:
            self.cLogger.error("fileload class init faild!")
            return -1
        self.cLogger.warning("FileLoader init success!")

        # load Thesaurus
        self.cThesaurus = Thesaurus()
        vParams = [self.cLogger, self.cTools, thesarus_file]
        if self.cThesaurus.Init(vParams) != 0:
            self.cLogger.error("thesarus init failed!")
            return -1
        self.cLogger.warning("Thesaurus init success!")

        # load Antonyms
        self.cAntonyms = Antonyms()
        vParams = [self.cLogger, self.cFileLoader.m_mAntonymsDict_]
        if self.cAntonyms.Init(vParams) != 0:
            self.cLogger.error("antonyms init failed!")
            return -1
        self.cLogger.warning("Antonyms init success!")

        # load RF
        self.cRF = RF()
        vParams = [self.cLogger, self.cFileLoader, self.cTools]
        if self.cRF.Init(vParams) != 0:
            self.cLogger.error("rf init failed!")
            return -1
        self.cLogger.warning("RF init success!")

        #load ltp
        if not os.path.exists(cws_model_path):
            self.cLogger.error("cws model path : %s not exists!" % cws_model_path)
            return -1
        if not os.path.exists(lexicon_path):
            self.cLogger.error("lexicon path : %s not exists!" % lexicon_path)
            return -1
        try:
            self.segmentor = Segmentor()  # 初始化实例
            self.segmentor.load_with_lexicon(cws_model_path, lexicon_path)  # 加载模型，第二个参数是您的外部词典文件路径
            self.cLogger.info("segmentor load success, cws model:%s and lexicon:%s" % (cws_model_path, lexicon_path))
        except:
            self.cLogger.error("segmentor load failed, cws model:%s and lexicon:%s" % (cws_model_path, lexicon_path))
            return -1
        try:
            self.postagger = Postagger()
            self.postagger.load(pos_model_path)
            self.cLogger.info("segmentor load success, pos model:%s" % (pos_model_path))
        except:
            self.cLogger.error("segmentor load failed, pos model:%s" % (pos_model_path))
            return -1
        self.cLogger.warning("ltp init success!")
        return 0


    def GetLtpResult(self, sent, segmentor, postagger):
        if sent == "":
            self.cLogger.warning("sent : %s is null!" % sent)
            return 0, [[], []]
        words, postags = [], []

        try:
            words = segmentor.segment(sent)
        except:
            self.cLogger.error("segment failed!")
            return -1, []
        try:
            postags = postagger.postag(words)  # 词性标注
        except:
            self.cLogger.error("postag failed!")
            return -1, []
        return 0, [words, postags]


    def RFMatch(self, right_text, user_text, right_segs, right_tags, user_segs, user_tags):
        nState, X = self.cRF.GetX(right_text, user_text, right_segs, right_tags, user_segs, user_tags)
        if nState != 0:
            self.cLogger.error("rf_match failed!")
            return -1, False
        nTotalScore = int(self.cRF.m_cModel.predict([X])[0])
        if nTotalScore == 1:
            return 0, True
        else:
            return 0, False


    def SpecialWordMatch(self, point_segs, vUserSegs):
        setUserSegs = set(vUserSegs)
        for sWord in point_segs:
            if sWord in self.cFileLoader.m_setSpecWords_ and sWord not in setUserSegs:
                return 0, True
        return 0, False


    def KeywordMatch(self, key_words, right_segs, right_tags, user_segs, user_tags):
        tags = ("a", "v", "i", "n", "ns", "nh", "nd", "ni", "nl", "nt", "r", "z", "d")
        distances = [self.cTools.NormCosin, self.cTools.NormEuclidean]
        vParams1 = (right_segs, right_tags, self.cThesaurus, self.cFileLoader.m_setSpecWords_,
                  self.cFileLoader.m_setEmotWords_, tags, self.cFileLoader.m_mWordVectors_, distances)
        vParams2 = (key_words, self.cThesaurus)

        vKeyAround = []
        if not self.cTools.HasChn(key_words):
            nState, mKeyArounds = self.cTools.ExtractKeywords(vParams1)
            fAroundMatchThreshold = 0.02  # 0.9
            fKeyMatchThreshold = 0.32  # 0.32
            fWordSimThreshold = 0.8  # 0.8
            fSimiWordThreshold = 0.8
            if nState != 0:
                self.cLogger.error("extract keywords failed!")
                return -1, False
            vKeyAround = [mKeyArounds] #自动抽取的关键词兼容提供的多套关键词的存储格式
        else:
            nState, vKeyAround = self.cTools.LoadKeyWords(vParams2)
            fAroundMatchThreshold = 0.02
            fKeyMatchThreshold = 0.12
            fWordSimThreshold = 0.8
            fSimiWordThreshold = 1
            if nState != 0:
                self.cLogger.error("load keywords failed!")
                return -1, False
        vUserSegs = [x for x in user_segs if x not in self.cFileLoader.m_setStopWords_]
        vRightSegs = [x for x in right_segs if x not in self.cFileLoader.m_setStopWords_]
        for mKeyAround in vKeyAround:
            matched_keyword_num = 0
            vMatchedKeywords = []
            vMatchedArounds = []
            if len(mKeyAround.keys()) == 0:
                return 0, False
            for k, v in mKeyAround.items():
                key_match_flag = False
                if k in vUserSegs:
                    key_match_flag = True
                    self.cLogger.info("keyword %s is contained in user" % k)
                sim_word = []
                # 中心词相似度
                if not key_match_flag:
                    for u in vUserSegs:
                        if self.cAntonyms.IsAntonymsWords(k, u):
                            continue
                        if k not in self.cFileLoader.m_mWordVectors_:
                            break
                        vKVec = self.cFileLoader.m_mWordVectors_[k]
                        if u not in self.cFileLoader.m_mWordVectors_:
                            continue

                        vUVec = self.cFileLoader.m_mWordVectors_[u]
                        fDistanceCosin = distances[0](vKVec, vUVec)
                        fDistanceEucli = distances[1](vKVec, vUVec)
                        # self.cLogger.info("keyword (%s, %s) cosin simi: %f eucli simi %f" % (k, u, fDistanceCosin, fDistanceEucli))
                        if fDistanceCosin > fWordSimThreshold or fDistanceEucli > fWordSimThreshold:
                            key_match_flag = True
                            sim_word.append(u)
                            self.cLogger.info("keyword %s is similar to user word %s" % (k, u))
                            break
                if key_match_flag:
                    vMatchedKeywords.append(k)

                    matched_keyword_num += 1
                    matched_around_num = 0
                    vMatchedArounds = []
                    if len(v) == 0:  # 没有周围词
                        log_sim_word = " ".join(sim_word)
                        self.cLogger.info("---Center Word Matched [%s->%s], No Around---" % (k, log_sim_word))
                        return 0, True
                    for around in v:
                        #65%

                        # 去除周围词与中心词的相似度过高的词
                        if k in self.cFileLoader.m_mWordVectors_ and around in self.cFileLoader.m_mWordVectors_:
                            vKVec = self.cFileLoader.m_mWordVectors_[k]
                            vAVec = self.cFileLoader.m_mWordVectors_[around]
                            if distances[0](vKVec, vAVec) > fSimiWordThreshold or distances[1](vKVec, vAVec) > fSimiWordThreshold:
                                continue

                        if around in vUserSegs and around != k:
                            matched_around_num += 1
                            vMatchedArounds.append(around)
                            self.cLogger.info("around word:%s match" % around)
                            matched_around_rate = matched_around_num / len(v)
                            log_matched_centers = "|".join(vMatchedKeywords)
                            log_arounds = "/".join(v)
                            log_matched_arounds = "|".join(vMatchedKeywords)
                            if matched_around_rate > fAroundMatchThreshold:  # 关键词匹配，周围词匹配大于某一阈值
                                self.cLogger.info("---Center Word Matched [%s], Around Words [%s] Matched [%s] Around  Match Rate (%.3f) Bigger Than (%.3f)---" % (log_matched_centers, log_arounds, log_matched_arounds, matched_around_rate, fAroundMatchThreshold))
                                return 0, True
            matched_keyword_rate = matched_keyword_num / len(mKeyAround.keys())
            log_matched_centers = "|".join(vMatchedKeywords)
            self.cLogger.info("matched center words: %s" % log_matched_centers)
            if matched_keyword_rate > fKeyMatchThreshold:  # 关键词匹配度达到某一阈值
                self.cLogger.info("---Center Word Matched [%s] Rate (%.3f) Bigger Than (%.3f)---" %
                             (log_matched_centers, matched_keyword_rate, fKeyMatchThreshold))
                return 0, True
        return 0, False

    def Process(self, data):
        vUsers, vRights, vScores, vKeyWords = [], [], [], []
        for mContent in data["userAnswerContent"]:
            vUsers.append(mContent["text"])

        for mContent in data["rightAnswerContent"]:
            vRights.append(mContent["text"])
            vScores.append(mContent["score"])
            if "keyWord" not in mContent:
                vKeyWords.append("")
            else:
                vKeyWords.append(mContent["keyWord"])
        vRightSegments = []
        vRightPostags = []
        for i in range(len(vRights)):
            nState, vItms = self.GetLtpResult(vRights[i], self.segmentor, self.postagger)
            if nState != 0:
                return -1, []
            vRightSegs, vRightTags = vItms
            vRightSegments.append(list(vRightSegs))
            vRightPostags.append(list(vRightTags))
            # self.cLogger.info("segments and postags for points: %d" % i)
            # self.cLogger.info("%s" % " ".join(list(vRightSegs)))
            # self.cLogger.info("%s" % " ".join(list(vRightTags)))
        vUserSegments = []
        vUserPostags = []
        for j in range(len(vUsers)):
            nState, vItms = self.GetLtpResult(vUsers[j], self.segmentor, self.postagger)
            if nState != 0:
                return -1, []
            vUserSegs, vUserTags = vItms
            vUserSegments.append(list(vUserSegs))
            vUserPostags.append(list(vUserTags))
            # self.cLogger.info("segments and postags for users: %d" % j)
            # self.cLogger.info("%s" % " ".join(list(vUserSegs)))
            # self.cLogger.info("%s" % " ".join(list(vUserTags)))
        nState, vItms = self.cTools.RemoveDuplicates(vRightSegments, vRightPostags)
        if nState != 0:
            self.cLogger.error("remove duplicates error")
            return -1, []
        vRightSegmentsRemoved, vRightPostagsRemoved = vItms
        fTotalScore = 0.0
        mMatchedPairs = {}

        features = ["char_match", "word_match", "rf_match", "keyword_match",  "special_word_match"]
        weights = [1, 1, 1, 1, -100]
        nWeightSum = 0
        for i in range(0, len(vRights)):
            vRightSegs, vRightTags = vRightSegmentsRemoved[i], vRightPostagsRemoved[i]
            self.cLogger.info("Ori Right Content[%d]: %s" % (i, vRights[i]))
            self.cLogger.info("Seg Right Content[%d]: %s" % (i, " ".join(vRightSegs)))
            right_text_removed = "".join(vRightSegs)
            for j in range(0, len(vUsers)):
                self.cLogger.info("=======P:%d==U%d================" % (i, j))
                vUserSegs, vUserTags = vUserSegments[j], vUserPostags[j]
                self.cLogger.info("--vRights num: %d--vUsers num: %d--vRights index: %d--vUsers index: %d--" % (
                    len(vRights), len(vUsers), i, j))
                self.cLogger.info("Ori User Content[%d]: %s" % (j, vUsers[j]))
                self.cLogger.info("Seg User Content[%d]: %s" % (j, " ".join(vUserSegs)))

                # char match
                chars1 = [c for c in right_text_removed if self.cTools.IsChn(c)]
                chars2 = [c for c in vUsers[j] if self.cTools.IsChn(c)]
                cjiaoji = set(chars1) & set(chars2)
                if len(chars1) == 0:
                    cmatch = 0
                else:
                    cmatch = float(len(cjiaoji) / len(set(chars1)))
                cvalue = 0.5
                cMatch = False
                wMatch = False
                if cmatch >= cvalue:
                    #value += weights[0]
                    cMatch = True
                    mMatchedPairs[str(i) + "-" + str(j) + "-" "char_match"] = 1
                else:
                    mMatchedPairs[str(i) + "-" + str(j) + "-" "char_match"] = 0
                self.cLogger.info("chars1: %s" % (" ".join(chars1)))
                self.cLogger.info("chars2: %s" % (" ".join(chars2)))
                self.cLogger.info("char match point: %d \t equal: %d" % (len(set(chars1)), len(cjiaoji)))
                self.cLogger.info("char match threshold:%f \t cmatch:%f" % (cvalue, cmatch))
                # word match
                words1 = [word for word in vRightSegs if word not in self.cFileLoader.m_setSpecWords_ and self.cTools.IsChn(word)]
                words2 = [word for word in vUserSegs if word not in self.cFileLoader.m_setSpecWords_ and self.cTools.IsChn(word)]
                self.cLogger.info("words1: %s" % (" ".join(words1)))
                self.cLogger.info("words2: %s" % (" ".join(words2)))
                wjiaoji = set(words1) & set(words2)
                if len(set(words1)):
                    wmatch = float(len(wjiaoji)) / len(set(words1))
                else:
                    wmatch = 0
                wvalue = 0.3
                if wmatch >= wvalue:
                    #value += weights[1]
                    wMatch = True
                    mMatchedPairs[str(i) + "-" + str(j) + "-" + "word_match"] = 1
                else:
                    mMatchedPairs[str(i) + "-" + str(j) + "-" + "word_match"] = 0
                self.cLogger.info("word match point: %d \t equal: %d" % (len(set(words1)), len(wjiaoji)))
                self.cLogger.info("word match threshold:%f \t wmatch:%f" %(wvalue, wmatch))
                # keyword match
                nState, bKeywordPred = self.KeywordMatch(vKeyWords[i], vRightSegs, vRightTags, vUserSegs, vUserTags)
                if nState != 0:
                    self.cLogger.error("keyword match failed!")
                    return -1, []
                if bKeywordPred:
                    mMatchedPairs[str(i) + "-" + str(j) + "-" + "keyword_match"] = 1
                else:
                    mMatchedPairs[str(i) + "-" + str(j) + "-" + "keyword_match"] = 0
                self.cLogger.info("keyword match's bKeywordPred:%d" % bKeywordPred)
                # rf match
                nState, bRFPred = self.RFMatch(vRights[i], vUsers[j], vRightSegs, vRightTags, vUserSegs, vUserTags)
                if nState != 0:
                    self.cLogger.error("rf match failed!")
                    return -1, []
                if bRFPred:
                    mMatchedPairs[str(i) + "-" + str(j) + "-" + "rf_match"] = 1
                else:
                    mMatchedPairs[str(i) + "-" + str(j) + "-" + "rf_match"] = 0
                self.cLogger.info("rf match's bRFPred:%d" % bRFPred)

                # special word match
                nState, bSpecWordMatch = self.SpecialWordMatch(vRightSegs, vUserSegs)
                if nState != 0:
                    self.cLogger.error("special_word_match failed!")
                    return -1, []
                if bSpecWordMatch:
                    mMatchedPairs[str(i) + "-" + str(j) + "-" + "special_word_match"] = 1
                else:
                    mMatchedPairs[str(i) + "-" + str(j) + "-" + "special_word_match"] = 0
                self.cLogger.info("special word match's bSpecWordMatch:%d" % bSpecWordMatch)
        sMatchedMethods = ""
        mUserMatchs = {}
        for i in range(len(vRights)):
            for j in range(len(vUsers)):
                weight_sum = 0
                matched_methods = ""
                for k in range(len(features)):
                    key_str = str(i) + "-" + str(j) + "-" + features[k]
                    if key_str not in mMatchedPairs:
                        continue
                    fea_score = mMatchedPairs[key_str]
                    if fea_score > 0:
                        weight_sum += weights[k]
                        matched_methods += (features[k] + "|")
                if weight_sum > nWeightSum:
                    if j not in mUserMatchs:
                        mUserMatchs[j] = [i]
                    else:
                        mUserMatchs[j].append(i)
                    fTotalScore += vScores[i]
                    sMatchedMethods += "P%dU%d:%s" % (i, j, matched_methods)
                    break
        if fTotalScore > float(data["maxScore"]):
            fTotalScore = float(data["maxScore"])
        self.cLogger.warning("final score: %d" % fTotalScore)
        vOutAnswerContent = []
        for j in range(len(vUsers)):
            mContent = {}
            mContent["id"] = j
            mContent["text"] = vUsers[j]
            fScore = 0.0
            vMatchRights = []
            if j not in mUserMatchs:
                mContent["score"] = 0.0
                mContent["matchedAnswerInfo"] = []
                vOutAnswerContent.append(mContent)
                continue
            for i in mUserMatchs[j]:
                fScore += data["rightAnswerContent"][i]["score"]
                vMatchRights.append(data["rightAnswerContent"][i]["text"])
            if fScore > float(data["maxScore"]):
                fScore = float(data["maxScore"])
            mContent["score"] = fScore
            mContent["matchedAnswerInfo"] = vMatchRights
            vOutAnswerContent.append(mContent)
        s = self.cJsonInteractor.PrintInfo(data, fTotalScore, sMatchedMethods)
        self.cLogger.warning(s)
        return 0, [fTotalScore, vOutAnswerContent]

    def Score(self, json_str):
        if not bInitFlag:
            cSubjectScorer.cLogger.error("subject scorer init failed!")
            nCode = 300034021
            sMsg = "init failed"
            vParams = [nCode, sMsg, 0.0, [], self.m_nSucCode]
            _, sOutJson = self.cJsonInteractor.HandleOutput(vParams)
            return sOutJson
        nState, mInputJson = self.cJsonInteractor.HandleInput(json_str)
        if nState != 0:
            self.cLogger.error("input json is not valid")
            nCode = 300034022
            sMsg = "input json is not valid"
            vParams = [nCode, sMsg, 0.0, [], self.m_nSucCode]
            _, sOutJson = self.cJsonInteractor.HandleOutput(vParams)
            return sOutJson

        nState, vItms = self.Process(mInputJson)
        if nState != 0 or len(vItms) != 2:
            if len(vItms) != 2:
                self.cLogger.error("process output item is not equal to 2")
            self.cLogger.error("score failed")
            nCode = 300034023
            sMsg = "score failed"
            vParams = [nCode, sMsg, 0.0, [], self.m_nSucCode]
            _, sOutJson = self.cJsonInteractor.HandleOutput(vParams)
            return sOutJson
        nCode = 300034020
        sMsg = "success"
        fTotalScore, vOutAnswerContent = vItms
        vParams = [nCode, sMsg, fTotalScore, vOutAnswerContent, self.m_nSucCode]
        _, sOutJson = self.cJsonInteractor.HandleOutput(vParams)

        self.cLogger.warning("Output Json:%s" % sOutJson)
        return sOutJson

# file path

rf_model_file = basePath + "/data/rf.pkl"
word_vec_file = basePath + "/data/word.vector"
thesarus_file = basePath + "/data/word_class.txt"
stop_words_file = basePath + "/data/stop_words"
spec_words_file = basePath + "/data/major_words.txt"
sim_dict_file = basePath + "/data/seg_pairs_sim.txt"
emotion_words_file = basePath + "/data/emotion_words.txt"
antonyms_file = basePath + "/data/antonyms_total.txt"
LTP_DATA_DIR = basePath + "/data/ltp_data_v3.4.0"
ner_model_path = os.path.join(LTP_DATA_DIR, 'ner.model')
cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')  # 分词模型路径，模型名称为`cws.model`
pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')  # 词性标注模型路径，模型名称为`pos.model`
lexicon_path = os.path.join(LTP_DATA_DIR, 'lexicon')
#13个
paths = [rf_model_file, word_vec_file, thesarus_file, stop_words_file, spec_words_file,
         sim_dict_file, emotion_words_file, antonyms_file, LTP_DATA_DIR, ner_model_path,
         cws_model_path, pos_model_path, lexicon_path]

bInitFlag = True
cSubjectScorer = SubjectScorer()
if cSubjectScorer.Init(paths) != 0:
    bInitFlag = False


if __name__ =="__main__":
    pass
