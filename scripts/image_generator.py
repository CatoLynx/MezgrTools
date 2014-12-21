#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Script by Julian Metzler

"""
Generate images with various patterns
"""

import argparse
import random

from PIL import Image, ImageColor, ImageDraw


def main():
	def _generate_image__maze(image, draw, spacing = 2, retries = 10):
		def __get_pixel(x, y):
			return pixels[y * args.image_width + x]
		
		def __set_pixel(x, y, value = 1):
			pixels[y * args.image_width + x] = value
		
		pixels = [0] * args.image_width * args.image_height
		x_range = (0, args.image_width - 1)
		y_range = (0, args.image_height - 1)
		
		fail_count = 0
		
		while fail_count < retries:
			pos = [random.randint(*x_range), random.randint(*y_range)]
			direction = -1
			
			while True:
				possible_directions = [0, 1, 2, 3]
				
				# Remove the direction we came from as a possibility
				if direction == 0:
					possible_directions.remove(2)
				elif direction == 1:
					possible_directions.remove(3)
				elif direction == 2:
					possible_directions.remove(0)
				elif direction == 3:
					possible_directions.remove(1)
				
				if spacing:
					"""
					We wanna keep a one-pixel wide slot free so it actually looks like a maze.
					Without that, it looks more like a weird map.
					So we check which directions are free two pixels around the current position.
					"""
					
					if 0 in possible_directions and (pos[0] < x_range[0] + spacing or __get_pixel(pos[0] - spacing, pos[1])):
						# Left is obstructed
						possible_directions.remove(0)
					
					if 1 in possible_directions and (pos[1] < y_range[0] + spacing or __get_pixel(pos[0], pos[1] - spacing)):
						# Up is obstructed
						possible_directions.remove(1)
					
					if 2 in possible_directions and (pos[0] > x_range[1] - spacing or __get_pixel(pos[0] + spacing, pos[1])):
						# Right is obstructed
						possible_directions.remove(2)
					
					if 3 in possible_directions and (pos[1] > y_range[1] - spacing or __get_pixel(pos[0], pos[1] + spacing)):
						# Down is obstructed
						possible_directions.remove(3)
					
					if not possible_directions:
						# We're stuck, time to start again somewhere else
						fail_count += 1
						break
				
				direction = random.choice(possible_directions)
				
				if direction == 0: # left
					pos[0] -= 1
					print "Left"
				elif direction == 1: # up
					pos[1] -= 1
					print "Up"
				elif direction == 2: # right
					pos[0] += 1
					print "Right"
				elif direction == 3: # down
					pos[1] += 1
					print "Down"
				
				__set_pixel(*pos)
				
				if not spacing and not (x_range[0] < pos[0] < x_range[1] and y_range[0] < pos[1] < y_range[1]):
					fail_count += 1
					break
			
			print "failed"
		
		fg_color = ImageColor.getrgb(args.foreground_color)
		bg_color = ImageColor.getrgb(args.background_color)
		image.putdata([fg_color if pixel else bg_color for pixel in pixels])
	
	parser = argparse.ArgumentParser(description = "Image generator")
	parser.add_argument('-m', '--mode',
		type = str,
		choices = ('maze', 'map'),
		default = 'maze',
		help = "What kind of image to generate")
	
	parser.add_argument('-of', '--output-file',
		type = str,
		help = "Filename for the generated image (Format is determined by the filename extension). If omitted, the image is shown on screen and not saved.")
	
	parser.add_argument('-iw', '--image-width',
		type = int,
		default = 250,
		help = "Width of the generated image")
	
	parser.add_argument('-ih', '--image-height',
		type = int,
		default = 250,
		help = "Height of the generated image")
	
	parser.add_argument('-bc', '--background-color',
		type = str,
		default = "white",
		help = "The background color of the generated image, in a format compatible to PIL (e.g. 'white' or '#ff0080')")
	
	parser.add_argument('-fc', '--foreground-color',
		type = str,
		default = "black",
		help = "The foreground color of the generated image")
	
	args = parser.parse_args()
	
	image = Image.new("RGB", (args.image_width, args.image_height), args.background_color)
	draw = ImageDraw.Draw(image)
	
	if args.mode == 'maze':
		_generate_image__maze(image, draw, spacing = 20)
	elif args.mode == 'map':
		_generate_image__maze(image, draw, spacing = 0)
	
	if args.output_file:
		image.save(args.output_file)
	else:
		image.show()

if __name__ == "__main__":
	main()