# Voice Memo 開発メモ

## 環境構築

- Python 3.6以上が必要
- Mac環境で開発・動作確認

## 必要なパッケージ

- rumps - Macのステータスバーアプリケーションフレームワーク
- watchdog - ファイルシステム監視ライブラリ（USBデバイスの検出に必須）

```
pip install rumps watchdog
```

## ディレクトリ構造

- `/app` - アプリケーションのソースコード
  - `/app/src` - Pythonソースファイル
  - `/app/tests` - テストファイル
- `/docs` - ドキュメント

## TODOリスト

### Issue #2: app/のREADME.mdにある (A)rumps を使わずに、ボイスレコーダーからファイルをコピーする処理を実装する

- [x] 既存のbashスクリプト（voice_sync.sh）をPythonで再実装
- [x] ユニットテストの作成
- [x] インストールスクリプトの更新

### Issue #3: app/のREADME.mdにある (B)rumps を使わずに、MP3 から文字起こしを行う機能実装する

- [x] 既存のbashスクリプト（voice_trans.sh）をPythonで再実装
- [x] ユニットテストの作成
- [x] 進捗（処理済ファイル数/全ファイル数）を取得できる機能の実装

### Issue #6: rakefileを用意する

- [x] アプリディレクトリにRakefileを作成
- [x] unittestを動かすタスクを実装
- [x] アプリを起動するタスクを実装

### Issue #5: pythonソースを app/src/以下に移動する

- [x] Pythonソースファイル（voice_sync.py, voice_trans.py）を app/src/ に移動
- [x] テストファイルを app/tests/ に移動
- [x] 各テストファイルのインポートパスを修正
- [x] Rakefileのパスを修正

### Issue #9: 空の rumps アプリを作る

- [x] rumpsを使用した基本的なステータスバーアプリを実装
- [x] アプリケーションをビルドするためのsetup.pyを作成
- [x] Rakefileにアプリ実行とビルドタスクを追加

### Issue #14: rumps アプリにボイスレコーダーからmp3ファイルを読み取る機能を呼び出せるようにする

- [x] ボイスメモをコピー機能の実装 (voice_sync.pyの統合)
- [x] テキスト起こし機能の実装 (voice_trans.pyの統合)
- [x] USBデバイス自動検出機能の実装
  - [x] watchdogライブラリを使用したファイルシステム監視
  - [x] voice_monitor.pyモジュールとして分離して実装
- [x] ボイスレコーダー接続時の自動処理機能の実装
- [x] メニューから手動でUSBデバイス自動検出の有効/無効を切り替え可能に
- [x] コマンドライン引数で起動時のUSBデバイス自動検出を有効化可能に

### 将来的な実装

- [x] 完全なGUIアプリケーション化（rumpsを使用）
- [x] 既存の機能（voice_sync, voice_trans）とrumpsアプリの統合
- [ ] 自動起動機能の実装
- [ ] 設定ファイルのサポート
- [ ] 進捗情報やステータスの詳細表示
