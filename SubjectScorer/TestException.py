from SubjectScorer import cSubjectScorer

print("正常输入")
# input = '{"userId": "12345", "gradeType": 8, "questionId": "3394713", "question": "None", ' \
#         '"maxScore": 3.0, "stdScore": 2, "userAnswerContent": [{"id": 0, "text": "用了比喻的修辞' \
#         '手法，把小河比作镜、绸、母亲，写出了 小河的喜爱之情。"}], "rightAnswerContent": [{"id": 0, "' \
#         'text": "画线句子使用了比喻的手法。将河水比作明镜和绸缎，流水声比作母亲的呢喃，生动形象地写出了秦岭' \
#         '自然风光美丽动人，", "score": 1.0, "keyWord": ""}, {"id": 1, "text": "为下文小女孩的出场作' \
#         '铺垫。", "score": 1.0, "keyWord": ""}, {"id": 2, "text": "表达了作者漫步秦岭时的愉悦心情，' \
#         '表现了秦岭深处美好的景色。 ", "score": 1.0, "keyWord": ""}]}'
input = '{"userId":"12345","gradeType":8,"questionId":"3394713","question":"None","maxScore":3.0,"stdScore":2,"userAnswerContent":[{"id":0,"text":"用了比喻的修辞手法，把小河比作镜、绸、母亲，写出了 小河的喜爱之情。"}],"rightAnswerContent":[{"id":0,"text":"画线句子使用了比喻的手法。将河水比作明镜和绸缎，流水声比作母亲的呢喃，生动形象地写出了秦岭自然风光美丽动人，","score":1.0,"keyWord":""},{"id":1,"text":"为下文小女孩的出场作铺垫。","score":1.0,"keyWord":""},{"id":2,"text":"表达了作者漫步秦岭时的愉悦心情，表现了秦岭深处美好的景色。 ","score":1.0,"keyWord":""}]}'
output = cSubjectScorer.Score(input)
print(output)

print("学生作答为空")
input = '{"userId":"12345","gradeType":8,"questionId":"3394713","question":"None","maxScore":3.0,"stdScore":2,"userAnswerContent":[{"id":0,"text":""}],"rightAnswerContent":[{"id":0,"text":"画线句子使用了比喻的手法。将河水比作明镜和绸缎，流水声比作母亲的呢喃，生动形象地写出了秦岭自然风光美丽动人，","score":1.0,"keyWord":""},{"id":1,"text":"为下文小女孩的出场作铺垫。","score":1.0,"keyWord":""},{"id":2,"text":"表达了作者漫步秦岭时的愉悦心情，表现了秦岭深处美好的景色。 ","score":1.0,"keyWord":""}]}'
output = cSubjectScorer.Score(input)
print(output)

print("标答为空")
input = '{"userId":"12345","gradeType":8,"questionId":"3394713","question":"None","maxScore":3.0,"stdScore":2,"userAnswerContent":[{"id":0,"text":"用了比喻的修辞手法，把小河比作镜、绸、母亲，写出了 小河的喜爱之情。"}],"rightAnswerContent":[{"id":0,"text":"","score":1.0,"keyWord":""},{"id":1,"text":"为下文小女孩的出场作铺垫。","score":1.0,"keyWord":""},{"id":2,"text":"表达了作者漫步秦岭时的愉悦心情，表现了秦岭深处美好的景色。 ","score":1.0,"keyWord":""}]}'
output = cSubjectScorer.Score(input)
print(output)


print("userId为空")
input = '{"userId":"","liveId":"live1","deviceId":0,"gradeType":9,"questionId":"1974977","question":"2. 阅读下面的宋词，完成下列小题。\n 清平乐·检校山园书所见 \n 辛弃疾 \n连云松竹，万事从今足。拄杖东家分社肉，白酒床头初熟。\n 西风梨枣山园，儿童偷把长竿。莫遣旁人惊去，老夫静处闲看。","questionType":"这首词抒发了作者哪些情感？","maxScore":1.0,"multiAnswerType":1,"userAnswerContent":[{"id":0,"text":"抒发了作者闲适，对乡村生活的喜爱之情，对松竹的喜爱之情。"}],"rightAnswerContent":[{"id":0,"text":"①对松竹的赞赏之情；","score":1,"keyWord":""},{"id":1,"text":"②对生活的满足之情；","score":1,"keyWord":""}]}'
output = cSubjectScorer.Score(input)
print(output)

print("正常输入")
input = '{"userId":"12345","gradeType":8,"questionId":"3394713","question":"None","maxScore":3.0,"stdScore":2,"userAnswerContent":[{"id":0,"text":"用了比喻的修辞手法，把小河比作镜、绸、母亲，写出了 小河的喜爱之情。"}],"rightAnswerContent":[{"id":0,"text":"画线句子使用了比喻的手法。将河水比作明镜和绸缎，流水声比作母亲的呢喃，生动形象地写出了秦岭自然风光美丽动人，","score":1.0,"keyWord":""},{"id":1,"text":"为下文小女孩的出场作铺垫。","score":1.0,"keyWord":""},{"id":2,"text":"表达了作者漫步秦岭时的愉悦心情，表现了秦岭深处美好的景色。 ","score":1.0,"keyWord":""}]}'
output = cSubjectScorer.Score(input)
print(output)

print("gradeType为空")
input = '{"userId": "12345","gradeType": ,"questionId": "3394713","question": "None","maxScore": 3.0,"stdScore": 2,"userAnswerContent": [{"id": 0,"text": "用了比喻的修辞手法，把小河比作镜、绸、母亲，写出了 小河的喜爱之情。"}],"rightAnswerContent": [{"id": 0,"text": "画线句子使用了比喻的手法。将河水比作明镜和绸缎，流水声比作母亲的呢喃，生动形象地写出了秦岭自然风光美丽动人，","score": 1.0,"keyWord": ""}, {"id": 1,"text": "为下文小女孩的出场作铺垫。","score": 1.0,"keyWord": ""}, {"id": 2,"text": "表达了作者漫步秦岭时的愉悦心情，表现了秦岭深处美好的景色。 ","score": 1.0,"keyWord": ""}]}'
output = cSubjectScorer.Score(input)
print(output)

print("gradeType为111")
input = '{"userId": "12345","gradeType": 111,"questionId": "3394713","question": "None","maxScore": 3.0,"stdScore": 2,"userAnswerContent": [{"id": 0,"text": "用了比喻的修辞手法，把小河比作镜、绸、母亲，写出了 小河的喜爱之情。"}],"rightAnswerContent": [{"id": 0,"text": "画线句子使用了比喻的手法。将河水比作明镜和绸缎，流水声比作母亲的呢喃，生动形象地写出了秦岭自然风光美丽动人，","score": 1.0,"keyWord": ""}, {"id": 1,"text": "为下文小女孩的出场作铺垫。","score": 1.0,"keyWord": ""}, {"id": 2,"text": "表达了作者漫步秦岭时的愉悦心情，表现了秦岭深处美好的景色。 ","score": 1.0,"keyWord": ""}]}'
output = cSubjectScorer.Score(input)
print(output)

print("gradeType为字符串")
input = '{"userId": "12345","gradeType": t,"questionId": "3394713","question": "None","maxScore": 3.0,"stdScore": 2,"userAnswerContent": [{"id": 0,"text": "用了比喻的修辞手法，把小河比作镜、绸、母亲，写出了 小河的喜爱之情。"}],"rightAnswerContent": [{"id": 0,"text": "画线句子使用了比喻的手法。将河水比作明镜和绸缎，流水声比作母亲的呢喃，生动形象地写出了秦岭自然风光美丽动人，","score": 1.0,"keyWord": ""}, {"id": 1,"text": "为下文小女孩的出场作铺垫。","score": 1.0,"keyWord": ""}, {"id": 2,"text": "表达了作者漫步秦岭时的愉悦心情，表现了秦岭深处美好的景色。 ","score": 1.0,"keyWord": ""}]}'
output = cSubjectScorer.Score(input)
print(output)

print("questionId错误输入为int")
input = '{"userId": "12345","gradeType": 8,"questionId": 88,"question": "None","maxScore": 3.0,"stdScore": 2,"userAnswerContent": [{"id": 0,"text": "用了比喻的修辞手法，把小河比作镜、绸、母亲，写出了 小河的喜爱之情。"}],"rightAnswerContent": [{"id": 0,"text": "画线句子使用了比喻的手法。将河水比作明镜和绸缎，流水声比作母亲的呢喃，生动形象地写出了秦岭自然风光美丽动人，","score": 1.0,"keyWord": ""}, {"id": 1,"text": "为下文小女孩的出场作铺垫。","score": 1.0,"keyWord": ""}, {"id": 2,"text": "表达了作者漫步秦岭时的愉悦心情，表现了秦岭深处美好的景色。 ","score": 1.0,"keyWord": ""}]}'
output = cSubjectScorer.Score(input)
print(output)

print("question输入为int")
input = '{"userId": "12345","gradeType": 8,"questionId": "3394713","question": 8,"maxScore": 3.0,"stdScore": 2,"userAnswerContent": [{"id": 0,"text": "用了比喻的修辞手法，把小河比作镜、绸、母亲，写出了 小河的喜爱之情。"}],"rightAnswerContent": [{"id": 0,"text": "画线句子使用了比喻的手法。将河水比作明镜和绸缎，流水声比作母亲的呢喃，生动形象地写出了秦岭自然风光美丽动人，","score": 1.0,"keyWord": ""}, {"id": 1,"text": "为下文小女孩的出场作铺垫。","score": 1.0,"keyWord": ""}, {"id": 2,"text": "表达了作者漫步秦岭时的愉悦心情，表现了秦岭深处美好的景色。 ","score": 1.0,"keyWord": ""}]}'
output = cSubjectScorer.Score(input)
print(output)

print("question输入题干测试")
input = '{"userId": "12345","gradeType": 8,"questionId": "3394713","question": "阅读材料【B】，说说“天舟一号”要完成哪些任务。（三点，每点1分，共3分）","maxScore": 3.0,"stdScore": 2,"userAnswerContent": [{"id": 0,"text": "用了比喻的修辞手法，把小河比作镜、绸、母亲，写出了 小河的喜爱之情。"}],"rightAnswerContent": [{"id": 0,"text": "画线句子使用了比喻的手法。将河水比作明镜和绸缎，流水声比作母亲的呢喃，生动形象地写出了秦岭自然风光美丽动人，","score": 1.0,"keyWord": ""}, {"id": 1,"text": "为下文小女孩的出场作铺垫。","score": 1.0,"keyWord": ""}, {"id": 2,"text": "表达了作者漫步秦岭时的愉悦心情，表现了秦岭深处美好的景色。 ","score": 1.0,"keyWord": ""}]}'
output = cSubjectScorer.Score(input)
print(output)

print("总分为int")
input = '{"userId": "12345","gradeType": 8,"questionId": "3394713","question": "None","maxScore": 3,"stdScore": 2,"userAnswerContent": [{"id": 0,"text": "用了比喻的修辞手法，把小河比作镜、绸、母亲，写出了 小河的喜爱之情。"}],"rightAnswerContent": [{"id": 0,"text": "画线句子使用了比喻的手法。将河水比作明镜和绸缎，流水声比作母亲的呢喃，生动形象地写出了秦岭自然风光美丽动人，","score": 1.0,"keyWord": ""}, {"id": 1,"text": "为下文小女孩的出场作铺垫。","score": 1.0,"keyWord": ""}, {"id": 2,"text": "表达了作者漫步秦岭时的愉悦心情，表现了秦岭深处美好的景色。 ","score": 1.0,"keyWord": ""}]}'
output = cSubjectScorer.Score(input)
print(output)

print("总分为字符串")
input = '{"userId": "12345","gradeType": 8,"questionId": "3394713","question": "None","maxScore": "","stdScore": 2,"userAnswerContent": [{"id": 0,"text": "用了比喻的修辞手法，把小河比作镜、绸、母亲，写出了 小河的喜爱之情。"}],"rightAnswerContent": [{"id": 0,"text": "画线句子使用了比喻的手法。将河水比作明镜和绸缎，流水声比作母亲的呢喃，生动形象地写出了秦岭自然风光美丽动人，","score": 1.0,"keyWord": ""}, {"id": 1,"text": "为下文小女孩的出场作铺垫。","score": 1.0,"keyWord": ""}, {"id": 2,"text": "表达了作者漫步秦岭时的愉悦心情，表现了秦岭深处美好的景色。 ","score": 1.0,"keyWord": ""}]}'
output = cSubjectScorer.Score(input)
print(output)

print("multiAnswerType 1")
input = '{"multiAnswerType" : 1, "userId": "12345","gradeType": 8,"questionId": "3394713","question": "None","maxScore": 3.0,"stdScore": 2,"userAnswerContent": [{"id": 0,"text": "用了比喻的修辞手法，把小河比作镜、绸、母亲，写出了 小河的喜爱之情。"}],"rightAnswerContent": [{"id": 0,"text": "画线句子使用了比喻的手法。将河水比作明镜和绸缎，流水声比作母亲的呢喃，生动形象地写出了秦岭自然风光美丽动人，","score": 1.0,"keyWord": ""}, {"id": 1,"text": "为下文小女孩的出场作铺垫。","score": 1.0,"keyWord": ""}, {"id": 2,"text": "表达了作者漫步秦岭时的愉悦心情，表现了秦岭深处美好的景色。 ","score": 1.0,"keyWord": ""}]}'
output = cSubjectScorer.Score(input)
print(output)

print("userAnswerContent 为空")
input = '{"userId": "12345","gradeType": 8,"questionId": "3394713","question": "None","maxScore": 3.0,"stdScore": 2,"userAnswerContent": [],"rightAnswerContent": [{"id": 0,"text": "画线句子使用了比喻的手法。将河水比作明镜和绸缎，流水声比作母亲的呢喃，生动形象地写出了秦岭自然风光美丽动人，","score": 1.0,"keyWord": ""}, {"id": 1,"text": "为下文小女孩的出场作铺垫。","score": 1.0,"keyWord": ""}, {"id": 2,"text": "表达了作者漫步秦岭时的愉悦心情，表现了秦岭深处美好的景色。 ","score": 1.0,"keyWord": ""}]}'
output = cSubjectScorer.Score(input)
print(output)

print("userAnswerContent 为整型")
input = '{"userId": "12345","gradeType": 8,"questionId": "3394713","question": "None","maxScore": 3.0,"stdScore": 2,"userAnswerContent": 5,"rightAnswerContent": [{"id": 0,"text": "画线句子使用了比喻的手法。将河水比作明镜和绸缎，流水声比作母亲的呢喃，生动形象地写出了秦岭自然风光美丽动人，","score": 1.0,"keyWord": ""}, {"id": 1,"text": "为下文小女孩的出场作铺垫。","score": 1.0,"keyWord": ""}, {"id": 2,"text": "表达了作者漫步秦岭时的愉悦心情，表现了秦岭深处美好的景色。 ","score": 1.0,"keyWord": ""}]}'
output = cSubjectScorer.Score(input)
print(output)

print("userAnswerContent 不存在")
input = '{"userId": "12345","gradeType": 8,"questionId": "3394713","question": "None","maxScore": 3.0,"stdScore": 2,"rightAnswerContent": [{"id": 0,"text": "画线句子使用了比喻的手法。将河水比作明镜和绸缎，流水声比作母亲的呢喃，生动形象地写出了秦岭自然风光美丽动人，","score": 1.0,"keyWord": ""}, {"id": 1,"text": "为下文小女孩的出场作铺垫。","score": 1.0,"keyWord": ""}, {"id": 2,"text": "表达了作者漫步秦岭时的愉悦心情，表现了秦岭深处美好的景色。 ","score": 1.0,"keyWord": ""}]}'
output = cSubjectScorer.Score(input)
print(output)

print("userAnswerContent 只有id，没有text")
input = '{"userId": "12345","gradeType": 8,"questionId": "3394713","question": "None","maxScore": 3.0,"stdScore": 2,"userAnswerContent": [{"id": 0}],"rightAnswerContent": [{"id": 0,"text": "画线句子使用了比喻的手法。将河水比作明镜和绸缎，流水声比作母亲的呢喃，生动形象地写出了秦岭自然风光美丽动人，","score": 1.0,"keyWord": ""}, {"id": 1,"text": "为下文小女孩的出场作铺垫。","score": 1.0,"keyWord": ""}, {"id": 2,"text": "表达了作者漫步秦岭时的愉悦心情，表现了秦岭深处美好的景色。 ","score": 1.0,"keyWord": ""}]}'
output = cSubjectScorer.Score(input)
print(output)

print("rightAnswerContent 只有text，没有id")
input = '{"userId": "12345","gradeType": 8,"questionId": "3394713","question": "None","maxScore": 3.0,"stdScore": 2,"userAnswerContent": [{"id": 0, "text": "用了比喻的修辞手法，把小河比作镜、绸、母亲，写出了 小河的喜爱之情。"}],"rightAnswerContent": [{"text": "画线句子使用了比喻的手法。将河水比作明镜和绸缎，流水声比作母亲的呢喃，生动形象地写出了秦岭自然风光美丽动人，","score": 1.0,"keyWord": ""}, {"id": 1,"text": "为下文小女孩的出场作铺垫。","score": 1.0,"keyWord": ""}, {"id": 2,"text": "表达了作者漫步秦岭时的愉悦心情，表现了秦岭深处美好的景色。 ","score": 1.0,"keyWord": ""}]}'
output = cSubjectScorer.Score(input)
print(output)

print("rightAnswerContent 为字符串")
input = '{"userId": "12345","gradeType": 8,"questionId": "3394713","question": "None","maxScore": 3.0,"stdScore": 2,"userAnswerContent": [{"id": 0,"text": "用了比喻的修辞手法，把小河比作镜、绸、母亲，写出了 小河的喜爱之情。"}],"rightAnswerContent": "str"}'
output = cSubjectScorer.Score(input)
print(output)

print("rightAnswerContent 缺失")
input = '{"userId": "12345","gradeType": 8,"questionId": "3394713","question": "None","maxScore": 3.0,"stdScore": 2,"userAnswerContent": [{"id": 0,"text": "用了比喻的修辞手法，把小河比作镜、绸、母亲，写出了 小河的喜爱之情。"}]}'
output = cSubjectScorer.Score(input)
print(output)


print("rightAnswerContent 采分点得分为0")
input = '{"userId":"12345","gradeType":8,"questionId":"3394713","question":"None","maxScore":3.0,"stdScore":2,"userAnswerContent":[{"id":0,"text":"用了比喻的修辞手法，把小河比作镜、绸、母亲，写出了 小河的喜爱之情。"}],"rightAnswerContent":[{"id":0,"text":"画线句子使用了比喻的手法。将河水比作明镜和绸缎，流水声比作母亲的呢喃，生动形象地写出了秦岭自然风光美丽动人，","score":0,"keyWord":""},{"id":1,"text":"为下文小女孩的出场作铺垫。","score":1.0,"keyWord":""},{"id":2,"text":"表达了作者漫步秦岭时的愉悦心情，表现了秦岭深处美好的景色。 ","score":1.0,"keyWord":""}]}'
output = cSubjectScorer.Score(input)
print(output)

print("最大分为负值")
input = '{"userId":"12345","gradeType":8,"questionId":"3394713","question":"None","maxScore":-3.0,"stdScore":2,"userAnswerContent":[{"id":0,"text":"用了比喻的修辞手法，把小河比作镜、绸、母亲，写出了 小河的喜爱之情。"}],"rightAnswerContent":[{"id":0,"text":"画线句子使用了比喻的手法。将河水比作明镜和绸缎，流水声比作母亲的呢喃，生动形象地写出了秦岭自然风光美丽动人，","score":1.0,"keyWord":""},{"id":1,"text":"为下文小女孩的出场作铺垫。","score":1.0,"keyWord":""},{"id":2,"text":"表达了作者漫步秦岭时的愉悦心情，表现了秦岭深处美好的景色。 ","score":1.0,"keyWord":""}]}'
output = cSubjectScorer.Score(input)
print(output)

print("-----back up ----")
input = '{"userId":"12345","gradeType":8,"questionId":"3394713","question":"None","maxScore":3.0,"stdScore":2,"userAnswerContent":[{"id":0,"text":"用了比喻的修辞手法，把小河比作镜、绸、母亲，写出了 小河的喜爱之情。"}],"rightAnswerContent":[{"id":0,"text":"画线句子使用了比喻的手法。将河水比作明镜和绸缎，流水声比作母亲的呢喃，生动形象地写出了秦岭自然风光美丽动人，","score":1.0,"keyWord":""},{"id":1,"text":"为下文小女孩的出场作铺垫。","score":1.0,"keyWord":""},{"id":2,"text":"表达了作者漫步秦岭时的愉悦心情，表现了秦岭深处美好的景色。 ","score":1.0,"keyWord":""}]}'
output = cSubjectScorer.Score(input)
print(output)
