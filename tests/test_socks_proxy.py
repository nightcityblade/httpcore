from __future__ import annotations

import pytest

import httpcore
from httpcore._async.socks_proxy import _init_socks5_connection


class TimeoutCheckingStream(httpcore.AsyncMockStream):
    async def read(self, max_bytes: int, timeout: float | None = None) -> bytes:
        assert timeout == 5.0
        return await super().read(max_bytes, timeout)

    async def write(self, buffer: bytes, timeout: float | None = None) -> None:
        assert timeout == 5.0


@pytest.mark.anyio
async def test_socks5_connect_timeout():
    stream = TimeoutCheckingStream([b"\x05\x00", b"\x05\x00\x00\x01" + bytes(6)])
    await _init_socks5_connection(stream, host=b"example.com", port=80, timeout=5.0)
