# Voice Memo アプリ

## 概要
Voice MemoはmacOSのステータスバーに常駐し、ボイスレコーダーからのファイル同期とテキスト起こしを行うシンプルなアプリケーションです。

## 機能
- ステータスバーからのシンプルな操作
- ボイスメモのコピー機能（未実装）
- テキスト起こし機能（未実装）

## 実行方法

### 開発モードで実行
```bash
cd /path/to/voice_memo/app
python src/voice_memo_app.py
```

### スタンドアロンアプリをビルド
```bash
cd /path/to/voice_memo/app
python setup.py py2app
```

ビルドが完了すると、`dist` ディレクトリに `Voice Memo.app` が作成されます。
このアプリケーションを Applications フォルダにドラッグ＆ドロップしてインストールできます。

## 注意事項
現在のバージョンは機能の実装フレームワークのみを提供しています。実際の機能は今後実装される予定です。
