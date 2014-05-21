#!/usr/bin/env python
# (C) 2014 Julian Metzler

import gtk
import webkit
import gobject
import subprocess

def open_link(view, frame, request, action, decision):
	# WHY THE FUCK ISN'T THIS WORKING
	uri = request.get_uri()
	if not uri.startswith("https://tweetdeck.twitter.com"):
		decision.ignore() # Tell WebKit to not give a fuck about the link, we handle this shit
		subprocess.call(["xdg-open", uri]) # HANDLE IT MOTHERFUCKER
	
	return False

def main():
	gobject.threads_init()
	win = gtk.Window()
	bro = webkit.WebView()
	bro.connect("navigation-policy-decision-requested", open_link)
	bro.open("https://tweetdeck.twitter.com/")
	win.add(bro)
	win.show_all()

	gtk.main()

if __name__ == "__main__":
	main()