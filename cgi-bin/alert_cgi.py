#!/usr/bin/env python3
import cgi
import json
import os
import sys
import traceback

# 親ディレクトリをPythonパスに追加
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from alert_manager import AlertManager

# データベースファイルのパスを設定
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db.sqlite3')
alert_manager = AlertManager(db_path)

def main():
    try:
        print("Content-Type: application/json; charset=utf-8")
        print()

        if os.environ['REQUEST_METHOD'] != 'POST':
            raise ValueError("Only POST method is allowed")

        form = cgi.FieldStorage()

        alert_manager = AlertManager()

        required_fields = ['subject', 'body', 'identifier', 'urgency']
        if not all(field in form for field in required_fields):
            raise ValueError("Missing required fields")

        try:
            alert_manager.add_alert(
                form.getvalue('subject'),
                form.getvalue('body'),
                form.getvalue('identifier'),
                form.getvalue('urgency')
            )
            print(json.dumps({"status": "success", "message": "Alert added successfully"}, ensure_ascii=False))
        except ValueError as e:
            print(json.dumps({"status": "error", "message": str(e)}, ensure_ascii=False))

    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}, ensure_ascii=False))
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
