# password (v1.2.0)

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
from typing import NoReturn


class Generate:
    LOWER = "abcdefghijklmnopqrstuvwxyz"
    UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    LETTERS = UPPER + LOWER
    DIGITS = NUMBERS = "0123456789"
    OCTET = "01234567"
    HEX = DIGITS + UPPER[:6] + LOWER[:6]
    PUNC = PUNCS = punctuation = r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""
    READABLES = UPPER + LOWER + DIGITS + PUNC
    WHITE = whitespace = "\t\n\v\f\r "
    PRINTABLE = READABLES + WHITE

    def __init__(self, chars: bytes | str = READABLES, separator: bytes | str = ''):
        self.chars: bytes | str = chars
        self.separator: bytes | str = separator

    def set_chars(self, chars: bytes | str) -> NoReturn:
        self.chars = chars

    def get_chars(self) -> bytes | str:
        return self.chars

    def set_separator(self, separator: bytes | str) -> NoReturn:
        self.separator = separator

    def get_separator(self) -> bytes | str:
        return self.separator

    def new(self, length: int) -> bytes | str:
        return self.get_separator().join([random.choice(self.get_chars()) for _ in range(length)])