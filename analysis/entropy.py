# entrpy (v1.0.0)

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

import math
from collections import defaultdict
from typing import NoReturn, Any


class Entropy:
    def __init__(self, data: bytes | str):
        self.data: bytes | str = data

    def set_data(self, data: bytes | str) -> NoReturn:
        self.data = data

    def get_data(self) -> bytes | str:
        return self.data

    def get(self, fraction: int = 16) -> float:
        """
        Get the entropy value of the provided data
        :param fraction:
        :return:
        """

        charCount: defaultdict[Any, int] = defaultdict(int)
        entropy: float = 0.0
        data: bytes | str = self.data

        for c in data:
            charCount[c] += 1

        for count in charCount.values():
            freq: float = count / len(data)
            entropy -= freq * (math.log(freq) / math.log(2))

        return round(entropy, fraction)
