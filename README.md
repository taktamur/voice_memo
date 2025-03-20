# ボイスメモ文字起こしツール

ボイスレコーダーを使った文字起こしを自動化するスクリプト集

## 機能

- (1)ボイスレコーダーから MP3 ファイルを Mac に転送する
- (2)転送した MP3 ファイルをテキスト起こし
- (1)(2)を呼び出す Rake タスク

## やっていること

ステップは以下２つ

1. Mac に接続したら、ボイスレコーダーの音声ファイルを Mac に移す
   - ボイスレコーダーの音声ファイルはこの段階で削除する
2. 音声ファイルからテキスト起こしを行う

## ファイル構成

- `voice_sync.sh` - ボイスレコーダーから MP3 ファイルを転送するスクリプト
- `voice_trans.sh` - MP3 ファイルをテキストに変換するスクリプト
- `Rakefile` - インストール用タスク
- `voicememo.rake` - ボイスメモ関連の Rake タスク

## パスについて

- USB 接続した際に、ボイスレコーダーは `/Volumes/NO NAME/VOICE` にマウントされる想定
  例：

```
/Volumes/NO NAME/VOICE
├── A
│   ├── REC005.MP3
│   ├── REC006.MP3
│   ├── ...
│   └── REC013.MP3
├── B
├── C
└── D
```

処理する対象の MP3 ファイルはこのように格納されている想定。A〜D のどこにあるかは場合による

- Mac 側の保存先は、`${HOME}/.voice_memo/`
  - 保存する際に、ファイル名をタイムスタンプ（YYYYMMDD_HHMMSS.MP3）に変換する

## インストール方法

```bash
rake install
```

上記コマンドで以下の処理を実行する：

- スクリプトファイルを `~/bin/` にコピー
- Rake タスクファイルを `~/.rake/` にコピー
- スクリプトファイルに実行権限を付与

## 使用方法

### 1. ボイスレコーダーの音声ファイルを Mac に転送

```bash
~/bin/voice_sync.sh
```

または

```bash
rake voicememo:sync
```

このスクリプトは以下の処理を行う：

1. ボイスレコーダーの接続チェック
2. MP3 ファイルの検索
3. MP3 ファイルを `${HOME}/.voice_memo/` へタイムスタンプ名でコピー
4. 元の MP3 ファイルを削除
5. ボイスレコーダーを安全にアンマウント

### 2. テキスト起こし

```bash
~/bin/voice_trans.sh
```

または

```bash
rake voicememo:trans
```

このスクリプトは以下の処理を行う：

1. `${HOME}/.voice_memo/` 内の MP3 ファイルをリストアップ
2. 未処理（対応するテキストファイルがない）の MP3 ファイルを特定
3. Whisper を使用してテキスト起こし
4. テキストファイルを元の MP3 ファイルと同じディレクトリに保存

## テキスト起こしについて

テキスト起こしは、OpenAI の[Whisper](https://github.com/openai/whisper)を利用する

### Whisper のインストール方法

```bash
# 前提ライブラリのインストール
brew install ffmpeg

# Whisperのインストール
pip install -U openai-whisper
```

### Whisper のオプション設定

スクリプトでは以下のオプションを使用している

- `--output_format=txt` - テキスト形式で出力
- `--output_dir="${TMP_DIR}"` - 一時的な出力先を指定
- `--language=ja` - 日本語で認識
