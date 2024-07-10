# gigabyte (v1.0.0)

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


class Gigabyte(float):
    def __init__(self, n: float | int):
        self.n: float | int = n

    def bit(self) -> float:
        return self * 8_000_000_000

    def byte(self) -> float:
        return self * 1_000_000_000

    def kilobit(self) -> float:
        return self * 8_000_000

    def kilobyte(self) -> float:
        return self * 1_000_000

    def megabit(self) -> float:
        return self * 8_000

    def megabyte(self) -> float:
        return self * 1_000

    def gigabit(self) -> float:
        return self * 8

    def terabit(self) -> float:
        return self / 125

    def terabyte(self) -> float:
        return self / 1_000

    def petabit(self) -> float:
        return self / 125_000

    def petabyte(self) -> float:
        return self / 1_000_000

    def exabit(self) -> float:
        return self / 125_000_000

    def exabyte(self) -> float:
        return self / 1_000_000_000

    def zettabit(self) -> float:
        return self / 125_000_000_000

    def zettabyte(self) -> float:
        return self / 1_000_000_000_000

    def yottabit(self) -> float:
        return self / 125_000_000_000_000

    def yottabyte(self) -> float:
        return self / 1_000_000_000_000_000
