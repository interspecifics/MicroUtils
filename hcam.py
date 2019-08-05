#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
handicam>> 
touchscreen camera controller
for speculative communications microscope
emmanuel@interspecifics.cc
http://interspecifics.cc/work/speculative-communications-2017/

v1.0 190306
requires picamera, pillow, pygame
display a permanent preview with overlay
detect buttons with pygame
two modes: timelapses and video
dedicated folder
requires backgrounds bg,bga.png
"""

from picamera import PiCamera
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import threading, sys, time, datetime
import subprocess, types, os
import pygame

def cam_start_callback(addr, tags, args, source):
	global run, state
	if args[0]==1:
		state = 1
		run = True
		print "[hCam]: --->]"

def cam_stop_callback(path, tags, args, source):
	global run, state
	if args[0]==1:
		state = 0
		run = False
		print "[hCam]: ---x]"

def getnow():
	#- return date_time string
	ta = datetime.date.today().isoformat().replace("-","")
	tb = time.asctime()[11:16].replace(":","")
	return ta+"_"+tb

def load_image(filename, transparent=False):
    try: image = pygame.image.load(filename)
    except pygame.error, message:
            raise SystemExit, message
    image = image.convert()
    if transparent:
            color = image.get_at((0,0))
            image.set_colorkey(color, RLEACCEL)
    return image

def main():
	#- init camera
	cam = PiCamera()
	cam.resolution = (2592, 1944)
	cam.framerate = 30
	print "[_hCam_]"
	#- other inits
	dir_tl = "/home/pi/CE/timelapses/"
	dir_vv = "/home/pi/CE/videos/"
	if not os.path.exists(dir_vv):
		os.makedirs(dir_vv)
		print "[hCam] : created video dir " + dir_vv
	if not os.path.exists(dir_tl):
		os.makedirs(dir_tl)
		print "[hCam] : created timelapse dir " + dir_tl
	act_dir = ""
	state = 0
	npics = 480
	cc = 0
	t0 = 0
	t1 = 0
	#- pygame inits
	size = w, h = 480, 320
	pygame.init()
	screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
	pygame.display.set_caption("[spec_coms]")
	pygame.mouse.set_visible(1)
	bg_img = load_image('./bg.png')
	bga_img = load_image('./bga.png')
	running = True
	#- cam inits
	cam.start_preview();
	#- then be sure to loop
	while running:
		if state==0:			# st0 is preview 
			screen.blit(bg_img, (0,0))
			pygame.display.flip()
		if state==1:			#st1 is ttimelapse
			screen.blit(bga_img, (0,0))
			pygame.display.flip()
			t1 = time.time()
			if t1 - t0 > 10:
				cam.capture(act_dir+'/i_%05d.jpg'%cc)
				t0 = time.time()
				cc+=1
				print cc,"-",
		if state==2: 			#st2 is video capture
			screen.blit(bga_img, (0,0))
			pygame.display.flip()
			cam.wait_recording(30, splitter_port=2)
		#- the logic is on the events
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:
				clickon = pygame.mouse.get_pos()
				print "click on", clickon
				if state==0:
					if clickon[0]<40:
						# init timelapse
						now = getnow()
						act_dir = dir_tl + now
						if not os.path.exists(act_dir):
							os.makedirs(act_dir)
						print "[hCam] : timelapse.start " + act_dir+'/'
						cc = 0
						t0 = time.time()
						state = 1
					if clickon[0]>440:
						# init recording
						now = getnow()
						nvid = dir_vv+'v_'+now+'.h264'
						cam.start_recording(nvid, splitter_port=2, resize=(1920, 1080))
						print "[hCam] : videorecord.start " + nvid
						state = 2
				elif state==1 or state == 2:
					if clickon[0]<40 or clickon[0]>440:
						if state==1:
							print "[hcam]: tl.stop " + act_dir+'/'
						elif state==2:
							cam.stop_recording(splitter_port=2)
							print "[hcam]: vv.stop " + nvid
						state = 0
			if event.type == pygame.KEYDOWN and event.key==K_SPACE:
				running = false
				cam.stop_preview()
			if event.type == pygame.QUIT: 
				running = false
				cam.stop_preview()
				#sys.exit()
	# end of the while
	ta = datetime.date.today().isoformat().replace("-","")
	tb = time.asctime()[11:16].replace(":","")
	Now = ta+"_"+tb
	return 0

#--- ##
if __name__ == "__main__":
	main()
