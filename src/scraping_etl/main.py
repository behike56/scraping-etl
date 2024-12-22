"""
https://artesnaut.com/wiki/?%E3%82%A2%E3%82%A4%E3%83%86%E3%83%A0%E5%9B%B3%E9%91%91
"""
import csv
import os
import requests
from bs4 import BeautifulSoup

# 1. ターゲットURLの指定
url = "https://artesnaut.com/wiki/?%E3%82%A2%E3%82%A4%E3%83%86%E3%83%A0%E5%9B%B3%E9%91%91"  # 例: スクレイピングしたいサイトのURL

# 2. ページ内容の取得
response = requests.get(url)  
html_content = response.text

# 2. 出力用ディレクトリがなければ作成
output_dir = "output"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def main():
    soup = BeautifulSoup(html_content, "html.parser")

    # 1. <div id="body"> のみを対象にする
    body_div = soup.find("div", id="body")
    if not body_div:
        print("Error: <div id='body'>が見つかりませんでした。")
        exit()

    # 2. <div id="body"> 内の <h3> タグをすべて取得
    h3_elements = body_div.find_all("h3")

    for h3 in h3_elements:
        title = h3.get_text(strip=True)
        print(f"タイトル: {title}")

        # ファイル名用にtitleから使えない文字を置換するなどの処理を行う（ここでは簡易的に置換例）
        safe_title = title.replace("/", "_").replace("\\", "_").replace(" ", "_")

        # 3. h3 の次にある <div class="ie5"> を取得
        div_ie5 = h3.find_next_sibling("div", class_="ie5")
        if not div_ie5:
            print(f"  {title} に対応する <div class='ie5'> が見つかりませんでした。")
            continue

        # 4. テーブルを取得
        table = div_ie5.find("table", class_="style_table")
        if not table:
            print(f"  {title} に対応する <table class='style_table'> が見つかりませんでした。")
            continue
        # 5. ヘッダー行（<thead>）を取得し、CSVの最初の行として使う
        thead = table.find("thead")
        if not thead:
            print(f"  {title} テーブルに <thead> がありません。")
            continue

        header_row = thead.find("tr")
        if not header_row:
            print(f"  {title} テーブルに thead の <tr> がありません。")
            continue

        # <th> 要素を取得してヘッダー用リストに
        header_cells = [th.get_text(strip=True) for th in header_row.find_all("th")]

        # 6. テーブルの tbody -> tr -> td を取得
        tbody = table.find("tbody")
        if not tbody:
            print(f"  {title} テーブルに <tbody> がありません。")
            continue

        rows = tbody.find_all("tr")
        if not rows:
            print(f"  {title} テーブルに <tr> がありません。")
            continue

        # 7. CSVファイルに書き込み
        filename = f"{safe_title}.csv"
        csv_path = os.path.join(output_dir, f"{safe_title}.csv")
        with open(csv_path, mode="w", newline="", encoding="utf-8") as csv_file:
            
            writer = csv.writer(csv_file)
            
            # 先頭行としてヘッダーを出力
            writer.writerow(header_cells)
            
            # tbody 内の各 <tr> の <td> を1行ずつ出力
            for row_idx, row in enumerate(rows, start=1):
                cells = [td.get_text(strip=True) for td in row.find_all("td")]
                writer.writerow(cells)

        print(f"  -> CSVファイルとして '{filename}' に出力しました。")
        print("-----")


if __name__ == "__main__":
    main()