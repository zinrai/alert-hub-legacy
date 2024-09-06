#!/usr/bin/env python3
import http.server
import os
import sys

# スクリプトのディレクトリをPythonパスに追加
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# CGIスクリプトのディレクトリを指定
cgi_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cgi-bin")

# カレントディレクトリをCGIスクリプトのディレクトリに変更
os.chdir(cgi_directory)

# ポート番号を指定（例: 8000）
port = 8000

# CGIHTTPRequestHandlerを使用してCGIスクリプトの実行を可能にする
handler = http.server.CGIHTTPRequestHandler
handler.cgi_directories = ["/"]

# サーバーを起動
server_address = ('', port)
httpd = http.server.HTTPServer(server_address, handler)

print(f"CGIサーバーがポート {port} で起動しました")
print(f"CGIスクリプトのディレクトリ: {cgi_directory}")
print("サーバーを停止するには、Ctrl+Cを押してください")

try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print("\nサーバーを停止しています...")
    httpd.server_close()
    print("サーバーが停止しました。")
