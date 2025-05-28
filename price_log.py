import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

# -------------------------------
# ① 価格.comの商品ページURL
# -------------------------------
URL = "https://kakaku.com/item/K0001382801/"  # ← 他の商品ページに変更OK
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# -------------------------------
# ② スクレイピングで価格を取得
# -------------------------------
res = requests.get(URL, headers=HEADERS)
soup = BeautifulSoup(res.content, "html.parser")

# 最安価格の取得
price_tag = soup.select_one(".priceTxt")
if price_tag:
    price_text = price_tag.get_text(strip=True).replace("¥", "").replace(",", "")
    price = int(price_text)
    print("取得した価格:", price)
else:
    print("価格が取得できませんでした")
    exit()

# -------------------------------
# ③ CSVファイルに保存（ログ記録）
# -------------------------------
log_file = "price_log.csv"
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

if os.path.exists(log_file):
    df = pd.read_csv(log_file)
else:
    df = pd.DataFrame(columns=["datetime", "price"])

df.loc[len(df)] = [now, price]
df.to_csv(log_file, index=False)
print("CSVに保存しました。")

# -------------------------------
# ④ グラフ表示（価格の推移）
# -------------------------------
df["datetime"] = pd.to_datetime(df["datetime"])
df["price"] = df["price"].astype(int)

plt.figure(figsize=(10, 5))
plt.plot(df["datetime"], df["price"], marker='o', linestyle='-')
plt.title("価格推移")
plt.xlabel("日付")
plt.ylabel("価格（円）")
plt.grid(True)
plt.tight_layout()
plt.show()
