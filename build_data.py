# 把 data/*.json 合併成 data/questions.js（讓 index.html 可直接雙擊開啟，不需要伺服器）
import json
a=json.load(open('data/airport_questions.json',encoding='utf-8'))
cs=[]
for f in ['countries_batch1','countries_batch2','countries_batch3']:
    cs+=json.load(open(f'data/{f}.json',encoding='utf-8'))['countries']
js='window.DATA='+json.dumps({'stages':a['stages'],'countries':cs,'verified_on':a['meta']['verified_on']},ensure_ascii=False)+';'
open('data/questions.js','w',encoding='utf-8').write(js)
print(len(a['stages']),'stages',len(cs),'countries')
