#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
voice_trans.py - MP3ファイルからWhisperを使って文字起こしを行うスクリプト
"""

import os
import sys
import subprocess
import glob
import tempfile
import shutil

class VoiceTrans:
    """MP3ファイルから文字起こしを行うクラス"""
    
    def __init__(self, voice_dir=None):
        # 設定
        self.voice_dir = voice_dir or os.path.expanduser("~/voice_memo")  # 音声ファイルのディレクトリ
        self.tmp_dir = tempfile.gettempdir()  # 一時ディレクトリ
        self.mp3_files = []  # 検出されたMP3ファイル
        self.unprocessed_files = []  # 未処理のMP3ファイル
        self.total_files = 0  # 合計ファイル数
        self.processed_files = 0  # 処理済みファイル数
    
    def find_mp3_files(self):
        """音声ディレクトリ内のMP3ファイルを検索"""
        print(f"{self.voice_dir}内のMP3ファイルを検索中...")
        
        # globを使って再帰的に検索
        pattern = os.path.join(self.voice_dir, "**", "*.MP3")
        self.mp3_files = glob.glob(pattern, recursive=True)
        
        if len(self.mp3_files) == 0:
            print(f"{self.voice_dir}内にMP3ファイルが見つかりませんでした")
            return False
        
        print(f"{len(self.mp3_files)}個のMP3ファイルが見つかりました")
        return True
    
    def find_unprocessed_files(self):
        """テキスト起こししていないファイルを検索"""
        self.unprocessed_files = []
        
        for mp3_file in self.mp3_files:
            txt_file = mp3_file.replace(".MP3", ".txt")
            if not os.path.exists(txt_file):
                self.unprocessed_files.append(mp3_file)
        
        self.total_files = len(self.unprocessed_files)
        self.processed_files = 0
        
        if len(self.unprocessed_files) == 0:
            print("テキスト起こしが必要なファイルはありません")
            return False
        
        print(f"{len(self.unprocessed_files)}個のテキスト起こしが必要なMP3ファイルが見つかりました")
        return True
    
    def transcribe_file(self, mp3_file):
        """Whisperを使ってMP3ファイルをテキスト起こし"""
        try:
            # Whisperのコマンドを実行
            result = subprocess.run(
                [
                    "whisper",
                    "--output_format=txt",
                    f"--output_dir={self.tmp_dir}",
                    "--language=ja",
                    mp3_file
                ],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env={**os.environ, "PYTHONWARNINGS": "ignore"}
            )
            
            # Whisperの出力ファイル名
            base_name = os.path.basename(mp3_file).replace(".MP3", "")
            whisper_file = os.path.join(self.tmp_dir, f"{base_name}.txt")
            
            # Whisperの出力ファイルを元のディレクトリに移動
            target_file = mp3_file.replace(".MP3", ".txt")
            shutil.copy2(whisper_file, target_file)
            
            return True
        except subprocess.CalledProcessError as e:
            print(f"エラー: Whisperの実行中にエラーが発生しました: {e}")
            print(f"stderr: {e.stderr.decode('utf-8')}")
            return False
        except Exception as e:
            print(f"エラー: ファイル処理中に例外が発生しました: {e}")
            return False
    
    def transcribe_all(self):
        """すべてのファイルをテキスト起こし"""
        success_count = 0
        
        for i, mp3_file in enumerate(self.unprocessed_files):
            print(f"処理中 {i+1}/{len(self.unprocessed_files)}: {mp3_file}")
            
            if self.transcribe_file(mp3_file):
                success_count += 1
                self.processed_files += 1
            
            # 進捗状況を更新
            print(f"進捗: {self.processed_files}/{self.total_files}")
        
        print(f"テキスト起こし完了: {success_count}/{len(self.unprocessed_files)}ファイルが処理されました")
        return success_count == len(self.unprocessed_files)
    
    def get_progress(self):
        """進捗状況を取得"""
        if self.total_files == 0:
            return 0, 0, 0  # 処理済み、全体、パーセント
        
        percentage = int((self.processed_files / self.total_files) * 100)
        return self.processed_files, self.total_files, percentage
    
    def run(self):
        """メイン処理を実行"""
        print("MP3ファイルのテキスト起こし処理を開始します...")
        
        # MP3ファイルの検索
        if not self.find_mp3_files():
            return False
        
        # 未処理ファイルの検索
        if not self.find_unprocessed_files():
            return True  # 処理するファイルがない場合も成功とみなす
        
        # テキスト起こし処理
        result = self.transcribe_all()
        
        print("すべての処理が完了しました")
        return result


def main():
    """スクリプトのメイン処理"""
    voice_trans = VoiceTrans()
    success = voice_trans.run()
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
