#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
voice_sync.py - ボイスレコーダーからMP3ファイルをMacに転送するスクリプト
"""

import os
import sys
import subprocess
import datetime
import glob
import shutil

class VoiceSync:
    """ボイスレコーダーからMP3ファイルを同期するクラス"""
    
    def __init__(self):
        # 設定
        self.voice_root_dir = "/Volumes/NO NAME/VOICE"  # ボイスレコーダーのパス
        self.voice_copy_dir = os.path.expanduser("~/voice_memo")  # 保存先ディレクトリ
        self.mp3_files = []  # 検出されたMP3ファイル
    
    def check_device(self):
        """ボイスレコーダーの接続とMP3ファイルを確認"""
        print("ボイスレコーダーの接続を確認中...")
        
        if not os.path.exists("/Volumes/NO NAME"):
            print("エラー: ボイスレコーダーが接続されていないか、マウントされていません")
            print("デバイスを接続して再度実行してください")
            return False
        
        if not os.path.exists(self.voice_root_dir):
            print("エラー: {} ディレクトリが見つかりません".format(self.voice_root_dir))
            print("ボイスレコーダーの構成が想定と異なります")
            return False
        
        print("ボイスレコーダーが正常に接続されています")
        
        # MP3ファイルの検索
        print("{}内のMP3ファイルを検索中...".format(self.voice_root_dir))
        self.find_mp3_files()
        
        if len(self.mp3_files) == 0:
            print("{}内にMP3ファイルが見つかりませんでした".format(self.voice_root_dir))
            return False
        
        print("{}個のMP3ファイルが見つかりました".format(len(self.mp3_files)))
        return True
    
    def find_mp3_files(self):
        """MP3ファイルをリストアップ"""
        # globを使って再帰的に検索
        pattern = os.path.join(self.voice_root_dir, "**", "*.MP3")
        self.mp3_files = glob.glob(pattern, recursive=True)
    
    def copy_files(self):
        """ボイスレコーダーのMP3ファイルをコピー"""
        # 出力先ディレクトリがなければ作成
        if not os.path.exists(self.voice_copy_dir):
            os.makedirs(self.voice_copy_dir)
        
        for i, mp3_file in enumerate(self.mp3_files):
            print("処理中 {}/{}: {}".format(i+1, len(self.mp3_files), mp3_file))
            
            # ファイルの更新日時を取得してタイムスタンプ形式に変換
            file_time = os.path.getmtime(mp3_file)
            timestamp = datetime.datetime.fromtimestamp(file_time).strftime("%Y%m%d_%H%M%S")
            new_file_name = os.path.join(self.voice_copy_dir, "{}.MP3".format(timestamp))
            
            # ファイルをコピー
            shutil.copy2(mp3_file, new_file_name)
        
        print("すべてのMP3ファイルのコピーが完了しました")
    
    def clean_files(self):
        """ボイスレコーダーのMP3ファイルを削除"""
        print("削除対象のMP3ファイルが{}個見つかりました".format(len(self.mp3_files)))
        
        for i, mp3_file in enumerate(self.mp3_files):
            print("削除中 {}/{}: {}".format(i+1, len(self.mp3_files), mp3_file))
            os.remove(mp3_file)
        
        print("すべてのMP3ファイルが削除されました")
    
    def unmount_drive(self):
        """ボイスレコーダーをアンマウント"""
        print("USBドライブをアンマウント中...")
        
        try:
            # diskutilコマンドを使用してアンマウント
            subprocess.run(["diskutil", "unmount", "/Volumes/NO NAME"], check=True)
            print("USBドライブが安全にアンマウントされました。取り外し可能です。")
            return True
        except subprocess.CalledProcessError:
            print("ドライブのアンマウント中にエラーが発生しました。使用中のファイルがないか確認してください。")
            return False
    
    def run(self):
        """メイン処理を実行"""
        print("ボイスレコーダーのデータ処理を開始します...")
        
        # デバイスチェック
        if not self.check_device():
            return False
        
        # コピー処理
        self.copy_files()
        
        # 削除処理
        self.clean_files()
        
        # アンマウント処理
        self.unmount_drive()
        
        print("すべての処理が完了しました")
        return True


def main():
    """スクリプトのメイン処理"""
    voice_sync = VoiceSync()
    success = voice_sync.run()
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
