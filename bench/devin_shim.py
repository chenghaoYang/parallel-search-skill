#!/usr/bin/env python3
"""Local pass-through proxy that makes devin2api's Responses output acceptable to Grok Build.

Grok Build's client requires usage.output_tokens_details (and usage itself); the local devin2api
omits them, so every swe-2 call fails with `serialization error: missing field output_tokens_details`.
This proxy forwards everything unchanged (headers included, so the provider's own key is used)
and only fills in missing usage fields, in plain JSON bodies and in SSE `data:` events.

usage: devin_shim.py [--listen 3004] [--upstream http://127.0.0.1:3003]
Point a Grok model provider at http://127.0.0.1:<listen>/v1 (see skills/deep-search/references/harness.md).
"""

import http.client
import json
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

ARGS = sys.argv[1:]
LISTEN = int(ARGS[ARGS.index("--listen") + 1]) if "--listen" in ARGS else 3004
UP = urlparse(ARGS[ARGS.index("--upstream") + 1] if "--upstream" in ARGS else "http://127.0.0.1:3003")
HOP = {"host", "content-length", "connection", "transfer-encoding", "accept-encoding", "keep-alive"}


def fix_usage(u):
    if not isinstance(u, dict):
        u = {}
    for k in ("input_tokens", "output_tokens", "total_tokens"):
        if not isinstance(u.get(k), int):
            u[k] = 0
    if not isinstance(u.get("input_tokens_details"), dict):
        u["input_tokens_details"] = {"cached_tokens": 0}
    if not isinstance(u.get("output_tokens_details"), dict):
        u["output_tokens_details"] = {"reasoning_tokens": 0}
    return u


def patch(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "usage":
                obj[k] = fix_usage(v)
            else:
                patch(v)
    elif isinstance(obj, list):
        for v in obj:
            patch(v)
    return obj


def patch_line(line):
    if not line.startswith(b"data:"):
        return line
    body = line[5:].strip()
    try:
        data = json.loads(body)
    except ValueError:
        return line
    return b"data: " + json.dumps(patch(data), ensure_ascii=False).encode() + b"\n"


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, *a):
        pass

    def do_GET(self):
        self.proxy()

    def do_POST(self):
        self.proxy()

    def chunk(self, data):
        self.wfile.write(b"%x\r\n%s\r\n" % (len(data), data))
        self.wfile.flush()

    def proxy(self):
        n = int(self.headers.get("Content-Length") or 0)
        body = self.rfile.read(n) if n else None
        headers = {k: v for k, v in self.headers.items() if k.lower() not in HOP}
        headers["Accept-Encoding"] = "identity"
        conn = http.client.HTTPConnection(UP.hostname, UP.port or 80, timeout=900)
        try:
            conn.request(self.command, self.path, body=body, headers=headers)
            resp = conn.getresponse()
        except OSError as e:
            msg = json.dumps({"error": {"message": f"devin_shim upstream error: {e}"}}).encode()
            self.send_response(502)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(msg)))
            self.send_header("Connection", "close")
            self.end_headers()
            self.wfile.write(msg)
            return
        ctype = resp.getheader("Content-Type", "")
        self.send_response(resp.status)
        for k, v in resp.getheaders():
            if k.lower() not in HOP and k.lower() != "content-encoding":
                self.send_header(k, v)
        self.send_header("Connection", "close")
        if "text/event-stream" in ctype:
            self.send_header("Transfer-Encoding", "chunked")
            self.end_headers()
            buf = b""
            while True:
                data = resp.read1(65536)
                if not data:
                    break
                buf += data
                while b"\n" in buf:
                    line, buf = buf.split(b"\n", 1)
                    self.chunk(patch_line(line + b"\n"))
            if buf:
                self.chunk(patch_line(buf))
            self.wfile.write(b"0\r\n\r\n")
            self.wfile.flush()
        else:
            data = resp.read()
            if "json" in ctype:
                try:
                    data = json.dumps(patch(json.loads(data)), ensure_ascii=False).encode()
                except ValueError:
                    pass
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        conn.close()


if __name__ == "__main__":
    ThreadingHTTPServer(("127.0.0.1", LISTEN), Handler).serve_forever()
