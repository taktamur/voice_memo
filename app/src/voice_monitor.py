#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
voice_monitor.py - ボイスレコーダーUSBデバイスの監視モジュール
watchdogを使用してUSBデバイスの接続を監視し、接続時に処理を行う
"""

import os
import time
import threading
import rumps
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from voice_sync import VoiceSync

class USBDeviceHandler(FileSystemEventHandler):
    """USBデバイスの検出を処理するイベントハンドラ"""
    
    def __init__(self, callback):
        """
        コンストラクタ
        
        Args:
            callback: デバイス検出時に呼び出すコールバック関数
        """
        self.callback = callback
        self.device_detected = False  # デバイス検出フラグ
    
    def on_created(self, event):
        """
        ファイル/ディレクトリ作成イベントの処理
        
        Args:
            event: ファイルシステムイベント
        """
        if event.is_directory and os.path.basename(event.src_path) == "NO NAME" and not self.device_detected:
            # ボイスレコーダーのマウントを検出
            self.device_detected = True
            voice_sync = VoiceSync()
            if voice_sync.check_device():
                # デバイスが見つかったら通知
                rumps.notification(
                    title="Voice Memo",
                    subtitle="デバイス検出",
                    message="ボイスレコーダーが接続されました。自動処理を開始します。",
                    sound=True
                )
                
                # コールバック関数を呼び出し
                self.callback()
                
                # 処理完了後にフラグをリセット
                def reset_flag():
                    time.sleep(10)  # 10秒後にフラグをリセット
                    self.device_detected = False
                
                # 別スレッドでフラグリセット処理を実行
                reset_thread = threading.Thread(target=reset_flag)
                reset_thread.daemon = True
                reset_thread.start()

class USBMonitor:
    """USBデバイスを監視するクラス"""
    
    def __init__(self, callback):
        """
        コンストラクタ
        
        Args:
            callback: デバイス検出時に呼び出すコールバック関数
        """
        self.callback = callback
        self.observer = None
    
    def start(self):
        """監視を開始"""
        if self.observer is not None and self.observer.is_alive():
            return  # すでに実行中
        
        # オブザーバーの作成
        self.observer = Observer()
        handler = USBDeviceHandler(self.callback)
        
        # /Volumes ディレクトリを監視対象に設定
        self.observer.schedule(handler, path="/Volumes", recursive=False)
        self.observer.start()
    
    def stop(self):
        """監視を停止"""
        if self.observer is not None:
            self.observer.stop()
            self.observer.join()
            self.observer = None
    
    def is_running(self):
        """実行中かどうかを確認"""
        return self.observer is not None and self.observer.is_alive()
