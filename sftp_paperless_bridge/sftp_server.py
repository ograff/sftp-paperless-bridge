import os
from io import BytesIO
from typing import Any, Callable

from paramiko import (
    ServerInterface,
    SFTPAttributes,
    SFTPHandle,
    SFTPServerInterface,
)
from paramiko.common import AUTH_SUCCESSFUL, OPEN_SUCCEEDED
from paramiko.sftp import SFTP_OP_UNSUPPORTED


class MyServer(ServerInterface):
    def check_auth_password(self, username: Any, password: Any) -> int:
        # all are allowed
        return AUTH_SUCCESSFUL

    def check_channel_request(self, kind: Any, chanid: Any) -> int:
        return OPEN_SUCCEEDED


class MySFTPHandle(SFTPHandle):
    def __init__(self, name: str, close_callback: Callable[[str, bytes], None], flags: int):
        self.name = name
        self.writefile = BytesIO()
        self.close_callback = close_callback
        super().__init__(flags)

    def close(self) -> None:
        self.close_callback(self.name, self.writefile.getvalue())
        self.writefile.close()


def create_sftp_server(close_callback: Callable[[str, bytes], None]) -> type[SFTPServerInterface]:
    class MySFTPServer(SFTPServerInterface):
        def __init__(self, server: ServerInterface, *args: Any, **kwargs: Any):
            self.close_callback = close_callback
            super().__init__(server, *args, **kwargs)

        def open(self, path: str, flags: int, attr: SFTPAttributes) -> int | MySFTPHandle:
            if not (flags & os.O_WRONLY):
                return SFTP_OP_UNSUPPORTED
            fobj = MySFTPHandle(path, self.close_callback, flags)
            return fobj

    return MySFTPServer
