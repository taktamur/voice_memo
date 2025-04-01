#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Voice Memo App - 音声メモアプリケーション
簡単なステータスバーアプリケーション
"""

import rumps

class VoiceMemoApp(rumps.App):
    """Voice Memoアプリケーションのメインクラス"""
    
    def __init__(self):
        super(VoiceMemoApp, self).__init__(
            "Voice Memo",  # アプリ名
            icon="🎤",     # アイコン（絵文字を使用）
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


if __name__ == "__main__":
    # デバッグモードを有効化
    rumps.debug_mode(True)
    
    # アプリケーション実行
    VoiceMemoApp().run()
