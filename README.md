# alert-hub-legacy

This application is a simple CGI-based alert management system created to verify integration with CGI systems. It allows users to register alerts, view a list of alerts, see alert details, and update alert statuses.

Please be aware that Python's CGI module is deprecated since version 3.11 and will be removed in version 3.13. This application is testing purposes only and should not be used in production environments.

https://docs.python.org/3/library/cgi.html

## Installing Dependencies

Create and activate a virtual environment:

```
$ python3 -m venv venv
$ source venv/bin/activate
```

Install the required packages using the following command:

```bash
$ pip install -r requirements.txt
```

## Starting the Server

Start the server with the following command:

```bash
$ python3 cgi_server.py
```

The server will start by default at http://localhost:8000.

## Registering an Alert

To register an alert, use the following curl command:

```bash
$ curl -X POST "http://localhost:8000/alert_cgi.py" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     --data-urlencode "subject=システム障害" \
     --data-urlencode "body=データベースサーバーがダウンしています。至急確認してください。" \
     --data-urlencode "identifier=SYS001" \
     --data-urlencode "urgency=HIGH"
```

## Viewing Alert List

Access the following URL in your browser:

```
http://localhost:8000/cgi-bin/alert_list_details.py?action=list
```

## Viewing Alert Details

Access the following URL in your browser (replace `<alert_id>` with the actual alert ID):

```
http://localhost:8000/cgi-bin/alert_list_details.py?action=details&id=<alert_id>
```

## License

This project is licensed under the MIT License - see the [LICENSE](https://opensource.org/license/mit) for details.
