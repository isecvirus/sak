# mask/email.py (v1.0.0)

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
from privacy.mask import Rule


def parts(email:str):
    username, domain_tld = email.split('@')
    *domain, tld = domain_tld.split('.', -1)

    return [username, '.'.join(domain), tld]


class Email(Rule):
    REGEX = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"

    def __init__(self, wildcard:str='*', limit: int = None, placeholder:str=None, level: list[bool, bool, bool] = [True, True, True], anonymize: bool = False):
        super().__init__(wildcard=wildcard, limit=limit, placeholder=placeholder)

        self.level = level + [True] * (3 - len(level))
        self.anonymize = anonymize

    def apply(self, string: str) -> str:
        emails = reversed(list(re.finditer(self.REGEX, string))[:self.limit])

        if self.placeholder:
            for match in emails:
                start, end = match.span()

                string = string[:start] + self.placeholder + string[end:]
        else:
            for match in emails:
                start, end = match.span()
                email = string[start:end]
                email_parts = parts(email)

                for (index, should_mask), part in zip(enumerate(self.level), email_parts):
                    if should_mask:
                        email_parts[index] = (self.wildcard * 3) if self.anonymize else (self.wildcard * len(part))

                final_email = f"{email_parts[0]}@{email_parts[1]}.{email_parts[2]}"

                string = string[:start] + final_email + string[end:]

        return string