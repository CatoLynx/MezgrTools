#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# © 2015 Julian Metzler

"""
POS Display clock
"""

import pos_display
import sys
import time

def main():
    display = pos_display.POSDisplay(sys.argv[1])

    while True:
        display.write(time.strftime("%H:%M:%S"), time.strftime("%A %d %b %Y"), 'center', 'center')
        time.sleep(1)

if __name__ == "__main__":
    main()