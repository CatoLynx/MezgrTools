#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2013 Julian Metzler
# See the LICENSE file for the full license.

"""
This script generates a panel indicator that can display text (e.g. the output of a command) periodically
"""

import appindicator
import argparse
import base64
import gobject
import gtk
import paramiko
import time

from subprocess import check_output

class Indicator:
	def __init__(self, args):
		self.args = args
		self.indicator = appindicator.Indicator("Mezgrman's generic text applet", icon_name = self.args.icon, category = appindicator.CATEGORY_APPLICATION_STATUS)
		self.indicator.set_status(appindicator.STATUS_ACTIVE)
		self.menu = gtk.Menu()
		self.add_menu_item("Quit", 'QUIT', gtk.STOCK_QUIT)
		self.menu.show_all()
		self.indicator.set_menu(self.menu)
		if self.args.remote_host:
			self.ssh_connect()
		self.update()
	
	def quit(self):
		try:
			self.ssh.close()
		except:
			pass
		gtk.main_quit()
	
	def add_menu_item(self, label, command, image = None):
		item = gtk.ImageMenuItem(label)
		if image is not None:
			img = gtk.image_new_from_stock(image, gtk.ICON_SIZE_MENU)
			item.set_image(img)
		item.connect('activate', self.handle_menu_item, command)
		self.menu.append(item)
	
	def handle_menu_item(self, widget = None, command = None):
		if command == 'QUIT':
			self.quit()
	
	def ssh_connect(self):
		self.ssh = paramiko.SSHClient()
		self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		self.ssh.connect(self.args.remote_host, username = self.args.remote_user, port = self.args.remote_port, timeout = self.args.interval or 5.0)
	
	def update(self, text = None):
		if text is None:
			text = self.generate_text()
		self.indicator.set_label(text)
		return True
	
	def generate_text(self):
		if self.args.mode == 'static':
			return self.args.text or "<placeholder>"
		elif self.args.mode == 'command':
			if self.args.remote_host:
				try:
					ssh_stdin, ssh_stdout, ssh_stderr = self.ssh.exec_command(self.args.command)
				except paramiko.SSHException:
					try:
						self.ssh.close()
					except:
						pass
					self.ssh_connect()
				return "\n".join(ssh_stdout).strip("\n")
			else:
				return check_output(self.args.command, shell = True).strip("\n")
		return "<placeholder>"

def main():
	parser = argparse.ArgumentParser(description = "Generic text applet")
	parser.add_argument('-i', '--icon', default = "none", help = "The icon file to use for the indicator")
	parser.add_argument('-m', '--mode', choices = ('static', 'command'), default = "static", help = "The operation mode")
	parser.add_argument('-t', '--text', help = "The static text to display")
	parser.add_argument('-c', '--command', default = "echo '<placeholder>'", help = "The command to execute")
	parser.add_argument('-rh', '--remote-host', help = "The remote host to run the command on via SSH (requires publickey auth)")
	parser.add_argument('-ru', '--remote-user', help = "The remote SSH username")
	parser.add_argument('-rp', '--remote-port', type = int, help = "The remote SSH port")
	parser.add_argument('-iv', '--interval', type = float, help = "The refresh interval in seconds (if omitted, it won't refresh)")
	args = parser.parse_args()
	
	indicator = Indicator(args)
	if args.interval:
		gobject.timeout_add(int(args.interval * 1000), indicator.update)
	try:
		gtk.main()
	except:
		try:
			indicator.quit()
		except:
			pass

if __name__ == "__main__":
	main()