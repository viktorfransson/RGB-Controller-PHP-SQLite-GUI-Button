#!/usr/bin/python
# PHP
# Python
# SQLite

import RPi.GPIO as GPIO
import pigpio
pi = pigpio.pi()

import subprocess
import os
import sys
import datetime
import time
import random
import numpy 
import mechanize
import sqlite3 as lite
from thread import start_new_thread


# PHP
# Port 8080
def phpServer():
	temp = "php -S 0.0.0.0:8080 -t php"
	print temp
	subprocess.call(temp,shell=True)
start_new_thread(phpServer,())

# Pins
RED_PIN	= 27
GREEN_PIN = 17
BLUE_PIN = 22
BUTTON_PIN = 20
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Steps
STEPS	= 5

# Delays
DELAY1  = 0.3
DELAY_INF = float('Inf')
DELAY_RAND = 3
DELAY_RAINBOW = 0.1
DELAY_ALLCOLORS = 0.1
LIGHTS_OUT = 60 * 30 # seconds
LOG_TIME = 120
PARAMETER = 10

# Color variables
r,b,g = 255,0,0
r_old,g_old,b_old = r,g,b
r_all,g_all,b_all = r,g,b
set_r,set_g,set_b = r,g,b

# Time variables
timestamp = time.time(); timeon = 0

# Mode variables
mode = 0; mode_old = 0

# Brightness variables
bright_adjust = 0; bright_adjust_old = 0; bright_adjust_set_old = 0; adjust = 0; change = 1

# Etc variables
rand_switch = 0
parts = 40.0
counter = 0

# Log file (for last LOG_TIME seconds)
def clearLog():
	while 1:
		log_file = open(os.path.join(os.getcwd(),"spa.log"),"w")
		sys.stdout = log_file
		with open(os.path.join(os.getcwd(),"spa.log"), 'w'):
			pass
		time.sleep(LOG_TIME)
start_new_thread(clearLog,())

# Update color function
def updateColor(color, step):
	color += step
	if color > 255:
		return 255
	if color < 0:
		return 0
	return color

# Set lights and brightness function
def setLights():
	global r, g, b, mode, bright_adjust, timeon, bright_adjust_set_old
	rgb = 	numpy.array([r,g,b]) * bright_adjust / 100
	pi.set_PWM_dutycycle(RED_PIN, rgb[0])
	pi.set_PWM_dutycycle(GREEN_PIN, rgb[1])
	pi.set_PWM_dutycycle(BLUE_PIN, rgb[2])
	
	# Log if brightness is not 0 (off)
	if (bright_adjust_set_old != 0):
		m, s = divmod(LIGHTS_OUT - timeon, 60)
		h, m = divmod(m, 60)
		print "Time:",datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'),"Mode:",mode,"Brightness:",bright_adjust,"   R:", rgb[0],"   \tG:",rgb[1],"   \tB:",rgb[2],"\tOff in: ", "%d:%02d:%02d" % (h, m, s)
		sys.stdout.flush()
	bright_adjust_set_old = bright_adjust

# Turn lights off after a time period (LIGHTS_OUT)
def checkSleep():
	global timestamp, LIGHTS_OUT, timestamp, timeon
	while 1:
		timeon = time.time() - timestamp
		if (timeon > LIGHTS_OUT):
			db = lite.connect(os.path.join(os.getcwd(),"db/data.sqlite"))
			cur = db.cursor()
			cur.execute ("UPDATE data SET brightness=? WHERE id=?", (0, 0))
			db.commit()
			db.close()
		time.sleep(DELAY1)
start_new_thread(checkSleep,())

# Check mode thread
def checkMode():
	global mode, bright_adjust, timestamp, set_r, set_g, set_b, PARAMETER,BUTTON_PIN, bright_adjust, mode
	modified_old = os.stat("spa.py").st_mtime 
	bright_adjust_old = 0
	while True:
		db = lite.connect(os.path.join(os.getcwd(),"db/data.sqlite"))
		cur = db.cursor()
		cur.execute("select * from data where id=0")
		for sql in cur.fetchall():
			mode = sql[1]
			bright_adjust = sql[2]
			set_r = sql[3]
			set_g = sql[4]
			set_b = sql[5]
			PARAMETER = sql[6]
		db.commit()
		db.close()
		if bright_adjust_old != bright_adjust:
			timestamp = time.time()
		bright_adjust_old = bright_adjust

		# Check for change and restart script if changes are found
		modified = os.stat("spa.py").st_mtime 
		if (modified != modified_old):
			subprocess.call("sudo supervisorctl restart spa", shell=True)
		modified_old = modified
		time.sleep(DELAY1) 
start_new_thread(checkMode, ())   

def checkButton():
	global BUTTON_PIN, bright_adjust, mode
	while 1:
		input_state = GPIO.input(BUTTON_PIN)
		if input_state == 0:
			db = lite.connect(os.path.join(os.getcwd(),"db/data.sqlite"))
			cur = db.cursor()
			mode_temp = mode
			if bright_adjust == 0:
				cur.execute ("UPDATE data SET brightness=? WHERE id=?", (100, 0))
				db.commit()
				db.close()
			else:
				cur.execute ("UPDATE data SET mode=? WHERE id=?", ((mode_temp+1)%11, 0))
				db.commit()
				db.close()
			while (input_state == 0):
				input_state = GPIO.input(BUTTON_PIN)
				print "Button Pressed"
				sys.stdout.flush()
				time.sleep(DELAY1)
		print "Button Released"
		sys.stdout.flush()
		time.sleep(DELAY1)
#start_new_thread(checkButton,())

# Delay time different depending on mode and changes of mode/brightness
def delayMain(m,t,ba,pa):
	global mode
	global bright_adjust
	global PARAMETER
	start = time.time()
	a = 0
	while (mode==m and a<t and ba==bright_adjust and pa == PARAMETER):
		a = time.time()-start
		if mode==7:
			if r!=set_r or g!=set_g or b!=set_b:
				break
		time.sleep(0.01)
		
# Main loop
time.sleep(2)
while 1:
	# Red
	if mode == 0:
		delay = DELAY_INF
		r = 255; g = 0; b = 0
		
	# Green
	if mode == 1:
		delay = DELAY_INF
		r = 0; g = 255; b = 0

	# Blue
	if mode == 2:
		delay = DELAY_INF
		r = 0; g = 0; b = 255
		
	# Cyan
	if mode == 3:
		delay = DELAY_INF
		r = 0; g = 255; b = 255

	# Magenta
	if mode == 4:
		delay = DELAY_INF
		r = 255; g = 0; b = 255

	# Yellow
	if mode == 5:
		delay = DELAY_INF
		r = 255; g = 255; b = 0
	
	# White
	if mode == 6:
		delay = DELAY_INF
		r = 255; g = 255; b = 255

	# Fix
	if mode == 7:
		delay = DELAY_INF
		r = set_r; g = set_g; b = set_b
		
	# Rainbow
	if mode == 8:
		delay = DELAY_RAINBOW
		
		if r == 255 and b == 0 and g < 255:
			g = updateColor(g, STEPS)

		elif g == 255 and b == 0 and r > 0:
			r = updateColor(r, -STEPS)

		elif r == 0 and g == 255 and b < 255:
			b = updateColor(b, STEPS)

		elif r == 0 and b == 255 and g > 0:
			g = updateColor(g, -STEPS)

		elif g == 0 and b == 255 and r < 255:
			r = updateColor(r, STEPS)

		elif r == 255 and g == 0 and b > 0:
			b = updateColor(b, -STEPS)
			
		else:
			r = 255
			g = 0
			b = 0

	# Random
	if mode == 9:
		delay = DELAY_RAND/parts
		
		if rand_switch == 0:
			if counter == 0:
				r_new = random.randint(0,255)
				if g_old<50 and b_old<50:
					r_new = random.randint(128,255)
				print 
				r_step = (r_new-r_old)/parts
				print "R: new",r_new,"step",r_step
			else:
				r = r + r_step
				
		elif rand_switch == 1:
			if counter == 0:
				g_new = random.randint(0,255)
				if r_old<50 and b_old<50:
					r_new = random.randint(128,255)
				print 
				g_step = (g_new-g_old)/parts
				print "G: new",g_new,"step",g_step
			else:
				g = g + g_step

		elif rand_switch == 2:
			if counter == 0:
				b_new = random.randint(0,255)
				if r_old<50 and g_old<50:
					b_new = random.randint(128,255)
				print 
				b_step = (b_new-b_old)/parts
				print "B: new",b_new,"step",b_step
			else:
				b = b + b_step

		if (counter) == parts:
			rand_switch = (rand_switch+1) % 3
			counter = 0
		else:
			counter = counter + 1


		
	# IF any change in color or brightness DO setLights
	if (r!=r_old or g!=g_old or b!=b_old or bright_adjust != bright_adjust_old):
		setLights()
	r_old = r;	g_old = g;	b_old = b
	bright_adjust_old = bright_adjust
	
	DELAY_RAND = PARAMETER
	DELAY_RAINBOW = 0.1 / PARAMETER
	DELAY_ALLCOLORS = 0.1 / PARAMETER
	
	delayMain(mode,delay, bright_adjust, PARAMETER)
