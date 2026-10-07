import argparse
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from pathlib import Path


def serve(data, port):
    class Handler(BaseHTTPRequestHandler):
        def send_json(self, value, status=200):
            body = json.dumps(value).encode()
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            if self.path == "/health":
                self.send_json({"ok": True})
            elif self.path == "/tasks":
                self.send_json(json.loads(data.read_text(encoding="utf-8")))
            else:
                self.send_error(404)

        def do_POST(self):
            if self.path != "/tasks":
                self.send_error(404)
                return
            task = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
            tasks = json.loads(data.read_text(encoding="utf-8"))
            tasks.append(task)
            data.write_text(json.dumps(tasks), encoding="utf-8")
            self.send_json(task, 201)

    data.parent.mkdir(parents=True, exist_ok=True)
    if not data.exists():
        data.write_text("[]", encoding="utf-8")
    server = HTTPServer(("127.0.0.1", port), Handler)
    print(json.dumps({"url": f"http://127.0.0.1:{server.server_port}"}), flush=True)
    server.serve_forever()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--port", type=int, default=0)
    args = parser.parse_args()
    serve(args.data, args.port)
