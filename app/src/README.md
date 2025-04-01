# Voice Memo アプリ

## 概要
Voice MemoはmacOSのステータスバーに常駐し、ボイスレコーダーからのファイル同期とテキスト起こしを行うシンプルなアプリケーションです。

## 機能
- ステータスバーからのシンプルな操作
- ボイスメモのコピー機能（未実装）
- テキスト起こし機能（未実装）

## 実行方法

### 通常実行
```bash
cd /path/to/voice_memo/app
python src/voice_memo_app.py
```

### Rakeを使った実行
```bash
cd /path/to/voice_memo/app
rake run:app
```

### デバッグモード（10秒で自動終了）
```bash
cd /path/to/voice_memo/app
python src/voice_memo_app.py --debug
```
または
```bash
cd /path/to/voice_memo/app
rake run:app_debug
```

### デバッグモード（指定秒数で自動終了）
```bash
cd /path/to/voice_memo/app
python src/voice_memo_app.py --debug --quit-after=5  # 5秒後に終了
```
または
```bash
cd /path/to/voice_memo/app
rake run:app_debug_timed[5]  # 5秒後に終了
```

## 注意事項
現在のバージョンは機能の実装フレームワークのみを提供しています。実際の機能は今後実装される予定です。
