#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
test_voice_sync.py - voice_sync.pyのテスト用スクリプト
"""

import unittest
import os
import sys
import tempfile
import shutil
import subprocess
from unittest.mock import patch, MagicMock
from voice_sync import VoiceSync

class TestVoiceSync(unittest.TestCase):
    """VoiceSyncクラスのテスト"""
    
    def setUp(self):
        """テスト環境のセットアップ"""
        self.voice_sync = VoiceSync()
        # テスト用の一時ディレクトリ
        self.temp_dir = tempfile.mkdtemp()
        self.voice_sync.voice_copy_dir = self.temp_dir
    
    def tearDown(self):
        """テスト環境のクリーンアップ"""
        # 一時ディレクトリの削除
        shutil.rmtree(self.temp_dir)
    
    @patch('os.path.exists')
    def test_check_device_no_device(self, mock_exists):
        """デバイスが接続されていない場合のテスト"""
        # "/Volumes/NO NAME"が存在しない
        mock_exists.side_effect = lambda path: False if path == "/Volumes/NO NAME" else True
        
        result = self.voice_sync.check_device()
        self.assertFalse(result)
    
    @patch('os.path.exists')
    def test_check_device_no_voice_dir(self, mock_exists):
        """VOICEディレクトリがない場合のテスト"""
        # "/Volumes/NO NAME"は存在するが、"/Volumes/NO NAME/VOICE"が存在しない
        mock_exists.side_effect = lambda path: False if path == "/Volumes/NO NAME/VOICE" else True
        
        result = self.voice_sync.check_device()
        self.assertFalse(result)
    
    @patch('os.path.exists')
    @patch('glob.glob')
    def test_check_device_no_mp3(self, mock_glob, mock_exists):
        """MP3ファイルがない場合のテスト"""
        # パスは存在するが、MP3ファイルが見つからない
        mock_exists.return_value = True
        mock_glob.return_value = []
        
        result = self.voice_sync.check_device()
        self.assertFalse(result)
    
    @patch('os.path.exists')
    @patch('glob.glob')
    def test_check_device_with_mp3(self, mock_glob, mock_exists):
        """MP3ファイルがある場合のテスト"""
        # パスも存在し、MP3ファイルも見つかる
        mock_exists.return_value = True
        mock_glob.return_value = ["/Volumes/NO NAME/VOICE/A/REC001.MP3"]
        
        result = self.voice_sync.check_device()
        self.assertTrue(result)
        self.assertEqual(len(self.voice_sync.mp3_files), 1)
    
    @patch('os.path.getmtime')
    @patch('shutil.copy2')
    @patch('os.makedirs')
    def test_copy_files(self, mock_makedirs, mock_copy2, mock_getmtime):
        """ファイルのコピーテスト"""
        # テスト用のMP3ファイルリストをセット
        self.voice_sync.mp3_files = ["/Volumes/NO NAME/VOICE/A/REC001.MP3"]
        
        # getmtimeのモック - タイムスタンプをモック
        mock_getmtime.return_value = 1617235200  # 2021-04-01 00:00:00 UTC
        
        # datetime.fromtimestampの振る舞いをモック
        with patch('datetime.datetime') as mock_datetime:
            # モックされた日時オブジェクトを設定
            mock_dt = MagicMock()
            mock_dt.strftime.return_value = "20210401_000000"
            mock_datetime.fromtimestamp.return_value = mock_dt
            
            # コピー処理を実行
            self.voice_sync.copy_files()
        
        # コピー先のパスを検証
        expected_dest = os.path.join(self.temp_dir, "20210401_000000.MP3")
        mock_copy2.assert_called_once_with("/Volumes/NO NAME/VOICE/A/REC001.MP3", expected_dest)
    
    @patch('os.remove')
    def test_clean_files(self, mock_remove):
        """ファイルの削除テスト"""
        # テスト用のMP3ファイルリストをセット
        self.voice_sync.mp3_files = ["/Volumes/NO NAME/VOICE/A/REC001.MP3"]
        
        # 削除処理を実行
        self.voice_sync.clean_files()
        
        # 削除パスを検証
        mock_remove.assert_called_once_with("/Volumes/NO NAME/VOICE/A/REC001.MP3")
    
    @patch('subprocess.run')
    def test_unmount_drive_success(self, mock_run):
        """アンマウント成功のテスト"""
        # サブプロセスの実行が成功
        mock_run.return_value = MagicMock(returncode=0)
        
        result = self.voice_sync.unmount_drive()
        self.assertTrue(result)
    
    @patch('subprocess.run')
    def test_unmount_drive_failure(self, mock_run):
        """アンマウント失敗のテスト"""
        # サブプロセスの実行が失敗
        mock_run.side_effect = subprocess.CalledProcessError(1, "diskutil")
        
        result = self.voice_sync.unmount_drive()
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
