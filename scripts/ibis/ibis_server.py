#!/usr/bin/env python
# -*- coding: utf-8 -*-
# © 2014 Julian Metzler

"""
IBIS controller and server for 4 displays
"""

import argparse
import ibis
import json
import socket
import thread
import time

class Listener(object):
	def __init__(self, controller, port = 4245):
		self.controller = controller
		self.port = port
		self.running = False
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	def reply(self, connection, data):
		connection.sendall(json.dumps(data))
	
	def run(self):
		self.running = True
		self.socket.bind(('', self.port))
		print "Listening on port %i" % self.port
		self.socket.listen(1)
		try:
			while self.running:
				try:
					conn, addr = self.socket.accept()
					print "Accepted connection from %s on port %i" % addr
					data = conn.recv(4096)
					message = json.loads(data)
					success = True
					if 'enable' in message.keys():
						if message['enable'] == 'toggle':
							try:
								self.controller.set_enabled(not self.controller.enabled)
							except:
								success = False
						else:
							try:
								self.controller.set_enabled(bool(message['enable']))
							except:
								success = False
						self.reply(conn, {'success': success})
					elif 'query' in message.keys():
						if message['query'] == 'current':
							self.reply(conn, self.controller.current_text)
						elif message['query'] == 'buffer':
							self.reply(conn, self.controller.buffer)
						elif message['query'] == 'enabled':
							self.reply(conn, self.controller.enabled)
					else:
						try:
							self.controller.set_message(message['address'], message['message'])
						except:
							success = False
						self.reply(conn, {'success': success})
				except KeyboardInterrupt:
					self.quit()
		finally:
			self.socket.close()
	
	def quit(self):
		self.running = False

class Controller(object):
	DEBUG = False
	VERBOSE = True
	TIMEOUT = 120.0
	
	def __init__(self, master):
		self.master = master
		self.running = False
		self.enabled = True
		self.buffer = {
			0: {
				'message': None,
				'current': 0,
				'last_refresh': 0.0,
				'last_update': 0.0
			},
			1: {
				'message': None,
				'current': 0,
				'last_refresh': 0.0,
				'last_update': 0.0
			},
			2: {
				'message': None,
				'current': 0,
				'last_refresh': 0.0,
				'last_update': 0.0
			},
			3: {
				'message': None,
				'current': 0,
				'last_refresh': 0.0,
				'last_update': 0.0
			}
		}
		self.current_text = {
			0: None,
			1: None,
			2: None,
			3: None
		}
	
	def set_enabled(self, value):
		"""
		Enable or disable the displays
		"""
		
		self.enabled = value
		
		if not self.enabled:
			self.send_text(-1, None)
		
		if self.VERBOSE:
			print "Power state changed to %s" % str(value)
	
	def send_text(self, address, text):
		"""
		Send text to a display
		"""
		
		# Set the address on the multiplexer or send to all displays if address is -1
		if address == -1:
			for i in range(4):
				self.send_text(i, text)
			return
		elif address == 0:
			self.master.device.setDTR(0)
			self.master.device.setRTS(0)
		elif address == 1:
			self.master.device.setDTR(0)
			self.master.device.setRTS(1)
		elif address == 2:
			self.master.device.setDTR(1)
			self.master.device.setRTS(0)
		elif address == 3:
			self.master.device.setDTR(1)
			self.master.device.setRTS(1)
		
		# Send the data
		self.master.send_next_stop__003c("" if text is None else text)
		if self.DEBUG:
			print address, text
		
		# Save the current text
		self.current_text[address] = text if text else None
	
	def set_message(self, address, message):
		"""
		Set the stuff to be displayed on a display, like a sequence of texts
		
		Message Examples
		
			Simple text
				{
					'type': 'text',
					'text': "Hello world"
				}
			
			Formatted time
				{
					'type': 'time',
					'format': "%d.%m.%Y %H:%M"
				}
			
			Two alternating texts with the same interval
				{
					'type': 'sequence',
					'messages': [
						{
							'type': 'time',
							'format': "%d.%m.%Y %H:%M"
						},
						{
							'type': 'text',
							'text': "SE50 Frankfurt"
						}
					],
					'interval': 5.0
				}
			
			Two alternating texts with different intervals
				{
					'type': 'sequence',
					'messages': [
						{
							'type': 'text',
							'text': "Next Stop",
							'duration': 2.0
						},
						{
							'type': 'text',
							'text': "Frankfurt",
							'duration': 5.0
						}
					],
					'interval': 5.0
				}
		
		Note: The 'interval' property of sequences is used for all messages that don't specify a duration of their own.
		"""
		
		self.buffer[address]['message'] = message
		
		if self.VERBOSE:
			print "Set message on display %i: %s" % (address, str(message))
	
	def send_message(self, address, message):
		"""
		Send a single message of various types
		"""
		
		now = time.time()
		current_text = self.current_text[address]
		last_refresh = self.buffer[address]['last_refresh']
		last_update = self.buffer[address]['last_update']
		
		if message:
			if message['type'] == 'text':
				if current_text != message['text']:
					self.send_text(address, message['text'])
					self.buffer[address]['last_refresh'] = now
					self.buffer[address]['last_update'] = now
				elif last_refresh + self.TIMEOUT <= now:
					self.send_text(address, current_text)
					self.buffer[address]['last_refresh'] = now
			elif message['type'] == 'time':
				try:
					text = time.strftime(message['format'])
				except:
					text = time.strftime(message['format'].encode('utf-8'))
				if current_text != text:
					self.send_text(address, text)
					self.buffer[address]['last_refresh'] = now
					self.buffer[address]['last_update'] = now
				elif last_refresh + self.TIMEOUT <= now:
					self.send_text(address, current_text)
					self.buffer[address]['last_refresh'] = now
			elif message['type'] == 'sequence':
				default_interval = message['interval']
				messages = message['messages']
				current = self.buffer[address]['current']
				if current >= len(messages) - 1:
					next_message = 0
				else:
					next_message = current + 1
				duration = messages[current].get('duration', None)
				if duration is None:
					duration = default_interval
				if last_update + duration <= now:
					self.buffer[address]['current'] = next_message
					self.send_message(address, messages[next_message])
				elif last_refresh + self.TIMEOUT <= now:
					self.send_text(address, current_text)
					self.buffer[address]['last_refresh'] = now
		else:
			if current_text is not None:
				self.send_text(address, None)
				self.buffer[address]['last_update'] = now
	
	def selftest(self):
		self.send_text(-1, None)
		time.sleep(2)
		self.send_text(-1, "IBIS Server")
		time.sleep(2)
		self.send_text(-1, "by Mezgrman")
		time.sleep(2)
		self.send_text(-1, "www.mezgrman.de")
		time.sleep(2)
		for i in range(4):
			self.send_text(i, "Display %i" % i)
		time.sleep(5)
		"""self.send_text(-1, "0" * 16)
		time.sleep(1)
		self.send_text(-1, "1" * 16)
		time.sleep(1)
		self.send_text(-1, "2" * 16)
		time.sleep(1)
		self.send_text(-1, "3" * 16)
		time.sleep(1)
		self.send_text(-1, "4" * 16)
		time.sleep(1)
		self.send_text(-1, "5" * 16)
		time.sleep(1)
		self.send_text(-1, "6" * 16)
		time.sleep(1)
		self.send_text(-1, "7" * 16)
		time.sleep(1)
		self.send_text(-1, "8" * 16)
		time.sleep(1)
		self.send_text(-1, "9" * 16)
		time.sleep(1)"""
		self.send_text(-1, None)
	
	def process_buffer(self):
		"""
		Periodically check what's in the buffer and update the displays if necessary
		"""
		
		while self.running:
			if self.enabled:
				for address in range(4):
					data = self.buffer[address]
					message = data['message']
					self.send_message(address, message)
			time.sleep(0.1)
	
	def run(self):
		self.running = True
		self.process_buffer()
	
	def quit(self):
		self.running = False

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-v', '--verbose', action = 'store_true')
	parser.add_argument('-d', '--debug', action = 'store_true')
	parser.add_argument('-s', '--selftest', action = 'store_true')
	parser.add_argument('-t', '--timeout', type = int, default = 120)
	parser.add_argument('-sp', '--serial-port', type = str, default = "/dev/ttyUSB0")
	parser.add_argument('-p', '--port', type = int, default = 4242)
	args = parser.parse_args()
	
	master = ibis.IBISMaster(args.serial_port)
	controller = Controller(master)
	controller.TIMEOUT = args.timeout
	controller.VERBOSE = args.verbose
	controller.DEBUG = args.debug
	if args.selftest:
		controller.selftest()
		
	thread.start_new_thread(controller.run, ())
	listener = Listener(controller, port = args.port)
	listener.run()

if __name__ == "__main__":
	main()