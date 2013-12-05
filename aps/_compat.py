# -*- coding: utf-8 -*-
import sys

if sys.version_info[0] == 2:
    # py2
    str_types = [unicode]
    bytes_types = [str]
else:
    # py3
    str_types = [str]
    bytes_types = [bytes]
