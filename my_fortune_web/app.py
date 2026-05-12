# -*- coding: utf-8 -*-
import json
import random
from flask import Flask

app = Flask(__name__)

def get_fortune():
    with open('fortunes.json', 'r', encoding='utf-8') as f:
        fortunes = json.load(f)
    return random.choice(fortunes)

@app.route('/')
def home():
    pick = get_fortune()
    return f"""
    <html>
        <head>
            <meta charset="utf-8">
            <title>50籤運勢網站</title>
            <style>
                body {{ font-family: "Microsoft JhengHei", sans-serif; background-color: #f7f7f7; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }}
                .container {{ text-align: center; }}
                
                /* 籤筒的樣子 */
                #fortune-box {{
                    font-size: 80px;
                    cursor: pointer;
                    display: inline-block;
                    transition: transform 0.1s;
                }}

                /* 搖晃動畫設定 */
                .shake {{
                    animation: shake-animation 0.5s infinite;
                }}

                @keyframes shake-animation {{
                    0% {{ transform: translate(0, 0) rotate(0deg); }}
                    25% {{ transform: translate(5px, 5px) rotate(5deg); }}
                    50% {{ transform: translate(0, 0) rotate(0deg); }}
                    75% {{ transform: translate(-5px, 5px) rotate(-5deg); }}
                    100% {{ transform: translate(0, 0) rotate(0deg); }}
                }}

                /* 隱藏結果，等搖完再顯示 */
                #result {{
                    display: none;
                    background: white;
                    padding: 30px;
                    border-radius: 20px;
                    box-shadow: 0 10px 20px rgba(0,0,0,0.1);
                    border: 3px solid #d9534f;
                }}

                h2 {{ color: #d9534f; margin-top: 0; }}
                .poetry {{ font-size: 24px; font-weight: bold; margin: 20px 0; letter-spacing: 2px; }}
                button {{ background: #d9534f; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-size: 16px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <!-- 初始顯示的籤筒 -->
                <div id="intro">
                    <h1>🔮 誠心求一籤 🔮</h1>
                    <div id="fortune-box" onclick="startShake()">🧧</div>
                    <p>點擊籤筒開始抽籤</p>
                </div>

                <!-- 抽籤結果 -->
                <div id="result">
                    <h2>【{pick['type']}】</h2>
                    <p>第 {pick['id']} 籤</p>
                    <div class="poetry">{pick['poetry']}</div>
                    <p>解釋：{pick['meaning']}</p>
                    <button onclick="location.reload()">重新求籤</button>
                </div>
            </div>

            <script>
                function startShake() {{
                    var box = document.getElementById('fortune-box');
                    var intro = document.getElementById('intro');
                    var result = document.getElementById('result');

                    // 1. 開始搖晃
                    box.classList.add('shake');
                    
                    // 2. 搖晃 1.5 秒後執行
                    setTimeout(function() {{
                        box.classList.remove('shake');
                        intro.style.display = 'none'; // 隱藏籤筒
                        result.style.display = 'block'; // 顯示結果
                    }}, 1500);
                }}
            </script>
        </body>
    </html>
    """

if __name__ == '__main__':
    app.run(debug=True)