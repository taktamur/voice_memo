#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
voice_config.py - 音声メモアプリの設定を管理するモジュール
設定ファイルの読み込み・保存や設定値の一元管理を行う
"""

import os
import sys
import yaml
import logging
import tempfile
from pathlib import Path

# ロガーの設定
logger = logging.getLogger("voice_config")

class VoiceConfig:
    """音声メモアプリの設定を管理するクラス"""
    
    # デフォルト設定
    DEFAULT_CONFIG = {
        # 基本設定
        "app": {
            "name": "Voice Memo",
            "debug": False,
        },
        # ボイスレコーダー設定
        "recorder": {
            "device_name": "NO NAME",
            "voice_dir": "VOICE",
            "mount_path": "/Volumes"
        },
        # 保存先設定
        "storage": {
            "voice_copy_dir": "~/voice_memo",
            "tmp_dir": None  # Noneの場合はtempfileのデフォルトを使用
        },
        # Whisper設定
        "whisper": {
            "language": "ja",
            "output_format": "txt"
        },
        # 監視設定
        "monitor": {
            "auto_detection": False,
            "reset_timeout": 10
        }
    }
    
    def __init__(self):
        """コンストラクタ"""
        logger.debug("VoiceConfigの初期化を開始します...")
        # デフォルト設定をコピー
        self.config = self.DEFAULT_CONFIG.copy()
        # 設定ファイルのパスを取得
        self.config_file = self._get_config_file_path()
        # 設定ファイルを読み込み
        self.load_config()
        logger.debug("VoiceConfigの初期化が完了しました")
    
    def _get_config_file_path(self):
        """設定ファイルのパスを取得"""
        # ユーザーホームディレクトリの.voice_memoフォルダ内のconfig.yamlを使用
        config_dir = Path.home() / ".voice_memo"
        config_dir.mkdir(exist_ok=True)
        return config_dir / "config.yaml"
    
    def load_config(self):
        """設定ファイルから設定を読み込む"""
        try:
            if self.config_file.