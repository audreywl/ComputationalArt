""" Generates a 350x350 pixel png format art, defined recursively with a random selection of product, average, cos, sin, square, and square root functions."""

import random, math
from PIL import Image
import pygame
from pygame.locals import QUIT
import alsaaudio
import audioop
import time

def build_random_function(min_depth, max_depth):
	""" Builds a random function of depth at least min_depth and depth
		at most max_depth (see assignment writeup for definition of depth
		in this context)

		min_depth: the minimum depth of the random function
		max_depth: the maximum depth of the random function
		returns: the randomly generated function represented as a nested list
				 (see assignment writeup for details on the representation of
				 these functions)
	"""
	if max_depth < 1:
		return random.choice([lambda x,y,t: x, lambda x,y,t: y, lambda x,y,t: t])
	elif min_depth < 1:
		if random.randint(0,1):
			return random.choice([lambda x,y,t: x, lambda x,y,t: y, lambda x,y,t: t])

	new_min_depth= min_depth-1
	new_max_depth = max_depth-1

	next_function_1 = build_random_function(new_min_depth, new_max_depth)
	next_function_2 = build_random_function(new_min_depth, new_max_depth)

	functions = [lambda x,y,t: next_function_1(x,y,t)*next_function_2(x,y,t), #product
	lambda x,y,t: .5*next_function_1(x,y,t)*next_function_2(x,y,t), #average
	lambda x,y,t: math.cos(2* math.pi * next_function_1(x,y,t)), #sine pi
	lambda x,y,t: math.sin(2* math.pi * next_function_1(x,y,t)), #cosine pi
	lambda x,y,t: next_function_1(x,y,t)*next_function_1(x,y,t), #square
	lambda x,y,t: math.sqrt(abs(next_function_1(x,y,t)))] #square root

	
	return random.choice(functions)
		

def remap_interval(val,
				   input_interval_start,
				   input_interval_end,
				   output_interval_start,
				   output_interval_end):
	""" Given an input value in the interval [input_interval_start,
		input_interval_end], return an output value scaled to fall within
		the output interval [output_interval_start, output_interval_end].

		val: the value to remap
		input_interval_start: the start of the interval that contains all
							  possible values for val
		input_interval_end: the end of the interval that contains all possible
							values for val
		output_interval_start: the start of the interval that contains all
							   possible output values
		output_inteval_end: the end of the interval that contains all possible
							output values
		returns: the value remapped from the input to the output interval

		>>> remap_interval(0.5, 0, 1, 0, 10)
		5.0
		>>> remap_interval(5, 4, 6, 0, 2)
		1.0
		>>> remap_interval(5, 4, 6, 1, 2)
		1.5
	"""
	val=float(val)
	input_length=(input_interval_end - input_interval_start)
	val_ratio=(val- input_interval_start)/input_length
	output_length=(output_interval_end - output_interval_start)
	new_val = val_ratio*output_length + output_interval_start
	return new_val
	


def color_map(val):
	""" Maps input value between -1 and 1 to an integer 0-255, suitable for
		use as an RGB color code.

		val: value to remap, must be a float in the interval [-1, 1]
		returns: integer in the interval [0,255]

		>>> color_map(-1.0)
		0
		>>> color_map(1.0)
		255
		>>> color_map(0.0)
		127
		>>> color_map(0.5)
		191
	"""
	# NOTE: This relies on remap_interval, which you must provide
	color_code = remap_interval(val, -1, 1, 0, 255)
	return int(color_code)


def test_image(filename, x_size=350, y_size=350):
	""" Generate test image with random pixels and save as an image file.

		filename: string filename for image (should be .png)
		x_size, y_size: optional args to set image dimensions (default: 350)
	"""
	# Create image and loop over all pixels
	im = Image.new("RGB", (x_size, y_size))
	pixels = im.load()
	for i in range(x_size):
		for j in range(y_size):
			x = remap_interval(i, 0, x_size, -1, 1)
			y = remap_interval(j, 0, y_size, -1, 1)
			pixels[i, j] = (random.randint(0, 255),  # Red channel
							random.randint(0, 255),  # Green channel
							random.randint(0, 255))  # Blue channel

	im.save(filename)


def generate_movie(filename, x_size=350, y_size=350, movie_frames=50):
	""" Generate computational art and save as an image file.

		filename: string filename for image (should be .png)
		x_size, y_size: optional args to set image dimensions (default: 350)
	"""
	# Functions for red, green, and blue channels - where the magic happens!
	red_function = build_random_function(6,9)
	green_function = build_random_function(6,9)
	blue_function = build_random_function(6,9)
	# Create image and loop over all pixels
	im = Image.new("RGB", (x_size, y_size))
	pixels = im.load()
	for time in range(movie_frames):
		frame_name = filename + str(time) + '.png'
		t = remap_interval(time, 0, movie_frames, -1, 1)
		for i in range(x_size):
			for j in range(y_size):
				x = remap_interval(i, 0, x_size, -1, 1)
				y = remap_interval(j, 0, y_size, -1, 1)
				pixels[i, j] = (
						color_map(red_function(x,y,t)),
						color_map(green_function(x,y,t)),
						color_map(blue_function(x,y,t))
						)

		im.save(frame_name)

def generate_art(filename, x_size=350, y_size=350):
	""" Generate computational art and save as an image file.

		filename: string filename for image (should be .png)
		x_size, y_size: optional args to set image dimensions (default: 350)
	"""
	# Functions for red, green, and blue channels - where the magic happens!
	red_function = build_random_function(6,9)
	green_function = build_random_function(6,9)
	blue_function = build_random_function(6,9)
	# Create image and loop over all pixels
	im = Image.new("RGB", (x_size, y_size))
	pixels = im.load()
	t=1
	for i in range(x_size):
		for j in range(y_size):
			x = remap_interval(i, 0, x_size, -1, 1)
			y = remap_interval(j, 0, y_size, -1, 1)
			pixels[i, j] = (
					color_map(red_function(x,y,t)),
					color_map(green_function(x,y,t)),
					color_map(blue_function(x,y,t))
					)
	im.save(filename)

def music_visualizer(file_extension, volume_precision, x_size=350, y_size=350):
	"""creates music visualizer using pygame, pyalsa, and functions from recursive art."""
	#audio setup
	inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE,0)
	inp.setchannels(1)
	inp.setrate(16000)
	inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
	inp.setperiodsize(160)
	#generate frames - uncomment to generate a whole new set of images to pull from
	#generate_movie(file_extension, x_size, y_size, volume_precision)
	#pygame load list of screens to choose from
	surface_list = []
	for i in range(volume_precision):
		filename=file_extension+str(i)+'.png'
		current_image = pygame.image.load(filename)
		surface_list.append(current_image)
	#start visualizer
	pygame.init()
	size=(x_size, y_size)
	screen= pygame.display.set_mode(size)
	running= True
	while running:
		for event in pygame.event.get():
			if event.type== QUIT:
				running= False
		l,data = inp.read()
		if l:
			   loudness = audioop.rms(data,2)
		
		frame = int(remap_interval(loudness, 500, 5000, 1, volume_precision))
		try:
			current_surface = surface_list[frame]
		except IndexError:
			current_surface = surface_list[49]
		screen.blit(current_surface, (0,0))
		pygame.display.update()
		time.sleep(.001)
if __name__ == '__main__':
	import doctest
	#generate_art("myart18.png")
	music_visualizer('frame', 50)