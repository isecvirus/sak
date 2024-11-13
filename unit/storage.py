# computer (v1.1.0)

"""
Copyright (c) virus, All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice,
   this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

class Storage:
    """
    Usage:
        storage = Storage(1000, "GB")
        storage.TB # 1.0
    """

    units = {
        "b": 1e0, "B": 1e0 / 8,
        "Kb": 1e3, "KB": 1e3 / 8,
        "Mb": 1e6, "MB": 1e6 / 8,
        "Gb": 1e9, "GB": 1e9 / 8,
        "Tb": 1e12, "TB": 1e12 / 8,
        "Pb": 1e15, "PB": 1e15 / 8,
        "Eb": 1e18, "EB": 1e18 / 8,
        "Zb": 1e21, "ZB": 1e21 / 8,
        "Yb": 1e24, "YB": 1e24 / 8
    }

    def __init__(self, size: float, unit: str = 'B'):
        self.size = size
        self.unit = unit

    def __getattr__(self, unit):
        if unit in self.units:
            return self.size * (self.units[self.unit] / self.units[unit])
        raise AttributeError(f"{unit!r} not supported unit!")