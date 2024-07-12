# combination (v1.0.0)

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


class Upper:
    def __init__(self, word: str, size: int = None):
        self.word = word
        self.size = len(word) if size is None else size

        assert 1 <= self.size <= len(self.word), f"The max portion should be in the range of the word's length"

    def total(self) -> int:
        return 2 ** len(self.word[:self.size])

    def bin_map(self) -> list[list[int]]:
        """
        Generates a binary map for the word

        :return: example
            [
                [0, 0, 0, 0], [1, 0, 0, 0], [0, 1, 0, 0], [1, 1, 0, 0],
                 t  e  s  t    T  e  s  t    t  E  s  t    T  E  s  t

                [0, 0, 1, 0], [1, 0, 1, 0], [0, 1, 1, 0], [1, 1, 1, 0],
                 t  e  S  t    T  e  S  t    t  E  S  t    T  E  S  t

                [0, 0, 0, 1], [1, 0, 0, 1], [0, 1, 0, 1], [1, 1, 0, 1],
                 t  e  s  T    T  e  s  T    t  E  s  T    T  E  s  T

                [0, 0, 1, 1], [1, 0, 1, 1], [0, 1, 1, 1], [1, 1, 1, 1]
                 t  e  S  T    T  e  S  T    t  E  S  T    T  E  S  T
            ]
        """

        result: list[list[int]] = []
        word: str = self.word

        for i in range(2 ** len(word)):  # 2 = for binary
            x: list[int] = []
            for j in range(len(word)):
                x.append((i >> j) & 1)
            result.append(x)

        return result

    def combine(self) -> list[str]:
        final: list[str] = []
        word: str = self.word

        part: str = word[:self.size]
        rest: str = word[self.size:]

        for i in range(2 ** len(part)):
            comb: str = ""

            for j, char in enumerate(part):
                if char.isalpha():
                    if (i >> j) & 1:
                        comb += char.upper()
                    else:
                        comb += char.lower()
                else:
                    comb += char

            final.append(comb + rest)

        return final