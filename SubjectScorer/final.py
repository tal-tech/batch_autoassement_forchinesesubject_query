#!/usr/bin/env python
# coding=utf-8
import sys
import time
import json

count = 0
mPiandi, mGuogao, mAlmostEqual, mAbsEqual, mTotal = {}, {}, {}, {}, {}
piandi, guogao, almost_equal, total = 0, 0, 0, 0
absolute_equal = 0

tic = time.time()
#for line in lines:
bInput = False
bOutput = False
sInput = "Input Json:"
sOutput = "Output Json:"
for line in open(sys.argv[1]):
    line = line.strip()
    #if not line:
    #if line.find("- final score: ") == -1:
    #    continue
    if line.find(sInput) != -1:
        bInput = True
        jsonInput = line.split(sInput)[-1]
        continue
    elif line.find(sOutput) != -1:
        bOutput = True
        jsonOutput = line.split(sOutput)[-1]
    if not (bInput and bOutput):
        continue
    bInput, bOutput = False, False
    count += 1
    print("行数：", count)
#    print(jsonInput)
#    print(type(jsonInput))
#    print(jsonOutput)
#    print(type(jsonOutput))
    jsonOutput = json.loads(jsonOutput)
    jsonOutput = jsonOutput["data"]
    jsonInput = json.loads(jsonInput)
    res = jsonOutput["totalScore"]
    print(int(res))
    if "stdScore" in jsonInput:
        stdscore = jsonInput["stdScore"]
    else:
        stdscore = 0 
    useranswers = jsonInput["userAnswerContent"]
    rightanswers = jsonInput["rightAnswerContent"]
    questionId = jsonInput["questionId"]
    if questionId not in mPiandi:
        mPiandi[questionId] = 0
    if questionId not in mGuogao:
        mGuogao[questionId] = 0
    if questionId not in mAlmostEqual:
        mAlmostEqual[questionId] = 0
    if questionId not in mAbsEqual:
        mAbsEqual[questionId] = 0
    if questionId not in mTotal:
        mTotal[questionId] = 0

    users = [answer["text"] for answer in useranswers]
    rights = [answer["text"] for answer in rightanswers]
    if stdscore == res or (stdscore > 0 and res - stdscore == 1):
        almost_equal += 1
        mAlmostEqual[questionId] += 1
    elif res < stdscore:
        piandi += 1
        mPiandi[questionId] += 1
        #sLog = "LR:" + " | ".join(rights) + "\n" + "U:" + " | ".join(users) + "\n" + str(stdscore) + "\t" + str(res)
        #print(sLog)
    elif res - stdscore > 1 or (stdscore == 0 and res == 1):
        guogao += 1
        mGuogao[questionId] += 1
        #sLog = "HR:" + " | ".join(rights) + "\n" + "U:" + " | ".join(users) + "\n" + str(stdscore) + "\t" + str(res)
        #print(sLog)
    if stdscore == res:
        absolute_equal += 1
        mAbsEqual[questionId] += 1
    total += 1
    mTotal[questionId] += 1
toc = time.time()
print("相对一致率: %f" % (float(almost_equal) / total))
print("绝对一致率: %f" % (float(absolute_equal) / total))
print("相对一致: %d" % almost_equal)
print("偏低: %d" % piandi)
print("过高: %d" % guogao)
print("总数: %d" % total)
print("---------------------------------")
for k in mTotal.keys():
    print("%s相对一致率: %f" % (k, float(mAlmostEqual[k]) / mTotal[k]))
    print("%s绝对一致率: %f" % (k, float(mAbsEqual[k]) / mTotal[k]))
    print("%s相对一致: %d" % (k, mAlmostEqual[k]))
    print("%s过高: %d" % (k, mGuogao[k]))
    print("%s过低: %d" % (k, mPiandi[k]))
    print("%s总数: %d" % (k, mTotal[k]))
    print('=================')

n = count
print("Run {} jsons,spend time is {:.2f}s,{:.2f} ms/json".format(n, toc-tic, ((toc-tic) * 1000) / n))
