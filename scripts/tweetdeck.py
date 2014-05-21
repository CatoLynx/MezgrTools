#!/usr/bin/env python
# (C) 2014 Julian Metzler

import gtk
import webkit
import gobject

def main():
	gobject.threads_init()
	win = gtk.Window()
	bro = webkit.WebView()
	bro.open("https://tweetdeck.twitter.com/")
	win.add(bro)
	win.show_all()

	gtk.main()

if __name__ == "__main__":
	main()