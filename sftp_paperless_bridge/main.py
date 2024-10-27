import logging
import os
import socket
from io import StringIO
from typing import Callable

import paramiko
import requests

from . import sftp_server


def start_server(close_callback: Callable[[str, bytes], None], sftp_pass: str, key: None | str = None) -> None:
    logging.basicConfig(level=logging.DEBUG)
    paramiko_logger = logging.getLogger("paramiko")
    paramiko_logger.setLevel(logging.DEBUG)
    server_key = paramiko.RSAKey.generate(bits=1024) if key is None else paramiko.RSAKey.from_private_key(StringIO(key))

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    server_socket.bind(("0.0.0.0", 2222))
    server_socket.listen(10)
    sessions = []
    while True:
        sessions = [session for session in sessions if session.is_active()]
        conn, addr = server_socket.accept()
        transport = paramiko.Transport(conn)
        transport.add_server_key(server_key)
        transport.set_subsystem_handler("sftp", paramiko.SFTPServer, sftp_server.create_sftp_server(close_callback))
        server = sftp_server.MyServer(password=sftp_pass)
        transport.start_server(server=server)
        _channel = transport.accept()
        sessions.append(transport)


def create_upload_handler(api_key: str, url: str) -> Callable[[str, bytes], None]:
    def handle_upload(name: str, data: bytes) -> None:
        print(f"Received {len(data)} bytes for file {name}")
        out = requests.post(
            f"{url}/api/documents/post_document/",
            headers={
                "Authorization": f"Token {api_key}",
            },
            files={"document": (name, data)},
            timeout=30,
        )
        out.raise_for_status()

    return handle_upload


def main() -> None:
    # Start an SFTP server
    key = os.environ.get("HOST_KEY")
    url = os.environ.get("API_URL")
    api_key = os.environ.get("API_KEY")
    sftp_pass = os.environ.get("SFTP_PASS")

    assert key is not None, "HOST_KEY environment variable must be set"
    assert url is not None, "API_URL environment variable must be set"
    assert api_key is not None, "API_KEY environment variable must be set"
    assert sftp_pass is not None, "SFTP_PASS environment variable must be set"

    start_server(create_upload_handler(api_key, url), sftp_pass=sftp_pass, key=key)
