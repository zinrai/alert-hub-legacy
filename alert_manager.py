import sqlite3
import os

class AlertManager:
    STATUS_MAP = {
        'new': '未対応',
        'in_progress': '対応中',
        'resolved': '完了',
        'on_hold': '保留'
    }

    def __init__(self, db_path=None):
        if db_path is None:
            # スクリプトのディレクトリを取得
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # cgi-binディレクトリへのパスを構築
            cgi_bin_dir = os.path.join(current_dir, 'cgi-bin')
            # データベースファイルへのパスを構築
            self.db_path = os.path.join(cgi_bin_dir, 'db.sqlite3')
        else:
            self.db_path = db_path
        self.initialize_db()

    def initialize_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS alerts
                     (id INTEGER PRIMARY KEY,
                      subject TEXT,
                      body TEXT,
                      identifier TEXT UNIQUE,
                      urgency TEXT,
                      status TEXT DEFAULT 'new')''')
        conn.commit()
        conn.close()

    def identifier_exists(self, identifier):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM alerts WHERE identifier = ?", (identifier,))
        count = c.fetchone()[0]
        conn.close()
        return count > 0

    def add_alert(self, subject, body, identifier, urgency):
        if self.identifier_exists(identifier):
            raise ValueError(f"Alert with identifier '{identifier}' already exists")

        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        try:
            c.execute("INSERT INTO alerts (subject, body, identifier, urgency, status) VALUES (?, ?, ?, ?, 'new')",
                      (subject, body, identifier, urgency))
            conn.commit()
        except sqlite3.IntegrityError:
            conn.rollback()
            raise ValueError(f"Alert with identifier '{identifier}' already exists")
        finally:
            conn.close()

    def update_status(self, alert_id, status):
        if status not in self.STATUS_MAP:
            raise ValueError(f"Invalid status: {status}")

        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("UPDATE alerts SET status = ? WHERE id = ?", (status, alert_id))
        if c.rowcount == 0:
            conn.close()
            raise ValueError(f"No alert found with id: {alert_id}")
        conn.commit()
        conn.close()

    def get_all_alerts(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT * FROM alerts")
        alerts = c.fetchall()
        conn.close()
        return [self._convert_status_to_japanese(alert) for alert in alerts]

    def get_alert_details(self, alert_id):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT * FROM alerts WHERE id = ?", (alert_id,))
        alert = c.fetchone()
        conn.close()
        return self._convert_status_to_japanese(alert) if alert else None

    def _convert_status_to_japanese(self, alert):
        if alert:
            alert_list = list(alert)
            alert_list[5] = self.STATUS_MAP.get(alert_list[5], alert_list[5])
            return tuple(alert_list)
        return alert

    @classmethod
    def get_status_options(cls):
        return [(k, v) for k, v in cls.STATUS_MAP.items()]

    @classmethod
    def get_english_status(cls, japanese_status):
        for eng, jpn in cls.STATUS_MAP.items():
            if jpn == japanese_status:
                return eng
        return japanese_status  # フォールバック
