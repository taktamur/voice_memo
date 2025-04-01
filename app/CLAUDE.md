# CLAUDE.md - ボイスメモプロジェクトガイドライン

## コマンド
- `./voice_sync.sh` - レコーダーから音声ファイルをMacに同期
- `./voice_trans.sh` - MP3ファイルをテキストに変換
- `rake voicememo:sync` - Rake経由で音声同期を実行
- `rake voicememo:trans` - Rake経由で文字起こしを実行
- `python voice_memo_app.py` - 開発モードでアプリ実行
- `python setup.py py2app` - スタンドアロンアプリのビルド
- `python test.py` - rumpsの基本テスト実行

## コードスタイル規約
- Python: PEP 8スタイルガイドに準拠
- シェルスクリプト: ファイル先頭に `#!/bin/bash` を記述
- 変数: 設定値やグローバル変数は大文字で記述
- 関数: snake_caseの命名規則を使用
- クラス: CamelCaseの命名規則を使用
- エラー処理: エラー時はコード1で終了し、情報メッセージを表示
- コメント: ユーザー向けメッセージは日本語、コード説明は英語
- 文字列: 変数や空白を含むパスは常にダブルクォートで囲む
- インデント: すべてのコードで4スペース
- 入力検証: 操作前にリソースの存在を確認
- パス処理: 特殊文字を常に適切に処理
- 関数設計: 各関数は単一の責任を持つこと

## プロジェクト構造
- ソースファイル: `/Volumes/NO NAME/VOICE`
- 保存先: `${HOME}/.voice_memo/`
- ファイル命名規則: YYYYMMDD_HHMMSS.MP3
- macOSステータスバー連携にrumpsを使用したPythonアプリ
- 日本語対応のWhisperによるMP3文字起こし