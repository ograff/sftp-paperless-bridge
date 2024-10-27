import os
import socket
import time
from io import StringIO
from typing import Callable

import paramiko

from . import sftp_server


def start_server(close_callback: Callable[[str, bytes], None], key: None | str = None) -> None:
    server_key = paramiko.RSAKey.generate(bits=1024) if key is None else paramiko.RSAKey.from_private_key(StringIO(key))

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    server_socket.bind(("0.0.0.0", 2222))
    server_socket.listen(10)
    while True:
        conn, addr = server_socket.accept()
        transport = paramiko.Transport(conn)
        transport.add_server_key(server_key)
        transport.set_subsystem_handler("sftp", paramiko.SFTPServer, sftp_server.create_sftp_server(close_callback))
        server = sftp_server.MyServer()
        transport.start_server(server=server)
        _channel = transport.accept()
        while transport.is_active():
            time.sleep(1)


def handle_upload(name: str, data: bytes) -> None:
    print(f"Received {len(data)} bytes for file {name}")


def main() -> None:
    # Start an SFTP server
    key = os.environ.get("HOST_KEY")

    assert key is not None, "HOST_KEY environment variable must be set"
    start_server(handle_upload, key=key)
