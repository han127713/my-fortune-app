# -*- coding: utf-8 -*-
import json
import random
from flask import Flask, request

app = Flask(__name__)

# 讀取資料庫
def load_fortunes():
    with open('fortunes.json', 'r', encoding='utf-8') as f:
        return json.load(f)

@app.route('/')
def home():
    fortunes = load_fortunes()
    
    # 這裡會隨機選出所有類別的籤，讓前端顯示
    pick = random.choice(fortunes)
    
    return f"""
    <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>人生指引抽籤筒</title>
            <style>
                body {{ font-family: "Microsoft JhengHei", sans-serif; background-color: #fff5f5; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; }}
                .container {{ text-align: center; background: white; padding: 40px; border-radius: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); max-width: 400px; width: 90%; }}
                
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
            </style>
        </head>
        <body>
            <div class="container">
                <div id="intro">
                    <h1 style="color:#d9534f;">🏮 心誠則靈 🏮</h1>
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
                    <button class="reload-btn" onclick="location.reload()">再次求籤</button>
                </div>
            </div>

            <script>
                const allFortunes = {json.dumps(fortunes, ensure_ascii=False)};

                function startDraw(category) {{
                    const box = document.getElementById('fortune-box');
                    const intro = document.getElementById('intro');
                    const result = document.getElementById('result');
                    
                    // 1. 開始搖晃
                    box.classList.add('shake');
                    
                    // 2. 篩選對應分類的籤
                    const pool = allFortunes.filter(f => f.category === category);
                    const pick = pool[Math.floor(Math.random() * pool.size)]; // 如果該分類沒籤會出錯，但我們補齊了
                    const finalPick = pool[Math.floor(Math.random() * pool.length)];

                    // 3. 延遲後顯示
                    setTimeout(function() {{
                        box.classList.remove('shake');
                        intro.style.display = 'none';
                        
                        document.getElementById('res-cat').innerText = "【問" + category + "】";
                        document.getElementById('res-type').innerText = finalPick.type;
                        document.getElementById('res-poetry').innerText = finalPick.poetry;
                        document.getElementById('res-meaning').innerText = finalPick.meaning;
                        
                        result.style.display = 'block';
                    }}, 1500);
                }}
            </script>
        </body>
    </html>
    """

if __name__ == '__main__':
    app.run(debug=True)

        
