# cisco (v1.1.0)

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

import random
import re
from typing import AnyStr


class CiscoPassword:
    def __init__(self, string: str):
        self.string: str = string

        self.xlat: list[int] = [
            0x64, 0x73, 0x66, 0x64, 0x3b,
            0x6b, 0x66, 0x6f, 0x41, 0x2c,
            0x2e, 0x69, 0x79, 0x65, 0x77,
            0x72, 0x6b, 0x6c, 0x64, 0x4a,
            0x4b, 0x44, 0x48, 0x53, 0x55,
            0x42, 0x73, 0x67, 0x76, 0x63,
            0x61, 0x36, 0x39, 0x38, 0x33,
            0x34, 0x6e, 0x63, 0x78, 0x76,
            0x39, 0x38, 0x37, 0x33, 0x32,
            0x35, 0x34, 0x6b, 0x3b, 0x66,
            0x67, 0x38, 0x37
        ]

    def encrypt(self) -> str:
        salt: int = random.randint(0, 15)
        final_password: str = "%02d" % salt

        for i in range(len(self.string)):
            final_password += "%02x" % (ord(self.string[i]) ^ self.xlat[salt])

            salt += 1

            if salt == 51:
                salt = 0

        return final_password

    def decrypt(self) -> str:
        cipher: str = self.string
        decipher: str = ""

        regex: re.Pattern[AnyStr] = re.compile("(^[0-9A-Fa-f]{2})([0-9A-Fa-f]+)")

        result: re.Match[str] | None = regex.search(cipher)

        start, e = int(result.group(1)), result.group(2)

        for pos in range(0, len(e), 2):
            i: int = int(e[pos:pos + 2], 16)

            if start <= 50:
                char: str = "%c" % (i ^ self.xlat[start])
                start += 1

            if start == 51:
                start: int = 0

            decipher += char

        return decipher
