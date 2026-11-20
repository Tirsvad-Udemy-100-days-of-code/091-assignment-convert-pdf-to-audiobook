import socket

import pytest


def test_connecting_a_socket_is_blocked() -> None:
    with socket.socket() as sock, pytest.raises(AssertionError, match="network access"):
        sock.connect(("127.0.0.1", 9))


def test_create_connection_is_blocked() -> None:
    with pytest.raises(AssertionError, match="network access"):
        socket.create_connection(("127.0.0.1", 9))
