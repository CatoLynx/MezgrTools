#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# © 2015 Julian Metzler

"""
Script to control a POS display connected via RS232
"""

import argparse
import serial

class POSDisplay(object):
  def __init__(self, port):
    self.port = serial.serial_for_url(port)
  
  def _prepare_text(self, text):
    text = text.replace("ä", chr(132))
    text = text.replace("ö", chr(148))
    text = text.replace("ü", chr(129))
    text = text.replace("Ä", chr(142))
    text = text.replace("Ö", chr(153))
    text = text.replace("Ü", chr(154))
    text = text.replace("ß", chr(225))
    return text
  
  def clear(self):
    self.port.write(chr(12))
    self.port.write(chr(11))
  
  def write_line(self, line, text):
    self.port.write(chr(31)) # Enter command mode
    self.port.write(chr(36)) # Line select
    self.port.write(chr(1))
    self.port.write(chr(line + 1))
    self.port.write(self._prepare_text(text))
  
  def write(self, top = "", bottom = "", top_align = 'center', bottom_align = 'center'):
    if not bottom and len(top) > 20:
      top = top[:40]
    else:
      if top_align == 'center':
        top = top[:20].center(20)
      elif top_align == 'right':
        top = top[:20].rjust(20)
      else:
        top = top[:20].ljust(20)
      
      if bottom_align == 'center':
        bottom = bottom[:20].center(20)
      elif bottom_align == 'right':
        bottom = bottom[:20].rjust(20)
      else:
        bottom = bottom[:20].ljust(20)
    
    self.clear()
    self.port.write(self._prepare_text(top + bottom))

def main():
  parser = argparse.ArgumentParser(description = "POS Display Control")
  parser.add_argument('-p', '--port', type = str, required = True, help = "Serial port")
  parser.add_argument('-t', '--top-text', type = str, default = "", help = "Top line text")
  parser.add_argument('-b', '--bottom-text', type = str, default = "", help = "Bottom line text")
  parser.add_argument('-ta', '--top-align', choices = ('left', 'center', 'right'), default = 'center', help = "Top line alignment (Default: Center)")
  parser.add_argument('-ba', '--bottom-align', choices = ('left', 'center', 'right'), default = 'center', help = "Bottom line alignment (Default: Center)")
  args = parser.parse_args()
  
  display = POSDisplay(args.port)
  display.write(args.top_text, args.bottom_text, args.top_align, args.bottom_align)

if __name__ == "__main__":
  main()