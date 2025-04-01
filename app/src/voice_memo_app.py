#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Voice Memo App - 音声メモアプリケーション
簡単なステータスバーアプリケーション
"""

import rumps
import sys
import argparse
import threading
import time

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
            "設定"
        ]
    
    @rumps.clicked("ボイスメモをコピー")
    def copy_voice_memos(self, _):
        """ボイスメモをコピーする機能"""
        rumps.alert(
            title="Voice Memo",
            message="この機能は未実装です",
            ok="OK"
        )
    
    @rumps.clicked("テキスト起こし")
    def transcribe_voice_memos(self, _):
        """ボイスメモをテキスト起こしする機能"""
        rumps.alert(
            title="Voice Memo",
            message="この機能は未実装です",
            ok="OK"
        )
    
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
    args = parser.parse_args()
    
    # デバッグモードを有効化
    rumps.debug_mode(True)
    
    app = VoiceMemoApp()
    
    # デバッグモードの場合、自動終了タイマーを設定
    if args.debug:
        quit_time = args.quit_after
        threading.Thread(target=auto_quit, args=(quit_time, app), daemon=True).start()
        print(f"デバッグモード有効: {quit_time}秒後に自動終了します")
    
    # アプリケーション実行
    app.run()
