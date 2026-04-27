"""Unity WebGL 本地开发服务器（后台模式）

直接运行：python _server.py <目录> <端口> <PID文件>
由 serve-start.sh 调用，不要直接使用。
"""

import os
import sys
import signal
from functools import partial
from http.server import HTTPServer, SimpleHTTPRequestHandler

MIME = {
    ".wasm": "application/wasm",
    ".data": "application/octet-stream",
    ".unityweb": "application/octet-stream",
    ".mem": "application/octet-stream",
    ".js": "application/javascript",
    ".json": "application/json",
}


class WebGLHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cross-Origin-Opener-Policy", "same-origin")
        self.send_header("Cross-Origin-Embedder-Policy", "require-corp")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        super().end_headers()

    def guess_type(self, path):
        base = path
        if path.endswith(".gz") or path.endswith(".br"):
            base = path[: path.rfind(".")]
        for ext, mime in MIME.items():
            if base.endswith(ext):
                return mime
        return super().guess_type(path)

    def send_head(self):
        path = self.translate_path(self.path)
        if os.path.isfile(path):
            for suffix, encoding in [(".gz", "gzip"), (".br", "br")]:
                if path.endswith(suffix):
                    f = open(path, "rb")
                    self.send_response(200)
                    self.send_header("Content-Type", self.guess_type(path))
                    self.send_header("Content-Encoding", encoding)
                    self.send_header(
                        "Content-Length", str(os.fstat(f.fileno()).st_size)
                    )
                    self.end_headers()
                    return f
        return super().send_head()

    def log_message(self, fmt, *args):
        pass  # 静默


def main():
    serve_dir = sys.argv[1]
    port = int(sys.argv[2])
    pid_file = sys.argv[3]

    # 写入 PID（Windows 原生 PID）
    with open(pid_file, "w") as f:
        f.write(str(os.getpid()))

    handler = partial(WebGLHandler, directory=serve_dir)
    server = HTTPServer(("0.0.0.0", port), handler)

    def shutdown_handler(*_):
        server.shutdown()
        sys.exit(0)

    signal.signal(signal.SIGTERM, shutdown_handler)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        try:
            os.remove(pid_file)
        except OSError:
            pass


if __name__ == "__main__":
    main()
