# password (v1.4.0)

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


class InvalidGroup(Exception):
    def __init__(self, group):
        super().__init__(f"Character group {group!r} is not valid")

class UnselectedGroup(Exception):
    def __init__(self, group):
        super().__init__(f"Character group {group!r} is not selected")


class InvalidCharacterError(Exception):
    def __init__(self, char):
        super().__init__(f"Character {char!r} does not fit into any group")


class InvalidPattern(Exception):
    def __init__(self, pattern):
        super().__init__(f"The password pattern {pattern!r} is not valid")

class InvalidPasswordLength(Exception):
    def __init__(self, length):
        super().__init__(f"Invalid password length {str(length)!r}")



class Password:
    """
    L: Lower
    U: Upper
    A: Alpha
    D: Digit
    O: Octet
    H: Hex
    P: Punctuations
    W: Whitespace
    R: Readable
    """

    CHARACTER_GROUPS = {
        'L': "abcdefghijklmnopqrstuvwxyz",
        'U': "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        'D': "0123456789",
        'A': "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
        'R': "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
        'O': "01234567",
        'H': "0123456789abcdefABCDEF",
        'P': r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~""",
        'W': "\t\n\v\f\r ",
    }

    SELECTED_GROUPS = {}

    def __init__(self):
        self.set()

    def set(self, chars: dict | list | str = None):
        self.SELECTED_GROUPS = self.parse(chars if chars else ['R'])



    def get(self, length: int, pattern:str=None) -> str:
        if not isinstance(length, int) or not length >= 1:
            raise InvalidPasswordLength(length)

        if pattern:
            return self.patterned_password(length=length, pattern=pattern)
        else:
            return ''.join([random.choice(''.join(self.SELECTED_GROUPS.values())) for _ in range(length)])

    def patterned_password(self, length: int, pattern:str):
        if len(pattern) > length or not pattern:
            raise InvalidPattern(pattern)

        password = ''
        pattern = (pattern * ((length // len(pattern)) + 1))[:length]

        for group in pattern:
            if group in self.CHARACTER_GROUPS:
                if not self.SELECTED_GROUPS.get(group):
                    raise UnselectedGroup(group)
                password += random.choice(self.SELECTED_GROUPS[group])
            else:
                raise InvalidPattern(pattern)
        return password

    def parse(self, chars: dict | list | str) -> dict:
        selected_groups = {}

        if isinstance(chars, list):
            try:
                selected_groups = {group: self.CHARACTER_GROUPS[group] for group in chars}
            except KeyError as error:
                raise InvalidGroup(error.args[0])
        elif isinstance(chars, dict):
            for group in chars.keys():
                if not group in self.CHARACTER_GROUPS.keys():
                    raise InvalidGroup(group)
                elif not chars[group]:
                    chars[group] = self.CHARACTER_GROUPS[group]
            selected_groups = chars
        elif isinstance(chars, str):
            for char in chars:
                categorized = False
                for (group, sequence) in self.CHARACTER_GROUPS.items():
                    if char in sequence:
                        selected_groups.setdefault(group, char)
                        if self.valid_group(group) and char not in selected_groups.get(group):
                            selected_groups[group] += char
                        categorized = True
                        break

                if not categorized:
                    raise InvalidCharacterError(char)

        return selected_groups

    def valid_group(self, group):
        return group in self.CHARACTER_GROUPS


password = Password()
password.set({
    'P': None,
    'L': None,
})
print(password.get(8, pattern="LP"))
