#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
test_voice_trans.py - voice_trans.pyのユニットテスト
"""

import unittest
import os
import tempfile
import shutil
import subprocess
from unittest.mock import patch, MagicMock

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.voice_trans import VoiceTrans


class TestVoiceTrans(unittest.TestCase):
    """VoiceTransクラスのテスト"""
    
    def setUp(self):
        """テスト用のディレクトリを設定"""
        self.test_dir = tempfile.mkdtemp()
        self.voice_trans = VoiceTrans(voice_dir=self.test_dir)
    
    def tearDown(self):
        """テスト用のディレクトリを削除"""
        shutil.rmtree(self.test_dir)
    
    def create_test_mp3(self, filename):
        """テスト用のMP3ファイルを作成"""
        mp3_path = os.path.join(self.test_dir, filename)
        with open(mp3_path, 'w') as f:
            f.write("dummy mp3 content")
        return mp3_path
    
    def test_find_mp3_files_empty(self):
        """MP3ファイルがない場合のテスト"""
        result = self.voice_trans.find_mp3_files()
        self.assertFalse(result)
        self.assertEqual(len(self.voice_trans.mp3_files), 0)
    
    def test_find_mp3_files(self):
        """MP3ファイルが存在する場合のテスト"""
        # テスト用のMP3ファイルを作成
        mp3_file = self.create_test_mp3("test.MP3")
        
        result = self.voice_trans.find_mp3_files()
        self.assertTrue(result)
        self.assertEqual(len(self.voice_trans.mp3_files), 1)
        self.assertEqual(self.voice_trans.mp3_files[0], mp3_file)
    
    def test_find_unprocessed_files_empty(self):
        """未処理ファイルがない場合のテスト"""
        # MP3ファイルとテキストファイルの両方を作成
        mp3_file = self.create_test_mp3("test.MP3")
        txt_file = mp3_file.replace(".MP3", ".txt")
        with open(txt_file, 'w') as f:
            f.write("dummy text content")
        
        self.voice_trans.mp3_files = [mp3_file]
        result = self.voice_trans.find_unprocessed_files()
        self.assertFalse(result)
        self.assertEqual(len(self.voice_trans.unprocessed_files), 0)
    
    def test_find_unprocessed_files(self):
        """未処理ファイルがある場合のテスト"""
        mp3_file = self.create_test_mp3("test.MP3")
        self.voice_trans.mp3_files = [mp3_file]
        
        result = self.voice_trans.find_unprocessed_files()
        self.assertTrue(result)
        self.assertEqual(len(self.voice_trans.unprocessed_files), 1)
        self.assertEqual(self.voice_trans.unprocessed_files[0], mp3_file)
    
    @patch('subprocess.run')
    def test_transcribe_file_success(self, mock_run):
        """テキスト起こしが成功する場合のテスト"""
        mp3_file = self.create_test_mp3("test.MP3")
        
        # 一時ディレクトリにWhisperの出力ファイルを作成
        whisper_output = os.path.join(self.voice_trans.tmp_dir, "test.txt")
        with open(whisper_output, 'w') as f:
            f.write("テスト文字起こし")
        
        # モックの設定
        mock_run.return_value = MagicMock(returncode=0)
        
        result = self.voice_trans.transcribe_file(mp3_file)
        self.assertTrue(result)
        
        # テキストファイルが作成されているか確認
        txt_file = mp3_file.replace(".MP3", ".txt")
        self.assertTrue(os.path.exists(txt_file))
    
    @patch('subprocess.run')
    def test_transcribe_file_error(self, mock_run):
        """テキスト起こしが失敗する場合のテスト"""
        mp3_file = self.create_test_mp3("test.MP3")
        
        # モックの設定
        mock_run.side_effect = subprocess.CalledProcessError(1, 'whisper', stderr=b'Error message')
        
        result = self.voice_trans.transcribe_file(mp3_file)
        self.assertFalse(result)
        
        # テキストファイルが作成されていないか確認
        txt_file = mp3_file.replace(".MP3", ".txt")
        self.assertFalse(os.path.exists(txt_file))
    
    def test_get_progress(self):
        """進捗状況のテスト"""
        # 初期状態
        processed, total, percent = self.voice_trans.get_progress()
        self.assertEqual(processed, 0)
        self.assertEqual(total, 0)
        self.assertEqual(percent, 0)
        
        # 進捗あり
        self.voice_trans.total_files = 10
        self.voice_trans.processed_files = 3
        processed, total, percent = self.voice_trans.get_progress()
        self.assertEqual(processed, 3)
        self.assertEqual(total, 10)
        self.assertEqual(percent, 30)


if __name__ == '__main__':
    unittest.main()