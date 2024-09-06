#!/usr/bin/env python3
import cgi
import os
import sys
import json
import traceback

# 親ディレクトリをPythonパスに追加
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from jinja2 import Environment, FileSystemLoader
from alert_manager import AlertManager

# データベースファイルのパスを設定
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db.sqlite3')
alert_manager = AlertManager(db_path)

def main():
    try:
        print("Content-Type: text/html; charset=utf-8")
        print()

        form = cgi.FieldStorage()
        action = form.getvalue('action', 'list')
        alert_id = form.getvalue('id')

        alert_manager = AlertManager()

        # テンプレートディレクトリのパスを修正
        template_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'templates')
        env = Environment(loader=FileSystemLoader(template_dir))

        if action == 'list':
            template = env.get_template('alert_list.html')
            alerts = alert_manager.get_all_alerts()
            print(template.render(alerts=alerts))
        elif action == 'details' and alert_id:
            if form.getvalue('update_status'):
                new_status = form.getvalue('new_status')
                alert_manager.update_status(alert_id, new_status)

            template = env.get_template('alert_details.html')
            alert = alert_manager.get_alert_details(alert_id)
            if alert:
                status_options = alert_manager.get_status_options()
                print(template.render(alert=alert, status_options=status_options))
            else:
                print("<h1>アラートが見つかりません</h1>")
                print(f"<p>ID {alert_id} のアラートは存在しません。</p>")
        else:
            raise ValueError("無効なアクション")

    except Exception as e:
        print("<h1>エラーが発生しました</h1>")
        print(f"<p>{str(e)}</p>")
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
