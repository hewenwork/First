import json
import shutil
from http.server import HTTPServer, BaseHTTPRequestHandler


class Requests(BaseHTTPRequestHandler):
    def handle(self):
        print("data", self.rfile.readline().decode())
        self.wfile.write(self.rfile.readline())

    def do_Get(self):
        print(self.requestline, "aa")

        data = {
            'result_code': '1',
            'result_desc': 'Success',
            'timestamp': '',
            'data': {'message_id': '25d55ad283aa400af464c76d713c07ad'}
        }
        self.send_response(200)
        # self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
        shutil.copyfileobj(self.send_header('Content-type', 'application/json'), self.wfile)



    def do_POST(self):
        print(self.headers)
        print(self.command)
        req_datas = self.rfile.read(int(self.headers['content-length']))  # 重点在此步!
        print(req_datas.decode())
        data = {
            'result_code': '2',
            'result_desc': 'Success',
            'timestamp': '',
            'data': {'message_id': '25d55ad283aa400af464c76d713c07ad'}
        }
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))
        return open(r"C:\Users\hewen\Desktop\Compare.py_debug.log", "rb").read()


if __name__ == '__main__':
    host = ('', 80)
    server = HTTPServer(host, Requests)
    print("Starting server, listen at: %s:%s" % host)
    server.serve_forever()
