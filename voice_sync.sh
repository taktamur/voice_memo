#!/bin/bash

# 設定
VOICE_ROOT_DIR="/Volumes/NO NAME/VOICE" # 空白を含むパスはダブルクォートで囲む
VOICE_COPY_DIR="${HOME}/.voice_memo"    # ホームディレクトリに保存

# ボイスレコーダーの接続チェックとMP3ファイルの確認
check_device() {
    echo "ボイスレコーダーの接続を確認中..."
    
    if [ ! -d "/Volumes/NO NAME" ]; then
        echo "エラー: ボイスレコーダーが接続されていないか、マウントされていません"
        echo "デバイスを接続して再度実行してください"
        exit 1
    fi
    
    if [ ! -d "${VOICE_ROOT_DIR}" ]; then
        echo "エラー: ${VOICE_ROOT_DIR} ディレクトリが見つかりません"
        echo "ボイスレコーダーの構成が想定と異なります"
        exit 1
    fi
    
    echo "ボイスレコーダーが正常に接続されています"
    
    # MP3ファイルの存在確認
    echo "${VOICE_ROOT_DIR}内のMP3ファイルを検索中..."
    find_mp3_files "${VOICE_ROOT_DIR}"
    
    if [ ${#MP3_FILES[@]} -eq 0 ]; then
        echo "${VOICE_ROOT_DIR}内にMP3ファイルが見つかりませんでした"
        exit 0
    fi
    
    echo "${#MP3_FILES[@]}個のMP3ファイルが見つかりました"
}

# MP3ファイルをリストアップする関数
find_mp3_files() {
    local dir="$1"
    local mp3_files=()
    local mp3_count=0
    
    # macOS互換の方法でファイルを処理する
    while IFS= read -r -d $'\0' mp3_file; do
        mp3_files[mp3_count]="${mp3_file}"
        ((mp3_count++))
    done < <(find "${dir}" -name "*.MP3" -print0)
    
    # グローバル変数として結果を返す
    MP3_FILES=("${mp3_files[@]}")
    return ${mp3_count}
}

# ボイスレコーダーのデータをコピーする関数
copy_files() {
    
    # 出力先ディレクトリがなければ作成する
    if [ ! -d "${VOICE_COPY_DIR}" ]; then
        mkdir -p "${VOICE_COPY_DIR}"
    fi
    
    for (( i=0; i<${#MP3_FILES[@]}; i++ )); do
        mp3_file="${MP3_FILES[$i]}"
        echo "処理中 $((i+1))/${#MP3_FILES[@]}: ${mp3_file}"
        
        # ファイルの更新日時を取得してタイムスタンプ形式に変換
        timestamp=$(date -r "${mp3_file}" "+%Y%m%d_%H%M%S")
        new_file_name="${VOICE_COPY_DIR}/${timestamp}.MP3"
        
        # ファイルをコピー
        cp "${mp3_file}" "${new_file_name}"
    done
    
    echo "すべてのMP3ファイルのコピーが完了しました"
}

# ボイスレコーダーのデータを削除する関数
clean_files() {
    echo "削除対象のMP3ファイルが${#MP3_FILES[@]}個見つかりました"
    
    for (( i=0; i<${#MP3_FILES[@]}; i++ )); do
        mp3_file="${MP3_FILES[$i]}"
        echo "削除中 $((i+1))/${#MP3_FILES[@]}: ${mp3_file}"
        rm "${mp3_file}"
    done
    
    echo "すべてのMP3ファイルが削除されました"
}

# ボイスレコーダーをアンマウントする関数
unmount_drive() {
    device_name=$(basename "${VOICE_ROOT_DIR}")
    echo "USBドライブをアンマウント中..."
    
    # 空白を含むボリューム名を正しく扱う
    if diskutil unmount "/Volumes/NO NAME"; then
        echo "USBドライブが安全にアンマウントされました。取り外し可能です。"
    else
        echo "ドライブのアンマウント中にエラーが発生しました。使用中のファイルがないか確認してください。"
    fi
}

# メイン処理 - 常にallの動作を実行
echo "ボイスレコーダーのデータ処理を開始します..."

# デバイスチェック処理
check_device

# コピー処理
copy_files

# 削除処理
clean_files

# アンマウント処理
unmount_drive

echo "すべての処理が完了しました"