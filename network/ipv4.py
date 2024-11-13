# ipv4 (v1.1.0)

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


class InvalidIPv4Error(ValueError):
    def __init__(self, address):
        super().__init__(f"{address!r} isn't a valid IPv4 address")


class InvalidRangeError(ValueError):
    def __init__(self, address):
        super().__init__(f"End-range ip can't be smaller than the start range: {address!r}")


class InvalidDecimalError(ValueError):
    def __init__(self, number):
        super().__init__(f"{number!r} isn't a valid decimal representation of IPv4 address")


class InvalidBinaryError(ValueError):
    def __init__(self, binary):
        super().__init__(f"{binary!r} isn't a valid binary representation of IPv4 address")


class InvalidBytesError(ValueError):
    def __init__(self, address):
        super().__init__(f"The packed IPv4 representation {address!r} isn't valid")


class IPv4:
    REGEX: str = r"(\b25[0-5]|\b2[0-4][0-9]|\b[01]?[0-9][0-9]?)(\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}"
    # The IPv4 separator
    SEP: str = '.'

    MIN_IP: int = 0x0
    MAX_IP: int = 0xffffffff
    MIN_CIDR: int = 0
    MAX_CIDR: int = 0x20

    def __init__(self, address: str):
        self.address: str = address

        if not self.valid():
            raise InvalidIPv4Error(address)

    def valid(self) -> bool:
        return isinstance(self.address, str) and (re.fullmatch(self.REGEX, self.address) is not None)

    def binary(self) -> list[int]:
        """
        Get the binary (0-1) representation of the IPv4

        :return:
        """

        octets: list[int] = []
        for o in self.address.split(self.SEP):
            octet: int = int(o)
            octets.append(int(bin(octet)[2:]))

        return octets

    def decimal(self) -> int:
        """
        Get the decimal (0-9) representation of the IPv4

        :return:
        """

        octets: list[int] = list(map(int, self.address.split(self.SEP)))

        o1: int = octets[0] << 24
        o2: int = octets[1] << 16
        o3: int = octets[2] << 8
        o4: int = octets[3]

        decimal = o1 | o2 | o3 | o4

        return decimal

    def pack(self) -> bytes:
        pack_array: bytearray = bytearray(4)
        octets: list[str] = self.address.split(IPv4.SEP)

        for i in range(4):
            pack_array[i] = int(octets[i])

        return bytes(pack_array)

    def cidr(self) -> int:
        """
        Get the cidr/prefix for an IPv4 address

        :return: IPv4.MIN_CIDR - IPv4.MAX_CIDR
        """

        return sum([str(o).count('1') for o in self.binary()])


class Range:
    def __init__(self, address: str):
        self.address: str = address

        if not IPv4(address).valid():
            raise InvalidIPv4Error(address)

    def pool(self, end: str) -> list[str]:
        """
        Generate a pool of ip addresses from range x to range y

        :param end:
        """

        ips: list[str] = []

        start: int = IPv4(self.address).decimal()
        end: int = IPv4(end).decimal()

        for decimal in range(start, end + 1):
            ip: str = Decimal(decimal).ip()
            ips.append(ip)

        return ips


class Network:
    def __init__(self, address: str):
        self.address: str = address

        if not IPv4(address).valid():
            raise InvalidIPv4Error(address)

    def range(self, cidr: int) -> tuple[str, str]:
        """
        Get the range <from>-<to> IPv4 using the prefix/cidr
        :param cidr: IPv4.MIN_CIDR - IPv4.MAX_CIDR
        :return:
        """

        network: int = IPv4(self.address).decimal()
        rest: int = IPv4.MAX_CIDR - cidr
        mask: int = IPv4.MAX_IP - (1 << rest)

        first: int = network & mask
        last: int = first | (2 ** (32 - cidr) - 1)

        return Decimal(first).ip(), Decimal(last).ip()

    def cidr(self, end: str) -> int:
        """
        Get ip cidr/prefix using <from>-<to> address e.g. (address-end)

        :param end: IPv4 address
        :return:
        """

        start: int = IPv4(self.address).decimal()
        end: int = IPv4(end).decimal()

        if not end >= start:
            raise InvalidRangeError(self.address)

        cidr: int = 32
        while (start ^ end) >> (IPv4.MAX_CIDR - cidr):
            cidr -= 1

        return cidr


class Decimal:
    def __init__(self, number: int):
        self.number: int = number

        if not self.valid():
            raise InvalidDecimalError(number)

    def valid(self) -> bool:
        return IPv4.MIN_IP <= self.number <= IPv4.MAX_IP

    def ip(self) -> str:
        """
        Convert decimal representation of IPv4 to plaintext IPv4

        :return:
        """

        octets: list[str] = []
        number: int = self.number

        for c in range(3, -1, -1):
            cidr: int = c << 3
            octet: str = str(number >> cidr & 255)
            octets.append(octet)

        return IPv4.SEP.join(octets)


class Binary:

    def __init__(self, address: list[int]):
        self.address: list[int] = address

        if not self.valid():
            raise InvalidBinaryError(IPv4.SEP.join(map(str, address)))

    def valid(self) -> bool:
        check1: bool = len(self.address) == 4
        all_01 = lambda o: all([c in "01" for c in str(o)])
        length = lambda o: 1 <= len(str(o)) <= 8
        check2: bool = all([all_01(o) and length(o) for o in self.address])

        return all([check1, check2])

    def ip(self) -> str:
        octets: list[str] = []

        for octet in self.address:
            octets.append(str(int(str(octet), 2)))

        return IPv4.SEP.join(octets)


class Bytes:

    def __init__(self, address: bytes):
        self.address: bytes = address

        if not self.valid():
            raise InvalidBytesError(address)

    def valid(self) -> bool:
        check1: bool = len(self.address) == 4
        check2: bool = all([IPv4.MIN_IP <= octet <= IPv4.MAX_IP for octet in self.address])

        return all([check1, check2])

    def unpack(self) -> str:
        return IPv4.SEP.join([o for o in map(str, self.address)])