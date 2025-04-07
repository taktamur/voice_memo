desc "ボイスメモスクリプトを~/bin/へインストール"
task :install do
  sh "cp voice_sync.sh voice_trans.sh ~/bin/"
  sh "cp voicememo.rake ~/.rake/"
  sh "chmod +x ~/bin/voice_sync.sh ~/bin/voice_trans.sh"
  puts "Installed voice scripts to ~/bin/"
end

desc "Streamlitアプリを起動する"
task :streamlit do
  sh "cd streamlit && streamlit run list.py"
end

desc "Streamlitをインストールする"
task :install_streamlit do
  sh "pip install streamlit"
  puts "Installed Streamlit"
end

# 依存関係の追加
task :streamlit => :install_streamlit