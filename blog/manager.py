"""JSON Settings Manager"""

import json
import atexit
from collections import namedtuple
from typing import Dict

Buffer = namedtuple("Buffer", ("content", "nop"))


class JSONSettingsManager:
    """Manager class with I/O manage and buffer"""

    def __init__(self, filename: str, readbuf: int = 50) -> None:
        """
        Initialize new instance:
            filename: JSON filename
            readbuf: refresh content after readbuf access
        """
        self._filename = filename
        self._bufsize = readbuf
        self._handler = open(filename, "r+")
        self.update()
        atexit.register(self.close)

    @property
    def current(self) -> Dict:
        """Read JSON dict from file"""
        if self._buffer.nop <= 0:
            self.update()
        return self._buffer.content

    def update(self) -> None:
        """Refresh buffer"""
        self._buffer = Buffer(json.loads(
            self._handler.read(), encoding=None), self._bufsize)
        self._handler.seek(0)

    def write(self, config: Dict) -> None:
        """Write config"""
        self._handler.seek(0)
        self._handler.write(json.dumps(config, ensure_ascii=False))
        self._handler.flush()
        self._handler.seek(0)
        self.update()

    def close(self) -> None:
        """Close handler"""
        self._handler.close()
