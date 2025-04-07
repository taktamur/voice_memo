namespace :voicememo do
  desc "USB接続したボイスレコーダーからMP3ファイルを取り込む"
  task :sync do
    sh "~/bin/voice_sync.sh"
  end

  desc "MP3ファイルをテキストに変換する"
  task :trans do
    sh "~/bin/voice_trans.sh"
  end
  
  desc "Streamlitをインストールする"
  task :install_streamlit do
    sh "pip install streamlit"
    puts "Installed Streamlit"
  end
  
  desc "ボイスメモのStreamlitビューアを起動する"
  task :view => :install_streamlit do
    voice_memo_dir = File.expand_path("~/proj/voice_memo")
    sh "cd #{voice_memo_dir}/streamlit && streamlit run list.py"
  end
end