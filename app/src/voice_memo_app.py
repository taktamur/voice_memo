#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Voice Memo App - 音声メモアプリケーション
簡単なステータスバーアプリケーション
"""

import rumps
import sys
import os
import argparse
import threading
import time
import subprocess
from voice_sync import VoiceSync
from voice_trans import VoiceTrans

class VoiceMemoApp(rumps.App):
    """Voice Memoアプリケーションのメインクラス"""
    
    def __init__(self):
        super(VoiceMemoApp, self).__init__(
            "Voice Memo",  # アプリ名
            # アイコンはとりあえずなし
            quit_button="終了"  # 終了ボタンのテキスト
        )
        
        # メニューの設定
        self.menu = [
            "ボイスメモをコピー",
            "テキスト起こし",
            None,  # セパレータ
            rumps.MenuItem("自動検出", callback=self.toggle_auto_detection),
            "設定"
        ]
        
        # 自動検出の有効/無効フラグ
        self.auto_detection_enabled = False
        self.menu["自動検出"].state = self.auto_detection_enabled
        
        # USBデバイス監視
        self.observer = None
    
    @rumps.clicked("ボイスメモをコピー")
    def copy_voice_memos(self, _):
        """ボイスメモをコピーする機能"""
        try:
            # 別スレッドで実行して、UIをブロックしないようにする
            threading.Thread(target=self._run_voice_sync).start()
        except Exception as e:
            rumps.alert(
                title="エラー",
                message=f"ボイスメモのコピー中にエラーが発生しました: {str(e)}",
                ok="OK"
            )
    
    def _run_voice_sync(self):
        """VoiceSyncを実行する内部メソッド"""
        try:
            self.title = "処理中..."
            voice_sync = VoiceSync()
            if voice_sync.check_device():
                # デバイスが正常にマウントされている場合
                result = voice_sync.run()
                if result:
                    rumps.notification(
                        title="Voice Memo",
                        subtitle="処理完了",
                        message="ボイスメモの同期が完了しました",
                        sound=True
                    )
                else:
                    rumps.notification(
                        title="Voice Memo",
                        subtitle="処理エラー",
                        message="ボイスメモの同期中にエラーが発生しました",
                        sound=True
                    )
            else:
                # デバイスが見つからない場合
                rumps.notification(
                    title="Voice Memo",
                    subtitle="デバイスエラー",
                    message="ボイスレコーダーが接続されていないか、認識できません",
                    sound=True
                )
        except Exception as e:
            rumps.notification(
                title="Voice Memo",
                subtitle="エラー",
                message=f"処理中にエラーが発生しました: {str(e)}",
                sound=True
            )
        finally:
            self.title = "Voice Memo"
    
    @rumps.clicked("テキスト起こし")
    def transcribe_voice_memos(self, _):
        """ボイスメモをテキスト起こしする機能"""
        try:
            # 別スレッドで実行して、UIをブロックしないようにする
            threading.Thread(target=self._run_voice_trans).start()
        except Exception as e:
            rumps.alert(
                title="エラー",
                message=f"テキスト起こし中にエラーが発生しました: {str(e)}",
                ok="OK"
            )
    
    def _run_voice_trans(self):
        """VoiceTransを実行する内部メソッド"""
        try:
            self.title = "処理中..."
            voice_trans = VoiceTrans()
            
            # MP3ファイルの検索
            if not voice_trans.find_mp3_files():
                rumps.notification(
                    title="Voice Memo",
                    subtitle="情報",
                    message="MP3ファイルが見つかりませんでした",
                    sound=True
                )
                self.title = "Voice Memo"
                return
            
            # 未処理ファイルの検索
            if not voice_trans.find_unprocessed_files():
                rumps.notification(
                    title="Voice Memo",
                    subtitle="情報",
                    message="テキスト起こしが必要なファイルはありません",
                    sound=True
                )
                self.title = "Voice Memo"
                return
            
            # 進捗表示用のスレッド
            def update_progress():
                while True:
                    processed, total, percentage = voice_trans.get_progress()
                    if total > 0:
                        self.title = f"処理中... {percentage}%"
                    
                    # 全て処理完了、または中断された場合
                    if processed >= total:
                        break
                    
                    time.sleep(1)
            
            progress_thread = threading.Thread(target=update_progress)
            progress_thread.daemon = True
            progress_thread.start()
            
            # テキスト起こし処理を実行
            result = voice_trans.transcribe_all()
            
            if result:
                rumps.notification(
                    title="Voice Memo",
                    subtitle="処理完了",
                    message="すべてのMP3ファイルのテキスト起こしが完了しました",
                    sound=True
                )
            else:
                rumps.notification(
                    title="Voice Memo",
                    subtitle="処理警告",
                    message="一部のファイルの処理中にエラーが発生しました",
                    sound=True
                )
        except Exception as e:
            rumps.notification(
                title="Voice Memo",
                subtitle="エラー",
                message=f"処理中にエラーが発生しました: {str(e)}",
                sound=True
            )
        finally:
            self.title = "Voice Memo"
    
    def toggle_auto_detection(self, sender):
        """USBデバイスの自動検出を有効/無効にする"""
        self.auto_detection_enabled = not self.auto_detection_enabled
        sender.state = self.auto_detection_enabled
        
        if self.auto_detection_enabled:
            # 自動検出を開始
            rumps.notification(
                title="Voice Memo",
                subtitle="自動検出",
                message="ボイスレコーダーの自動検出を開始しました",
                sound=False
            )
            self.start_usb_monitor()
        else:
            # 自動検出を停止
            rumps.notification(
                title="Voice Memo",
                subtitle="自動検出",
                message="ボイスレコーダーの自動検出を停止しました",
                sound=False
            )
            self.stop_usb_monitor()
    
    def start_usb_monitor(self):
        """USBデバイス監視を開始"""
        if self.observer is not None and self.observer.is_alive():
            return  # すでに実行中
        
        # 監視イベントハンドラを設定
        threading.Thread(target=self._monitor_usb_devices).start()
    
    def stop_usb_monitor(self):
        """USBデバイス監視を停止"""
        if self.observer is not None:
            self.observer.stop()
            self.observer.join()
            self.observer = None
    
    def _monitor_usb_devices(self):
        """USBデバイスを監視して、ボイスレコーダーが接続されたら自動処理を実行"""
        # watchdog パッケージが必要
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler
        
        class USBDeviceHandler(FileSystemEventHandler):
            def __init__(self, app):
                self.app = app
                self.device_detected = False  # デバイス検出フラグ
            
            def on_created(self, event):
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
                        
                        # 同期処理を実行
                        self.app._run_voice_sync()
                        
                        # 処理完了後にフラグをリセット
                        def reset_flag():
                            time.sleep(10)  # 10秒後にフラグをリセット
                            self.device_detected = False
                        
                        # 別スレッドでフラグリセット処理を実行
                        reset_thread = threading.Thread(target=reset_flag)
                        reset_thread.daemon = True
                        reset_thread.start()
        
        # オブザーバーの作成
        self.observer = Observer()
        handler = USBDeviceHandler(self)
        
        # /Volumes ディレクトリを監視対象に設定
        self.observer.schedule(handler, path="/Volumes", recursive=False)
        self.observer.start()
        
        # このスレッドを終了すると自動的にObserverは終了する
    
    @rumps.clicked("設定")
    def preferences(self, _):
        """設定画面を表示する機能"""
        window = rumps.Window(
            title="Voice Memo 設定",
            message="設定画面",
            dimensions=(300, 100)
        )
        window.run()


def auto_quit(seconds, app):
    """指定した秒数後にアプリケーションを終了する"""
    print(f"デバッグモード: {seconds}秒後に自動終了します")
    time.sleep(seconds)
    print("自動終了します")
    rumps.quit_application()

if __name__ == "__main__":
    # コマンドライン引数の処理
    parser = argparse.ArgumentParser(description='Voice Memo アプリケーション')
    parser.add_argument('--debug', action='store_true', help='デバッグモードで実行（10秒後に自動終了）')
    parser.add_argument('--quit-after', type=int, default=10, help='指定秒数後に自動終了（デバッグモード使用時のみ有効、デフォルト: 10秒）')
    parser.add_argument('--auto-detect', action='store_true', help='起動時にUSBデバイスの自動検出を有効にする')
    args = parser.parse_args()
    
    # デバッグモードを有効化
    rumps.debug_mode(True)
    
    app = VoiceMemoApp()
    
    # 自動検出オプションが指定されている場合
    if args.auto_detect:
        app.auto_detection_enabled = True
        app.menu["自動検出"].state = True
        app.start_usb_monitor()
        print("USBデバイスの自動検出が有効化されました")
    
    # デバッグモードの場合、自動終了タイマーを設定
    if args.debug:
        quit_time = args.quit_after
        threading.Thread(target=auto_quit, args=(quit_time, app), daemon=True).start()
        print(f"デバッグモード有効: {quit_time}秒後に自動終了します")
    
    # アプリケーション実行
    app.run()