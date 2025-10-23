"""
Git License Scanner - 授權檢測工具
"""

__version__ = "0.5.0"
__author__ = "YOU-RONG, ZHENG"

from .scanner import LicenseScanner
from .licenses_db import LicenseDatabase

__all__ = ['LicenseScanner', 'LicenseDatabase']