"""Taste Vault's local server, read-only. Run: python server.py --port 4610"""

import argparse
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
from urllib.parse import unquote, urlparse


class VaultHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, directory=None, **kwargs):
        self.root = Path(directory).resolve()
        super().__init__(*args, directory=str(self.root), **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        super().end_headers()

    def list_directory(self, path):
        self.send_error(403, "Directory listing is disabled")
        return None

    # Judged on the decoded path the file is served from, so /%2eenv is /.env (#84).
    def hidden(self):
        path = unquote(urlparse(self.path).path)
        return any(segment.startswith(".") for segment in path.split("/") if segment)

    def do_HEAD(self):
        if self.hidden():
            self.send_error(404)
            return
        super().do_HEAD()

    def do_GET(self):
        path = urlparse(self.path).path
        if self.hidden():
            self.send_error(404)
            return
        if path == "/api/health":
            self.json_response(200, {"status": "ok"})
            return
        super().do_GET()

    def json_response(self, status, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def make_server(root, port):
    def handler(*args, **kwargs):
        return VaultHandler(*args, directory=root, **kwargs)

    return ThreadingHTTPServer(("127.0.0.1", port), handler)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    # The seed's port (cth9191/taste-vault), which serve.bat opens and README.md gives.
    parser.add_argument("--port", type=int, default=4610)
    args = parser.parse_args()
    server = make_server(Path(__file__).resolve().parent, args.port)
    print(
        f"Taste Vault is running at http://127.0.0.1:{server.server_port}", flush=True
    )
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
