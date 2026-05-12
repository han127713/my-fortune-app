# -*- coding: utf-8 -*-
import json
import random
import datetime
from flask import Flask

app = Flask(__name__)

# 載入籤詩資料
def load_fortunes():
    with open('fortunes.json', 'r', encoding='utf-8') as f:
        return json.load(f)

# 產生今日宜忌的函數
def get_daily_status():
    # 使用當天日期作為隨機種子，確保當天每個人看到的都一樣
    today_str = datetime.date.today().strftime('%Y-%m-%d')
    random.seed(today_str)
    
    yi_list = ["喝杯好茶", "散步運動", "閱讀好書", "與好友通話", "整理環境", "早睡早起", "多吃蔬果", "保持微笑"]
    ji_list = ["憂慮太多", "熬夜看劇", "生氣發火", "亂花錢", "吃太油膩", "猶豫不決", "久坐不動", "忘記喝水"]
    
    yi = random.sample(yi_list, 2)
    ji = random.sample(ji_list, 2)
    
    # 記得把隨機種子重設，以免影響後面的抽籤隨機性
    random.seed()
    return f"宜：{'、'.join(yi)} | 忌：{'、'.join(ji)}"

@app.route('/')
def home():
    fortunes = load_fortunes()
    daily_status = get_daily_status()
    today_date = datetime.date.today().strftime('%m月%d日')
    
    return f"""
    <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>人生指引抽籤筒</title>
            <style>
                body {{ font-family: "Microsoft JhengHei", sans-serif; background-color: #fff5f5; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; overflow-x: hidden; }}
                .container {{ text-align: center; background: white; padding: 40px; border-radius: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); max-width: 400px; width: 90%; position: relative; z-index: 10; }}
                
                .daily-box {{ background: #fff1f0; border: 1px solid #ffccc7; padding: 10px; border-radius: 10px; margin-bottom: 20px; font-size: 14px; color: #cf1322; }}
                
                #fortune-box {{ font-size: 100px; cursor: pointer; display: inline-block; transition: transform 0.1s; margin: 20px 0; }}
                .shake {{ animation: shake-animation 0.5s infinite; }}
                @keyframes shake-animation {{
                    0% {{ transform: translate(0, 0) rotate(0deg); }}
                    25% {{ transform: translate(5px, 5px) rotate(5deg); }}
                    50% {{ transform: translate(0, 0) rotate(0deg); }}
                    75% {{ transform: translate(-5px, 5px) rotate(-5deg); }}
                    100% {{ transform: translate(0, 0) rotate(0deg); }}
                }}

                .btn-group {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 20px; }}
                .category-btn {{ background: white; border: 2px solid #d9534f; color: #d9534f; padding: 12px; border-radius: 15px; cursor: pointer; font-size: 16px; font-weight: bold; transition: 0.3s; }}
                .category-btn:hover {{ background: #d9534f; color: white; }}

                #result {{ display: none; border-top: 3px double #d9534f; margin-top: 20px; padding-top: 20px; }}
                h2 {{ color: #d9534f; margin: 10px 0; }}
                .poetry {{ font-size: 22px; font-weight: bold; color: #333; margin: 15px 0; line-height: 1.5; }}
                .meaning {{ font-size: 16px; color: #666; background: #fef2f2; padding: 15px; border-radius: 10px; }}
                .reload-btn {{ background: #d9534f; color: white; border: none; padding: 12px 25px; border-radius: 10px; cursor: pointer; margin-top: 20px; }}

                .confetti {{ position: fixed; width: 10px; height: 10px; background-color: #f2d74e; top: -10px; z-index: 1; animation: fall 3s linear forwards; }}
                @keyframes fall {{ to {{ transform: translateY(100vh) rotate(720deg); }} }}
            </style>
        </head>
        <body>
            <div class="container">
                <div id="intro">
                    <h1 style="color:#d9534f; margin-bottom:5px;">🏮 心誠則靈 🏮</h1>
                    <div class="daily-box">
                        <strong>📅 {today_date} 今日提醒</strong><br>
                        {daily_status}
                    </div>
                    <p>請先默念您的問題，再選擇分類</p>
                    <div id="fortune-box">🧧</div>
                    <div class="btn-group">
                        <button class="category-btn" onclick="startDraw('運勢')">今日運勢</button>
                        <button class="category-btn" onclick="startDraw('學業')">學業進展</button>
                        <button class="category-btn" onclick="startDraw('感情')">感情緣分</button>
                        <button class="category-btn" onclick="startDraw('健康')">身體健康</button>
                    </div>
                </div>

                <div id="result">
                    <p id="res-cat" style="color:#888; font-weight:bold;"></p>
                    <h2 id="res-type"></h2>
                    <div class="poetry" id="res-poetry"></div>
                    <div class="meaning" id="res-meaning"></div>
                    <button class="reload-btn" onclick="location.reload()">返回首頁</button>
                </div>
            </div>

            <script>
                const allFortunes = {json.dumps(fortunes, ensure_ascii=False)};

                function createConfetti() {{
                    const colors = ['#f2d74e', '#95c3de', '#ff9a91', '#f2ceff', '#aeed91'];
                    for (let i = 0; i < 50; i++) {{
                        const confetti = document.createElement('div');
                        confetti.className = 'confetti';
                        confetti.style.left = Math.random() * 100 + 'vw';
                        confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
                        confetti.style.animationDelay = Math.random() * 2 + 's';
                        document.body.appendChild(confetti);
                        setTimeout(() => confetti.remove(), 5000);
                    }}
                }}

                function startDraw(category) {{
                    const box = document.getElementById('fortune-box');
                    const intro = document.getElementById('intro');
                    const result = document.getElementById('result');
                    
                    box.classList.add('shake');
                    
                    const pool = allFortunes.filter(f => f.category === category);
                    const finalPick = pool[Math.floor(Math.random() * pool.length)];

                    setTimeout(function() {{
                        box.classList.remove('shake');
                        intro.style.display = 'none';
                        
                        document.getElementById('res-cat').innerText = "【問" + category + "】";
                        document.getElementById('res-type').innerText = finalPick.type;
                        document.getElementById('res-poetry').innerText = finalPick.poetry;
                        document.getElementById('res-meaning').innerText = finalPick.meaning;
                        
                        result.style.display = 'block';

                        if (finalPick.type === "大吉" || finalPick.type === "中吉") {{
                            createConfetti();
                        }}
                    }}, 1500);
                }}
            </script>
        </body>
    </html>
    """

if __name__ == '__main__':
    app.run(debug=True)


        
