# 產生報告用的概念圖（需要 Pillow 與 Noto Sans CJK 字型）
from PIL import Image, ImageDraw, ImageFont
FP='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
F=lambda s:ImageFont.truetype(FP,s,index=3)
Y,B,LB,G,R,W='#ffd400','#14305c','#dbe9ff','#e3f5dc','#ffe0e0','#ffffff'
def canvas(title,sub=''):
    im=Image.new('RGB',(1600,900),'#f6f8fb');d=ImageDraw.Draw(im)
    d.rectangle([0,0,1600,90],fill=B);d.text((40,18),title,font=F(46),fill=W)
    if sub:d.text((40,100),sub,font=F(26),fill='#556')
    return im,d
def tx(d,cx,cy,t,fs=28,fill=B):
    ls=t.split('\n');h=fs*1.35;y=cy-h*len(ls)/2
    for l in ls:
        w=d.textlength(l,font=F(fs));d.text((cx-w/2,y),l,font=F(fs),fill=fill);y+=h
def box(d,cx,cy,w,h,t,fill=LB,fs=28,ol=B):
    d.rounded_rectangle([cx-w/2,cy-h/2,cx+w/2,cy+h/2],18,fill=fill,outline=ol,width=3);tx(d,cx,cy,t,fs)
def dia(d,cx,cy,w,h,t,fill=Y,fs=28):
    d.polygon([(cx,cy-h/2),(cx+w/2,cy),(cx,cy+h/2),(cx-w/2,cy)],fill=fill,outline=B,width=3);tx(d,cx,cy,t,fs)
def arrow(d,pts,label=None,fs=24,col=B):
    for a,b in zip(pts,pts[1:]):d.line([a,b],fill=col,width=5)
    (x0,y0),(x1,y1)=pts[-2],pts[-1]
    import math;an=math.atan2(y1-y0,x1-x0)
    d.polygon([(x1,y1),(x1-22*math.cos(an-.4),y1-22*math.sin(an-.4)),(x1-22*math.cos(an+.4),y1-22*math.sin(an+.4))],fill=col)
    if label:
        mx,my=(pts[0][0]+pts[1][0])/2,(pts[0][1]+pts[1][1])/2;d.text((mx+8,my-34),label,font=F(fs),fill='#b00020')

# 1 遊戲流程
im,d=canvas('圖 1　遊戲整體流程（真實出境動線）','前一關沒通過，下一關的柵欄不會打開；每關 3 顆愛心，答錯扣血，歸零只重打該關')
S=[('① 出發前準備','旅遊諮詢員 Bob','選目的地＋2 題'),('② 報到劃位','報到櫃檯人員 Dave','6 題抽 3'),('③ 託運行李','行李地勤員 Carl','9 題抽 3'),('④ 安全檢查','安檢員 Mel','7 題抽 3'),
   ('⑤ 證照查驗','移民官 Tim','7 題抽 3'),('⑥ 免稅店','免稅店店員 Stuart','4 題抽 3'),('⑦ 登機門','登機門地勤 Kevin','3 題'),('⑧ 機艙內','空服員 Phil','8 題抽 3')]
xs=[230,590,950,1310];P=[]
for i,(a,b,c) in enumerate(S):
    cx=xs[i] if i<4 else xs[7-i];cy=330 if i<4 else 620
    box(d,cx,cy,300,170,f'{a}\n{b}\n{c}',fill=Y if i==0 else LB,fs=28);P.append((cx,cy))
for i in range(3):arrow(d,[(P[i][0]+150,P[i][1]),(P[i+1][0]-150,P[i+1][1])])
arrow(d,[(P[3][0],P[3][1]+85),(P[4][0],P[4][1]-85)])
for i in range(4,7):arrow(d,[(P[i][0]-150,P[i][1]),(P[i+1][0]+150,P[i+1][1])])
box(d,260,180,440,70,'選角：Gru／Agnes／Edith／Margo',fill=G,fs=24);arrow(d,[(230,215),(230,242)])
box(d,230,790,330,90,'旅途平安祝福\n產生「出境手冊」',fill=G,fs=26);arrow(d,[(P[7][0],P[7][1]+85),(P[7][0],745)])
d.text((700,760),'出境手冊內容：\n旅客、目的地、日期、每關題目與解析、\n資料來源（可列印／存成 PDF）',font=F(26),fill=B)
im.save('docs/images/01_game_flow.png')

# 2 答題機制
im,d=canvas('圖 2　單一關卡的答題機制','愛心扣完只重打該關，不會從頭開始')
A,Bn,C,Dd,E,Gb,H,I,J=(160,450),(480,450),(800,450),(1100,450),(1100,190),(1100,640),(1100,810),(800,810),(1420,810)
box(d,*A,230,110,'走近小小兵\n按空白鍵',fill=Y,fs=26);box(d,*Bn,250,120,'隨機抽 3 題\n（優先沒遇過的）',fs=26);box(d,*C,230,110,'玩家選擇答案\n（滑鼠或數字鍵）',fs=26)
dia(d,*Dd,220,150,'答對？');box(d,*E,380,120,'小小兵鼓勵＋補充知識\n最後一題→柵欄打開',fill=G,fs=26);box(d,*Gb,330,110,'扣 1 顆愛心\n耐心解釋為什麼錯',fill=R,fs=26)
dia(d,*H,220,130,'愛心=0？');box(d,*I,260,110,'只重打該關\n（愛心恢復 3 顆）',fill=R,fs=24);box(d,*J,260,110,'再試一次\n（錯誤選項反灰）',fs=24)
arrow(d,[(275,450),(355,450)]);arrow(d,[(605,450),(685,450)]);arrow(d,[(915,450),(990,450)])
arrow(d,[(1100,375),(1100,250)],'是');arrow(d,[(1100,525),(1100,585)],'否')
arrow(d,[(1100,695),(1100,745)]);arrow(d,[(990,810),(930,810)],'是');arrow(d,[(1210,810),(1290,810)],'否')
arrow(d,[(935,190),(480,190),(480,390)],'下一題')
arrow(d,[(1420,755),(1420,330),(800,330),(800,395)])
arrow(d,[(670,810),(480,810),(480,510)])
im.save('docs/images/02_question_loop.png')

# 3 系統架構
im,d=canvas('圖 3　系統架構（純靜態網頁，無後端、無 API Key）','可雙擊 index.html 本機開啟，也可放上 GitHub Pages')
box(d,800,190,760,62,'玩家（瀏覽器：Chrome／Edge／Safari）',fill=Y,fs=28)
d.rounded_rectangle([200,250,1400,590],24,fill='#eaf1fb',outline=B,width=4);d.text((230,262),'index.html（單一檔案：HTML + CSS + JavaScript）',font=F(30),fill=B)
for (cx,cy,t) in [(430,390,'Canvas 2D\n地圖、角色、路人\n柵欄、地面標線'),(800,390,'DOM 介面\n對話框、選項按鈕\n出境手冊'),(1170,390,'遊戲邏輯\n關卡鎖定、愛心\n抽題與計分')]:box(d,cx,cy,320,130,t,fill=W,fs=26)
box(d,800,525,640,60,'localStorage：記住答過的題目（下次優先抽新題）',fill=G,fs=24)
arrow(d,[(800,221),(800,250)])
box(d,330,740,420,110,'data/questions.js\n（由 build_data.py 合併產生）',fs=26);box(d,330,870,0,0,'')
box(d,800,740,380,110,'assets/characters/*.png\n12 張去背角色圖\nassets/bg/title.jpg',fs=24);box(d,1250,740,420,110,'部署：GitHub Pages\n或本機直接開啟',fill=G,fs=26)
for x in (330,800):arrow(d,[(x,685),(x,590)])
box(d,330,860,420,60,'data/*.json　題庫＋來源＋查證日期',fill=Y,fs=22);arrow(d,[(330,830),(330,795)])
d.text((1030,806),'技術：HTML5 Canvas・JavaScript・JSON\nPython：合併題庫、去背、畫概念圖\nPlaywright：自動通關測試',font=F(21),fill=B)
im.save('docs/images/03_architecture.png')

# 4 內容製作流程
im,d=canvas('圖 4　生成式 AI 協作流程（文字、圖像、程式）','AI 負責生成與查證，人負責決策、審閱與取捨')
lanes=[('文字：題庫',[('設計關卡與規格','（我）'),('Claude 網路搜尋\n官方／權威來源'),('生成題目 JSON\n題目、選項、解析、來源'),('標記 recheck\n與過期日期'),('人工審閱\n合併進遊戲')]),
('圖像：角色與場景',[('蒐集小小兵圖片','（我）'),('Python 程式去背\n連通區域演算法'),('目視檢查發現\n護目鏡被誤刪'),('調整門檻\n重新去背'),('放入 assets\n地圖用 Canvas 繪製')]),
('程式：vibe coding',[('用自然語言\n描述需求（我）'),('Claude 撰寫\nHTML/JS 程式'),('Playwright\n自動通關測試'),('截圖檢查畫面\n發現問題'),('回饋修改\n再次測試')])]
for r,(n,items) in enumerate(lanes):
    y=250+r*250;d.rounded_rectangle([40,y-90,1560,y+90],20,fill=['#eef6ff','#fff6dc','#eaf8ea'][r],outline='#b9c6d8',width=2);d.text((60,y-84),n,font=F(26),fill='#b00020')
    for k,t in enumerate(items):
        t='\n'.join(t) if isinstance(t,tuple) else t;cx=190+k*300;box(d,cx,y+15,250,110,t,fill=W,fs=22)
        if k:arrow(d,[(cx-150,y+15),(cx-125-0,y+15)] if False else [(cx-157,y+15),(cx-127,y+15)])
im.save('docs/images/04_ai_workflow.png')
print('ok')
