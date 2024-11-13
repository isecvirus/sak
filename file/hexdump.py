# hexdump (v1.0.0)

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

import re

class Hexdump:
    def __init__(self, file: str):
        self.file = file

    def dump(self) -> str:
        table: str = ''

        with open(self.file, "rb") as stream:
            line: int = 0
            buffer: bytes = stream.read(16)

            while buffer:
                s1: str = ' '.join([f"{c:02x}" for c in buffer])
                s1: str = s1[0:23] + ' ' + s1[23:]

                width: int = 48

                s2: str = ''.join([chr(c) if 32 <= c <= 127 else '.' for c in buffer])
                table += f"{line * 16:08x}  {s1:<{width}}  |{s2}|\n"

                line += 1
                buffer: bytes = stream.read(16)
            stream.close()

        return table.strip()

    def pick(self, dump:str) -> str|bytes:
        data = b''

        for line in dump.splitlines():
            line: str = re.sub("^[0-9A-f]+\\W+", repl='', string=line)
            line: list[str] = re.findall("^([0-9A-f ]+)", line)[0].rstrip(' ').split()
            chunk: bytes = b''.join([bytes.fromhex(byte) for byte in line])

            data += chunk

        return data