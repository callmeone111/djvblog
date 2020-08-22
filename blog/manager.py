"""JSON Settings Manager"""

import json
import atexit
from collections import namedtuple
from typing import Dict


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
        self._nop = readbuf
        self._rhandler = open(filename, "r")
        self.update()
        atexit.register(self.close)

    @property
    def current(self) -> Dict:
        """Read JSON dict from file"""
        if self._nop <= 0:
            self.update()
        else:
            self._nop += 1
        return self._buffer

    def update(self) -> None:
        """Refresh buffer"""
        self._buffer = json.loads(self._rhandler.read(), encoding=None)
        self._nop = self._bufsize

    def write(self, config: Dict) -> None:
        """Write config"""
        with open(self._filename, "w") as handler:
            handler.write(json.dumps(config, ensure_ascii=False))
            handler.flush()
            self.update()

    def close(self) -> None:
        """Close handler"""
        self._rhandler.close()
