# このリポジトリの説明

ボイスレコーダーを使った文字起こしに関するアイデアと自分用スクリプトを格納している。

## やりたいこと

散歩などで思いついたネタを、ボイスレコーダーに吹き込んでいる。
これをテキスト化したい。

ステップは以下２つ

- Mac に接続したら、ボイスレコーダーの音声ファイルを Mac に移す。
  - ボイスレコーダーの音声ファイルはこの段階で削除する
- 音声ファイルからテキスト起こしを行う。

## パスについて

- USB 接続した際に、ボイスレコーダーは /Volumes/NO\ NAME/VOICE にマウントされる
  例：

```
tak@mba2020 vo2ob % tree /Volumes/NO\ NAME/VOICE
/Volumes/NO NAME/VOICE
├── A
│   ├── REC005.MP3
│   ├── REC006.MP3
│   ├── ...
│   └── REC013.MP3
├── B
├── C
└── D
```

処理する対象の MP3 ファイルはこのように格納されています。A〜D のどこにあるかは場合による

- Mac 側の保存先は、{HOME}/.voice_memo/以下に保存する
  - 保存する際に、ファイル名をタイムスタンプ（YYYYMMDD_HHMMSS.MP3）とする。

## ボイスレコーダーの音声ファイルを Mac に移す

ボイスレコーダーは USB 接続なので、安全に抜けるように unmount も行う

## テキスト起こしについて

テキスト起こしは、cli コマンドの whisper を利用する。

### Whisper について

音声ファイルから文字起こしを行う、OpenAI の cli コマンド

- CLI ツールとして利用: `whisper input.wav --model medium --language Japanese`
- インストール方法: `pip install -U openai-whisper`
- 前提ライブラリ: `brew install ffmpeg`

## 実装方法

shell スクリプト(\*.sh)で実装する
ボイスレコーダーの音声ファイルを Mac に移す、と、テキスト起こし、それぞれを 1 つずつの sh として実装する

- この sh は他の rake タスクや n8n から呼び出される事を想定
