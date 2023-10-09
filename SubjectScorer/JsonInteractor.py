import json
class JsonInteractor():
    def Init(self, params):
        cLogger = params[0]
        self.cLogger = cLogger

        return 0

    def HandleInput(self, json_line):
        mJsonData = {}
        try:
            mJsonData = json.loads(json_line)
            self.cLogger.warning("Input Json:%s" % json_line)
        except:
            self.cLogger.error("input json:%s is not valid, please check input" % json_line)
            return -1, {}
        if "userId" not in mJsonData:
            self.cLogger.error("input json lack of info: userId!")
            return -1, {}
        if mJsonData["userId"] == "":
            self.cLogger.error("input json's userId is null!")
            return -1, {}
        if type(mJsonData["userId"]) != str:
            self.cLogger.error("input json's userId's type is not str!")
            return -1, {}
        if "liveId" in mJsonData:
            if type(mJsonData["liveId"]) != str:
                self.cLogger.error("input json's liveId's type is not str!")
                return -1, {}
        if "deviceId" in mJsonData:
            if type(mJsonData["deviceId"]) != int:
                self.cLogger.error("input json's deviceId's type is not int!")
                return -1, {}
        if "questionType" in mJsonData:
            if type(mJsonData["questionType"]) != str:
                self.cLogger.error("input json's questionType's type is not str!")
                return -1, {}
        if "gradeType" not in mJsonData:
            self.cLogger.error("input json lack of info: gradeType!")
            return -1, {}
        if type(mJsonData["gradeType"]) != int:
            self.cLogger.error("input json's gradeType's type is not int!")
            return -1, {}
        if mJsonData["gradeType"] not in [8, 9, 10]:
            self.cLogger.error("input json's gradeType is out of range!")
            return -1, {}

        if "questionId" not in mJsonData:
            self.cLogger.error("input json lack of info: questionId!")
            return -1, {}
        if mJsonData["questionId"] == "":
            self.cLogger.error("input json's questionId is null!")
            return -1, {}
        if type(mJsonData["questionId"]) != str:
            self.cLogger.error("input json's questionId's type is not str!")
            return -1, {}

        if "question" not in mJsonData:
            self.cLogger.error("input json lack of info: question!")
            return -1, {}
        if mJsonData["question"] == "":
            self.cLogger.error("input json's question is null!")
            return -1, {}
        if type(mJsonData["question"]) != str:
            self.cLogger.error("input json's question's type is not str!")
            return -1, {}

        if "maxScore" not in mJsonData:
            self.cLogger.error("input json lack of info: maxScore!")
            return -1, {}
        if type(mJsonData["maxScore"]) != float and type(mJsonData["maxScore"]) != int:
            self.cLogger.error("input json's maxScore's type is not float!")
            return -1, {}
        if float(mJsonData["maxScore"]) <= 0:
            self.cLogger.error("input json's maxScore's value is not valid!")
            return -1, {}
        
        if "multiAnswerType" not in mJsonData:
            mJsonData["multiAnswerType"] = 1
        else:
            if mJsonData["multiAnswerType"] not in [1, 2]:
                self.cLogger.error("input json's multiAnswerType is not valid!")
                return -1, {}
        
        if "userAnswerContent" not in mJsonData:
            self.cLogger.error("input json lack of info: userAnswerContent!")
            return -1, {}
        if type(mJsonData["userAnswerContent"]) != list:
            self.cLogger.error("input json's userAnswerContent's type is not array!")
            return -1, {}
        if len(mJsonData["userAnswerContent"]) == 0:
            self.cLogger.error("input json's userAnswerContent's is null array!")
            return -1, {}

        for itm in mJsonData["userAnswerContent"]:
            if "id" not in itm:
                self.cLogger.error("input json's userAnswerContent lack of info: id!")
                return -1, {}
            if type(itm["id"]) != int:
                self.cLogger.error("input json's userAnswerContent's id's type is not int!")
                return -1, {}
            if "text" not in itm:
                self.cLogger.error("input json's userAnswerContent lack of info: text!")
                return -1, {}
            if type(itm["text"]) != str:
                self.cLogger.error("input json's userAnswerContent's text's type is not str!")
                return -1, {}

        if "rightAnswerContent" not in mJsonData:
            self.cLogger.error("input json lack of info: rightAnswerContent!")
            return -1, {}
        if type(mJsonData["rightAnswerContent"]) != list:
            self.cLogger.error("input json's rightAnswerContent's type is not array!")
            return -1, {}
        if len(mJsonData["rightAnswerContent"]) == 0:
            self.cLogger.error("input json's rightAnswerContent's is null array!")
            return -1, {}

        for itm in mJsonData["rightAnswerContent"]:
            if "id" not in itm:
                self.cLogger.error("input json's rightAnswerContent lack of info: id!")
                return -1, {}
            if type(itm["id"]) != int:
                self.cLogger.error("input json's rightAnswerContent's id's type is not int!")
                return -1, {}

            if "text" not in itm:
                self.cLogger.error("input json's rightAnswerContent lack of info: text!")
                return -1, {}
            if itm["text"] == "":
                self.cLogger.error("input json's rightAnswerContent's text is null!")
                return -1, {}
            if type(itm["text"]) != str:
                self.cLogger.error("input json's rightAnswerContent's text's type is not str!")
                return -1, {}

            if "score" not in itm:
                self.cLogger.error("input json's rightAnswerContent lack of info: score!")
                return -1, {}
            if type(itm["score"]) != float and type(itm["score"]) != int:
                self.cLogger.error("input json's rightAnswerContent's score's type is not float!")
                return -1, {}
            if float(itm["score"]) <= 0:
                self.cLogger.error("input json's rightAnswerContent's score's value is not valid!")
                return -1, {}

            if "keyWord" not in itm:
                self.cLogger.error("input json's rightAnswerContent lack of info:keyWord!")
            if "keyWord" in itm and type(itm["keyWord"]) != str:
                self.cLogger.error("input json's rightAnswerContent's keyWord's type is not str!")
                return -1, {}
        return 0, mJsonData

    def HandleOutput(self, params):
        if len(params) != 5:
            self.cLogger.error("handle output params is not equal to 4!")
            return -1, ""
        nCode, sMsg, fTotalScore, vOutAnswerContent, nSuccCode = params
        jsonOut = {}
        if nCode != nSuccCode:
            jsonOut["code"] = nCode
            jsonOut["msg"] = sMsg
            jsonOut["requestId"] = ""
            jsonOut["data"] = {}
            self.cLogger.error("handle output failed, error code:%d" % nCode)
            return -1, jsonOut

        mJsonData = {}
        mJsonData["totalScore"] = float(fTotalScore)
        mJsonData["userAnswerContent"] = vOutAnswerContent

        jsonOut["code"] = nCode
        jsonOut["msg"] = sMsg
        jsonOut["requestId"] = ""
        jsonOut["data"] = mJsonData
        sOutJosn = json.dumps(jsonOut, ensure_ascii=False).replace("\'", "\"")
        self.cLogger.info("handle output json success : %s" % sOutJosn)
        return 0, sOutJosn



    def PrintInfo(self, input_json, total_score, matched_methods):

        users = [answer["text"] for answer in input_json["userAnswerContent"]]
        rights = [answer["text"] for answer in input_json["rightAnswerContent"]]
        if "stdScore" not in input_json:
            stdScore = str(0.0)
        else:
            stdScore = str(input_json["stdScore"])
        s = "####-"
        s += input_json["userId"] + "\t" + input_json["questionId"] + "\t"
        s += " | ".join(rights) + "\t"
        s += " | ".join(users) + "\t"
        s += str(input_json["maxScore"]) + "\t"
        s += stdScore + "\t"
        s += str(total_score) + "\t"
        s += matched_methods
        # for content in userAnswerContents:
        #     s += content["text"] + "\t" + str(content["score"]) + "\t"
        #     s += " | ".join(content["matchedAnswerInfo"]) + "\t"
        return s
