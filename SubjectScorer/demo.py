"""
中文主观题批改模型
"""
from SubjectScorer import cSubjectScorer
import ast
import json

input0 = '{"userId": "12345", "gradeType": 8, "questionId": "3394713", "question": "None", ' \
        '"maxScore": 3.0, "stdScore": 2, "userAnswerContent": [{"id": 0, "text": "用了比喻的修辞' \
        '手法，把小河比作镜、绸、母亲，写出了 小河的喜爱之情。"}], "rightAnswerContent": [{"id": 0, "' \
        'text": "画线句子使用了比喻的手法。将河水比作明镜和绸缎，流水声比作母亲的呢喃，生动形象地写出了秦岭' \
        '自然风光美丽动人，", "score": 1.0, "keyWord": ""}, {"id": 1, "text": "为下文小女孩的出场作' \
        '铺垫。", "score": 1.0, "keyWord": ""}, {"id": 2, "text": "表达了作者漫步秦岭时的愉悦心情，' \
        '表现了秦岭深处美好的景色。 ", "score": 1.0, "keyWord": ""}]}'
"""
输入主观题的json字符串，进行打分，打分后输出json字符串
"""
input1 = '{"userId":"stu1","liveId":"live1","deviceId":0,"gradeType":9,"questionId":"1974977","question":"2. 阅读下面的宋词，完成下列小题。\n 清平乐·检校山园书所见 \n 辛弃疾 \n连云松竹，万事从今足。拄杖东家分社肉，白酒床头初熟。\n 西风梨枣山园，儿童偷把长竿。莫遣旁人惊去，老夫静处闲看。","questionType":"这首词抒发了作者哪些情感？","maxScore":1.0,"multiAnswerType":1,"userAnswerContent":[{"id":0,"text":"抒发了作者闲适，对乡村生活的喜爱之情，对松竹的喜爱之情。"}],"rightAnswerContent":[{"id":0,"text":"①对松竹的赞赏之情；","score":1,"keyWord":""},{"id":1,"text":"②对生活的满足之情；","score":1,"keyWord":""}]}'
input2 = '{"userId": "12345","gradeType": 8,"questionId": "3394713","question": "None","maxScore": 3.0,"stdScore": 2,"userAnswerContent": [{"id": 0,"text": "用了比喻的修辞手法，把小河比作镜、绸、母亲，写出了 小河的喜爱之情。"}],"rightAnswerContent": [{"id": 0,"text": "画线句子使用了比喻的手法。将河水比作明镜和绸缎，流水声比作母亲的呢喃，生动形象地写出了秦岭自然风光美丽动人，","score": 1.0,"keyWord": ""}, {"id": 1,"text": "为下文小女孩的出场作铺垫。","score": 1.0,"keyWord": ""}, {"id": 2,"text": "表达了作者漫步秦岭时的愉悦心情，表现了秦岭深处美好的景色。 ","score": 1.0,"keyWord": ""}]}'
input3 = '{"multiAnswerType":3, "userId": "stu1", "question": "2. 阅读下面的宋词，完成下列小题。\\n 清平乐·检校山园书所见 \\n 辛弃疾 \\n连云松竹，万事从今足。拄杖东家分社肉，白酒床头初熟。\\n 西风梨枣山园，儿童偷把长竿。莫遣旁人惊去，老夫静处闲看。","maxScore": 1.0,"questionId": "1974977","gradeType": 9,  "rightAnswerContent": [{"score": 1, "id": 0, "text": "①对松竹的赞赏之情；"}, {"score": 1, "id": 1, "text": "②对生活的满足之情；"}],"userAnswerContent": [{"id": 0, "text": "抒发了作者闲适，对乡村生活的喜爱之情，对松竹的喜爱之情。"}]}'
# output = cSubjectScorer.Score(input)
# output1 = cSubjectScorer.Score(input1)a
# inp = input()
# output2 = cSubjectScorer.Score(input0)
# print(output)
# print(cSubjectScorer.Score(input3))
# print(output2)

querys = [input0, input2]
def batch_query(querys):
    tmp = []
    for q in querys:
        res = ast.literal_eval(cSubjectScorer.Score(q))
        if(res["code"] == 300034020):
            tmp.append(res["data"]["totalScore"])
    return tmp

print(batch_query(querys))
"""
{"code": 300034020, "msg": "success", "requestId": "", "data": {"totalScore": 1, "userAnswerContent":
 [{"id": 0, "text": "用了比喻的修辞手法，把小河比作镜、绸、母亲，写出了 小河的喜爱之情。", "score": 1.0, 
 "matchedAnswerInfo": ["画线句子使用了比喻的手法。将河水比作明镜和绸缎，流水声比作母亲的呢喃，生动形象地写出了秦岭自
 然风光美丽动人，"]}]}}


code	msg	解释
300034020	success	调用成功
300034021	init failed	初始化失败
300034022	json lack info	json必填项缺失
300034023	score failed	批改失败

"""
