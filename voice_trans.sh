#!/bin/bash

# 設定
VOICE_DIR="${HOME}/.voice_memo"    # ホームディレクトリに保存
TMP_DIR="/tmp"

# VOICE_DIR内のMP3ファイルを検索
echo "${VOICE_DIR}内のMP3ファイルを検索中..."
MP3_FILES=()
while IFS= read -r -d $'\0' mp3_file; do
    MP3_FILES+=("${mp3_file}")
done < <(find "${VOICE_DIR}" -name "*.MP3" -print0)

if [ ${#MP3_FILES[@]} -eq 0 ]; then
    echo "${VOICE_DIR}内にMP3ファイルが見つかりませんでした"
    exit 0
fi

echo "${#MP3_FILES[@]}個のMP3ファイルが見つかりました"

# テキスト起こししていないファイルをリストアップ
UNPROCESSED_FILES=()
for mp3_file in "${MP3_FILES[@]}"; do
    txt_file="${mp3_file%.MP3}.txt"
    if [ ! -f "${txt_file}" ]; then
        UNPROCESSED_FILES+=("${mp3_file}")
    fi
done

if [ ${#UNPROCESSED_FILES[@]} -eq 0 ]; then
    echo "テキスト起こしが必要なファイルはありません"
    exit 0
fi

echo "${#UNPROCESSED_FILES[@]}個のテキスト起こしが必要なMP3ファイルが見つかりました"

# テキスト起こし処理
for (( i=0; i<${#UNPROCESSED_FILES[@]}; i++ )); do
    mp3_file="${UNPROCESSED_FILES[$i]}"
    echo "処理中 $((i+1))/${#UNPROCESSED_FILES[@]}: ${mp3_file}"
    
    # 言語は日本語、output_formatはtxt、output_dirはtmp
    # warningがうるさいので抑止
    PYTHONWARNINGS="ignore" whisper --output_format=txt --output_dir="${TMP_DIR}" --language=ja "${mp3_file}"
    
    # whisperの出力ファイル名
    base_name=$(basename "${mp3_file}" .MP3)
    whisper_file="${TMP_DIR}/${base_name}.txt"
    
    # whisperの出力ファイルをVOICE_DIRに移動
    cp "${whisper_file}" "$(dirname "${mp3_file}")"
done

echo "すべてのMP3ファイルのテキスト起こしが完了しました"