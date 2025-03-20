namespace :voicememo do
  desc "USB接続したボイスレコーダーからMP3ファイルを取り込む"
  task :sync do
    sh "~/bin/voice_sync.sh"
  end

  desc "MP3ファイルをテキストに変換する"
  task :trans do
    sh "~/bin/voice_trans.sh"
  end
end