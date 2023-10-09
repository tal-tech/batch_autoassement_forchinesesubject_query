from SubjectScorer import cSubjectScorer
import sys
import time
import json


with open(sys.argv[1], "r", encoding="utf8") as f:
    lines = f.readlines()
    epochs = 0
    while True:
        mPiandi, mGuogao, mAlmostEqual, mAbsEqual, mTotal = {}, {}, {}, {}, {}
        piandi, guogao, almost_equal, total = 0, 0, 0, 0
        absolute_equal = 0
        mi, ma = float("inf"), -float("inf")
        tic = time.time()
        for line in lines:
            line = line.strip()
            if not line:
                continue
            start = time.time()
            jsonInput = json.loads(line)
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

            sOutJson = cSubjectScorer.Score(line)
            end = time.time()
            t = (end - start) * 1000
            if t > ma:
                ma = t
            if t < mi:
                mi = t
            print("OOOOOOOOOOOOO costs:%d" % t)
            jsonOutput = json.loads(sOutJson)
            jsonOutput = jsonOutput["data"]
            jsonInput = json.loads(line)
            res = jsonOutput["totalScore"]
            stdscore = int(jsonInput["stdScore"])
            useranswers = jsonInput["userAnswerContent"]
            rightanswers = jsonInput["rightAnswerContent"]

            users = [answer["text"] for answer in useranswers]
            rights = [answer["text"] for answer in rightanswers]
            if stdscore == res or (stdscore > 0 and res - stdscore == 1):
                almost_equal += 1
                mAlmostEqual[questionId] += 1
            elif res < stdscore:
                piandi += 1
                mPiandi[questionId] += 1
                sLog = "LR:" + " | ".join(rights) + "\n" + "U:" + " | ".join(users) + "\n" + str(stdscore) + "\t" + str(res)
                print(sLog)
            elif res - stdscore > 1 or (stdscore == 0 and res == 1):
                guogao += 1
                mGuogao[questionId] += 1
                sLog = "HR:" + " | ".join(rights) + "\n" + "U:" + " | ".join(users) + "\n" + str(stdscore) + "\t" + str(res)
                print(sLog)
            if stdscore == res:
                absolute_equal += 1
                mAbsEqual[questionId] += 1
            total += 1
            mTotal[questionId] += 1
        toc = time.time()
        epochs += 1
        print("相对一致率: %f" % (float(almost_equal) / total))
        print("绝对一致率: %f" % (float(absolute_equal) / total))
        print("相对一致: %d" % almost_equal)
        print("偏低: %d" % piandi)
        print("过高: %d" % guogao)
        print("总数: %d" % total)
        print("Epochs Num: %d" % epochs)
        print("---------------------------------")
        for k in mTotal.keys():
            print("%s相对一致率: %f" % (k, float(mAlmostEqual[k]) / mTotal[k]))
            print("%s绝对一致率: %f" % (k, float(mAbsEqual[k]) / mTotal[k]))
            print("%s相对一致: %d" % (k, mAlmostEqual[k]))
            print("%s过高: %d" % (k, mGuogao[k]))
            print("%s过低: %d" % (k, mPiandi[k]))
            print("%s总数: %d" % (k, mTotal[k]))
            print('=================')

        n = len(lines)
        print("Run {} jsons,spend time is {:.2f}s,{:.2f} ms/json".format(n, toc-tic, ((toc-tic) * 1000) / n))
        print("max time:%d, min time:%d" % (ma, mi))
        #time.sleep(10)
        break

"""

相对一致率: 0.758703
相对一致: 2528
偏低: 520
过高: 284
总数: 3332
Run 833 jsons,spend time is 337.39s,2.47 json/s
Run 833 jsons,spend time is 361.68s,2.30 json/s
相对一致率: 0.758703
相对一致: 6320
偏低: 1300
过高: 710
总数: 8330
Run 833 jsons,spend time is 369.06s,2.26 json/s

相对一致率: 0.758703
相对一致: 8216
偏低: 1690
过高: 923
总数: 10829
Run 833 jsons,spend time is 365.72s,2.28 json/s

top - 08:30:36 up 160 days,  7:43,  4 users,  load average: 36.17, 37.13, 36.43
Tasks:   1 total,   1 running,   0 sleeping,   0 stopped,   0 zombie
%Cpu(s): 90.3 us,  8.7 sy,  0.0 ni,  0.9 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st
%us：表示用户空间程序的cpu使用率（没有通过nice调度）

%sy：表示系统空间的cpu使用率，主要是内核程序。

%ni：表示用户空间且通过nice调度过的程序的cpu使用率。

%id：空闲cpu

%wa：cpu运行时在等待io的时间

%hi：cpu处理硬中断的数量

%si：cpu处理软中断的数量

%st：被虚拟机偷走的cpu
————————————————


KiB Mem : 26403614+total,  9474636 free, 13610955+used, 11845196+buff/cache
KiB Swap:  4194300 total,     2320 free,  4191980 used. 12201599+avail Mem 

   PID USER      PR  NI    VIRT    RES    SHR S  %CPU %MEM     TIME+ COMMAND                                      
 28913 zhaojia+  20   0 7079304 2.118g  30860 R  3774  0.8  27572:16 python   
 
zhaojia+  28913 3314  0.8 7079304 2221296 pts/5 Rl+  May20 27639:05 python TestPerformance.py data/shuqi_simi_833_new
2221296 = 2.221296GB
2221000 = 2.221GB
2	1
相对一致率: 0.758703
相对一致: 101752
偏低: 20930
过高: 11431
总数: 134113
Run 833 jsons,spend time is 360.65s,2.31 json/s
"""
