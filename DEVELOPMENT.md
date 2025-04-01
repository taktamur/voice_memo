# Voice Memo 開発メモ

## 環境構築

- Python 3.6以上が必要
- Mac環境で開発・動作確認

## ディレクトリ構造

- `/app` - アプリケーションのソースコード
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

### 将来的な実装

- [ ] 完全なGUIアプリケーション化（rumpsを使用）
- [ ] 自動起動機能の実装
- [ ] 設定ファイルのサポート
- [ ] 既存の機能（voice_sync, voice_trans）とrumpsアプリの統合
