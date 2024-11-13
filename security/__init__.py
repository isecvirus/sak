# security/__init__.py
# written by virus
# v1.1.0

from .password import Password
from .cisco import CiscoPassword
from .otp import OTP

__all__ = [
    "Password",
    "CiscoPassword",
    "OTP",
]