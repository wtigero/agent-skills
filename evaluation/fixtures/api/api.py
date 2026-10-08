import argparse
from http.server import BaseHTTPRequestHandler, HTTPServer
import json


def invoice():
    return {"invoice_id": "inv-7", "total_cents": 1250}


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/invoice":
            self.send_error(404)
            return
        body = json.dumps(invoice()).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=0)
    args = parser.parse_args()
    server = HTTPServer(("127.0.0.1", args.port), Handler)
    print(server.server_port, flush=True)
    server.serve_forever()
