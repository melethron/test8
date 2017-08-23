#!/usr/bin/env python3
import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from tinydb import TinyDB, Query
from validate_email import validate_email


DB = TinyDB('db.json')


class TaskServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write("<h1>Hello!</h1>".encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode(encoding='utf-8')
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        post_dict = dict(x.split('=') for x in post_data.split('&'))
        #print(check_date("25-01-1989"))
        # Looking for form match with POST
        for entry in DB.all():
            #print(set(entry.values()).issuperset(set([x for x in post_dict])))
            if set(entry.values()).issuperset(set([x for x in post_dict])) and check_request_fields(post_dict):
                self.wfile.write(entry['name'].encode('utf-8'))


def check_date(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        try:
            datetime.datetime.strptime(date_text, '%d-%m-%Y')
        except ValueError:
            return False
    return True


def check_phone(phone_number):
    if len(phone_number) != 16:
        return False
    for i in range(3, 12):
        if i in [6, 10, 13]:
            if phone_number[i] != ' ':
                return False
        elif not phone_number[i].isalnum():
            return False
    if phone_number[:3] != '+7 ':
        return False
    return True


def check_mail(email):
    return validate_email(email)


def check_request_fields(request):
    for key in request:
        if key == 'date':
            return check_date(request[key])
        elif key == 'phone':
            return check_phone(request[key])
        elif key == 'email':
            return check_mail(request[key])
    return True



def run(server_class=HTTPServer, handler_class=TaskServer):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    print("Starting server")
    httpd.serve_forever()


run()
