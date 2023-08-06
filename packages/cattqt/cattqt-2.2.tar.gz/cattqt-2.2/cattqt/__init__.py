"""A control GUI for Chromecasts"""

# -*- coding: utf-8 -*-

import sys
from cattqt import cattqt

if sys.version_info.major < 3:
    print("This program requires Python 3 and above to run.")
    sys.exit(1)


__author__ = "Scott Moreau"
__email__ = "oreaus@gmail.com"
__version__ = "2.2"


def main() -> None:
    cattqt.main(__version__)
