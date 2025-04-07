#!/usr/bin/env python
# streamlitを使って、~/voice_memo/*.txtをリスト表示する

import streamlit as st
import os
import glob
import re
from datetime import datetime
from collections import defaultdict

# ページタイトル設定
st.set_page_config(page_title="ボイスメモ一覧", layout="wide")
st.title("ボイスメモ一覧")

# ファイルパスを取得
home_dir = os.path.expanduser("~")
voice_memo_dir = os.path.join(home_dir, "voice_memo")
txt_files = glob.glob(os.path.join(voice_memo_dir, "*.txt"))

# 日付ごとにファイルをグループ化
date_pattern = re.compile(r"(\d{8})_\d{6}\.txt$")
files_by_date = defaultdict(list)

for file_path in txt_files:
    file_name = os.path.basename(file_path)
    match = date_pattern.search(file_name)
    
    if match:
        date_str = match.group(1)
        # YYYYMMDDのフォーマットを日付オブジェクトに変換
        date_obj = datetime.strptime(date_str, "%Y%m%d")
        formatted_date = date_obj.strftime("%Y年%m月%d日")
        
        # ファイル名からタイムスタンプを抽出してDateTime形式に変換
        timestamp_match = re.search(r"(\d{8})_(\d{6})\.txt$", file_name)
        if timestamp_match:
            date_part = timestamp_match.group(1)
            time_part = timestamp_match.group(2)
            timestamp = f"{date_part[:4]}-{date_part[4:6]}-{date_part[6:]} {time_part[:2]}:{time_part[2:4]}:{time_part[4:]}"
            datetime_obj = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            
            # ファイルの内容を読み込む
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 辞書に追加 (日付、時間、内容をタプルで保存)
            files_by_date[formatted_date].append((datetime_obj, content, file_name, date_obj))

# 日付でソート
sorted_dates = sorted(files_by_date.keys(), key=lambda x: datetime.strptime(x, "%Y年%m月%d日"), reverse=True)

# 各日付ごとにファイルを表示
for date in sorted_dates:
    # 対応するファイルのリストを取得
    files = files_by_date[date]
    
    # 一番最初の日付オブジェクトを取得してScrapboxリンクを生成
    if files:
        date_obj = files[0][3]  # タプルの4番目の要素が日付オブジェクト
        scrapbox_date = date_obj.strftime("%Y%%2F%m%%2F%d")
        scrapbox_link = f"https://scrapbox.io/taktamur-diary/{scrapbox_date}"
        
        # 日付の見出しとScrapboxへのリンク
        st.header(f"📆 {date}")
        st.markdown(f"[Scrapboxページを開く]({scrapbox_link})", unsafe_allow_html=True)
        
        # その日のファイルを時間順にソート
        sorted_files = sorted(files, key=lambda x: x[0])
        
        # 日付ごとのすべてのテキストを結合（各行の先頭に"> "を追加）
        all_text_for_date = ""
        
        # 賑やかしの絵文字を追加（最初のセクションの先頭にのみ）
        all_text_for_date += "💬 ボイスメモより\n\n"
        
        for datetime_obj, content, file_name, _ in sorted_files:
            time_str = datetime_obj.strftime("%H:%M:%S")
            # 見出しの追加
            all_text_for_date += f"> ===== {time_str} =====\n"
            
            # 各行の先頭に"> "を追加
            content_lines = content.splitlines()
            quoted_content = "\n".join([f"> {line}" for line in content_lines])
            
            all_text_for_date += quoted_content + "\n\n"
        
        # 日付全体のテキストをコピー可能なコードブロックで表示
        st.code(all_text_for_date, language=None)
        
        # 区切り線を追加
        st.markdown("---")

# サイドバーにフィルター機能
with st.sidebar:
    st.header("フィルター")
    st.text("今後実装予定の機能")
    st.markdown("---")
    st.caption("Voice Memo Streamlit Viewer")
