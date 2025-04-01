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
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from voice_sync import VoiceSync

# ロガーの設定
logger = logging.getLogger("voice_monitor")
logger.setLevel(logging.DEBUG)

# コンソール出力用ハンドラ
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

class USBDeviceHandler(FileSystemEventHandler):
    """USBデバイスの検出を処理するイベントハンドラ"""
    
    def __init__(self, callback):
        """
        コンストラクタ
        
        Args:
            callback: デバイス検出時に呼び出すコールバック関数
        """
        logger.debug("USBDeviceHandlerを初期化しています...")
        self.callback = callback
        self.device_detected = False  # デバイス検出フラグ
        logger.debug("USBDeviceHandlerの初期化が完了しました")
    
    def on_created(self, event):
        """
        ファイル/ディレクトリ作成イベントの処理
        
        Args:
            event: ファイルシステムイベント
        """
        # すべての作成イベントをログに記録
        logger.debug(f"作成イベント検出: {event.src_path} (ディレクトリ: {event.is_directory})")
        
        if event.is_directory:
            logger.info(f"ディレクトリがマウントされました: {event.src_path}")
            
        if event.is_directory and os.path.basename(event.src_path) == "NO NAME" and not self.device_detected:
            # ボイスレコーダーのマウントを検出
            logger.info(f"ボイスレコーダーと思われるデバイスを検出: {event.src_path}")
            self.device_detected = True
            voice_sync = VoiceSync()
            
            # デバイスチェック
            logger.debug("VoiceSync.check_device()を実行中...")
            device_check_result = voice_sync.check_device()
            logger.debug(f"デバイスチェック結果: {device_check_result}")
            
            if device_check_result:
                # デバイスが見つかったら通知
                logger.info("ボイスレコーダーを正常に検出しました。処理を開始します。")
                rumps.notification(
                    title="Voice Memo",
                    subtitle="デバイス検出",
                    message="ボイスレコーダーが接続されました。自動処理を開始します。",
                    sound=True
                )
                
                # コールバック関数を呼び出し
                logger.debug("コールバック関数を呼び出します...")
                self.callback()
                logger.debug("コールバック関数の呼び出しが完了しました")
                
                # 処理完了後にフラグをリセット
                def reset_flag():
                    time.sleep(10)  # 10秒後にフラグをリセット
                    self.device_detected = False
                    logger.debug("デバイス検出フラグをリセットしました")
                
                # 別スレッドでフラグリセット処理を実行
                reset_thread = threading.Thread(target=reset_flag)
                reset_thread.daemon = True
                reset_thread.start()
                logger.debug("フラグリセット用スレッドを開始しました")
            else:
                logger.warning(f"デバイスが検出されましたが、ボイスレコーダーではありませんでした: {event.src_path}")
                self.device_detected = False

class USBMonitor:
    """USBデバイスを監視するクラス"""
    
    def __init__(self, callback):
        """
        コンストラクタ
        
        Args:
            callback: デバイス検出時に呼び出すコールバック関数
        """
        logger.debug("USBMonitorを初期化しています...")
        self.callback = callback
        self.observer = None
        logger.debug("USBMonitorの初期化が完了しました")
    
    def start(self):
        """監視を開始"""
        logger.info("USBデバイス監視の開始を試みています...")
        
        if self.observer is not None and self.observer.is_alive():
            logger.info("USBデバイス監視はすでに実行中です")
            return  # すでに実行中
        
        # オブザーバーの作成
        logger.debug("新しいObserverを作成しています...")
        self.observer = Observer()
        handler = USBDeviceHandler(self.callback)
        
        # /Volumes ディレクトリを監視対象に設定
        logger.debug("/Volumesディレクトリの監視を設定しています...")
        self.observer.schedule(handler, path="/Volumes", recursive=False)
        self.observer.start()
        logger.info("USBデバイス監視を開始しました (/Volumes ディレクトリを監視中)")
    
    def stop(self):
        """監視を停止"""
        logger.info("USBデバイス監視の停止を試みています...")
        
        if self.observer is not None:
            logger.debug("Observerを停止しています...")
            self.observer.stop()
            self.observer.join()
            self.observer = None
            logger.info("USBデバイス監視を停止しました")
        else:
            logger.info("USBデバイス監視はすでに停止しています")
    
    def is_running(self):
        """実行中かどうかを確認"""
        is_running = self.observer is not None and self.observer.is_alive()
        logger.debug(f"USBデバイス監視の状態: {'実行中' if is_running else '停止中'}")
        return is_running
