import time
from neopixel import *
import threading
import math
import RPi.GPIO as GPIO
import requests
defaultColor = Color(255, 147, 41)
minuteColor = Color(255, 147, 41)
hourColor = Color(255, 147, 41)
red = Color(255, 0, 0)
green = Color(0, 255, 0)
blue = Color(0, 0, 255)
off = Color(0, 0, 0)
white = Color(255, 255, 255)
placeholder = blue

#Weather Underground
APIKEY = "0f9045beb1c7e0e7"
CITY = "Cuyahoga_Falls"
STATE = "OH"
INDICATOR = {'TOR': 'Color(255, 0, 0)', 'TOW': 'Color(255, 0, 0)', 'WRN': 'Color(255, 168, 0)', 'SEW': 'Color(255, 168, 0)', 'WIN': 'Color(77, 233, 255)', 'FLO': 'Color(5, 255, 0)', 'WAT': 'Color(5, 255, 0)', 'WND': 'Color(33, 255, 135)', 'HEA': 'Color(255, 81, 20)'} 
update_interval = 180 #In seconds

#GPIO
GPIO.setmode(GPIO.BCM)
lightSensPin = 25

#LED strip configuration:
LED_COUNT = 30 #Number of LED Pixels.
LED_PIN = 18 #GPIO pin connected to the pixels (must support PWM!)
LED_FREQ_HZ = 800000 #LED signal frequency in hertz (usually 800khz)
LED_DMA = 5 #DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 74 #Set to 0 for darkest and 255 for brightest. 100 is the most my power supply will support.
LED_INVERT = False #True to invert the signal (when using NPN transistor level shift)

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)

forceupdate = 1

def timeCheck():
	currentTime = time.localtime()
	return currentTime

def updateClock():
	global running
	global forceupdate
	global strip
	hour = time.localtime().tm_hour
	minute = time.localtime().tm_min
	second = 'OFF'
	#For Debugging
#	print(time.localtime().tm_hour - 12, time.localtime().tm_min)
	while running == 1:
		actualTime = timeCheck()
		if actualTime.tm_hour == 0:
			convertedHour = 12
		if actualTime.tm_hour >=13:
			convertedHour = actualTime.tm_hour - 12
		if 1 <= actualTime.tm_hour <=12:
			convertedHour = actualTime.tm_hour
		if convertedHour - hour == 1 or convertedHour - hour == -11 or forceupdate == 1: 
			hour = actualTime.tm_hour
			strip.begin()#Reinit strip, clear it?
#			print('pre', hour)
			if hour == 0:
				hour = 12
			if hour >= 13:
				hour = hour - 12
			hour_str = str(hour)
#			print('post', hour)
			if 1 <= hour <= 9:
				for x in xrange(hour):
					strip.setPixelColor(x, hourColor)
				inuseHour = hour - 1
			if 10 <= hour:
				for x in xrange(int(hour_str[0])):
					strip.setPixelColor(x, hourColor)
				if int(hour_str[1]) == 0:
					strip.setPixelColor(int(hour_str[0]), placeholder)
					inuseHour = int(hour_str[0])
					secondary_minute_str = str(actualTime.tm_min)
					for x in range(1, 20 ):
						strip.setPixelColor(inuseHour + 3 + int(secondary_minute_str[0]) + x, Color(0, 0, 0))
				else:
					for x in xrange(int(hour_str[1])):
#						strip.setPixelColor(int(hour_str[0]) + 1, Color(0, 0, 0))
						strip.setPixelColor(int(hour_str[0]) + 1 + x, hourColor)
					inuseHour = int(hour_str[0]) + int(hour_str[1])
#			print(hour)
			#Here, add another pixil to the clock
		if actualTime.tm_min - minute == 1 or actualTime.tm_min - minute == -59 or forceupdate == 1:
#			print('look here', convertedHour - hour)
#			print('tm_hour', convertedHour)
#			print('hour', hour)
			minute = actualTime.tm_min
			minute_str = str(minute)
#			print(minute)
#			print(inuseHour)
			#minute action here
			print(hour, minute)
			if minute == 0:
				for x in xrange(inuseHour + 1, inuseHour + 15):
					strip.setPixelColor(x, Color(0, 0, 0))	#Clear the minutes
			if 1 <= minute <= 9:
				for x in xrange(minute):
					strip.setPixelColor(inuseHour + x + 3, minuteColor)
			if 10 <= minute:
				for x in xrange(int(minute_str[0])):
					strip.setPixelColor(inuseHour + x + 3, minuteColor)
				if int(minute_str[1]) == 0:
					strip.setPixelColor(inuseHour + 3 + int(minute_str[0]), placeholder)
					for x in range(1,10):
						strip.setPixelColor(inuseHour + 3 + int(minute_str[0]) + x, Color(0, 0, 0))
				else:
					for x in xrange(int(minute_str[1])):
						strip.setPixelColor(inuseHour + 3 +  int(minute_str[0]), Color(0, 0, 0))
						strip.setPixelColor(inuseHour + 3 + int(minute_str[0]) + 1 + x, minuteColor)
		if second == 'OFF':
			#Turn LED On
			print('on')
			second = 'ON'
			strip.setPixelColor(strip.numPixels() - 1, defaultColor)
		elif second == 'ON':
			#Turn LED Off
			print('off')
			second = 'OFF'
			strip.setPixelColor(strip.numPixels() - 1, Color(0, 0, 0))
		strip.show()
		if forceupdate == 1:
			forceupdate = 0
		time.sleep(1)

def brightnessUpdate():
	def lightSens(x):
		global running
		while running == 1:
			reading = 0
			GPIO.setup(x, GPIO.OUT)
			GPIO.output(x, GPIO.LOW)
			time.sleep(0.1)
			GPIO.setup(x, GPIO.IN)
			while (GPIO.input(x) == GPIO.LOW):
				reading += 1
			return reading
	def averageBrightness():
		global running
		brightness = []
		while running == 1:
			for i in range(0,5):
				while running == 1:
					brightness.append(lightSens(lightSensPin))
					time.sleep(1)
			return float(sum(brightness)/len(brightness))
	#Variables for following equation
	a = 111.63
	b = 0.999998
	global strip
	global forceupdate
	firstrun = 1
	ambientLight1 = averageBrightness()
	while running == 1:
		ambientLight2 = averageBrightness()
		if ambientLight1 != ambientLight2 or firstrun == 1:
			ambientLight1 = ambientLight2
			adjustedBrightness = math.ceil(a * math.pow(b,ambientLight2))
			if adjustedBrightness > 100:
				adjustedBrightness = 100
			strip.setBrightness(int(adjustedBrightness))
			strip.show()
			print ('Brightness -', adjustedBrightness)
			if firstrun == 1:
				firstrun = 0
		else:
			pass
		time.sleep(1)

def weather(): #Run the entirity of this function once every 3 minutes, or 180 seconds. 
#		testalert = 'HEA' #If you want to test an alert type, uncomment tihs variable and the code below that refers to it. Take care to comment the code that it replaces, though. 
		global strip
		global defaultColor
		time_marker = 0
		while running == 1:
			if time_marker + update_interval <= time.time():
				time_marker = time.time()
				try:
					r = requests.get('http://api.wunderground.com/api/' + str(APIKEY) + '/alerts/hourly/q/' + str(STATE) + '/' + str(CITY) + '.json')
					# Parsing and displaying the probability of precip.
					pop = "Color(0, 0, " + str(int((float(str(r.json()['hourly_forecast'][0]['pop']))/100)*255)) + ")"
					strip.setPixelColor(strip.numPixels() - 3, eval(pop))
					# Checking for weather alerts, comparing them against my dictionary of color values, and displaying them.
					strip.setPixelColor(strip.numPixels() - 2, INDICATOR[str(r.json()['alerts'][0]['type'])])
#					strip.setPixelColor(strip.numPixels() - 2, eval(INDICATOR[testalert]))
					if str(r.json()['alerts'][0]['type']) == 'TOR' or 'WRN' or 'FLO': 
#					if str(testalert) == 'TOR' or str(testalert) == 'WRN' or str(testalert) == 'FLO': 
						defaultColor = INDICATOR[str(r.json()['alerts'][0]['type'])] 
#						print(INDICATOR[str(testalert)]) 
#						defaultColor = eval(INDICATOR[str(testalert)])
					else:
						defaultColor = Color(255, 147, 41)
				except IndexError:
					print('Currently, there are no severe weather alerts for your area.')
					defaultColor = Color(255, 147, 41) #We know of this error and there are no weather alerts, so make sure the second indicator is its normal color
					pass
				except requests.ConnectionError:
					print("There's an issue with the network.")
					defaultColor = Color(255, 0, 0) #Indicate an error
					pass
				except:
					defaultColor = Color(255, 0, 0) #Indicate an error
					raise
			else:
				time.sleep(1) 

# Supported Alerts
# TOR - Tornado Warning
# TOW - Tornado Watch
# WRN - Severe Thunderstorm Warning
# SEW - Severe Thunderstorm Watch
# WIN - Winter Weather
# FLO - Flood Warning
# WAT - Flood Watch
# WND - Wind Advisory
# HEA - Heat Advisory
#
# Watches will consist of a solid color above the second indicator
# Warnings will consist of a solid color above the second indicator as well as having the second indicator the same color
def startThreads():
	try:
		global running
		closing_event = threading.Event()
		closing_event.set()
		brightnessThread = threading.Thread(target=brightnessUpdate)
		clockThread = threading.Thread(target=updateClock)
		weatherThread = threading.Thread(target=weather)
		brightnessThread.start()
		clockThread.start()
		weatherThread.start()
		while True:
			time.sleep(0.5)
			if not closing_event.is_set():
				break
	except KeyboardInterrupt:
		print "Finishing Up"
		closing_event.clear()
		running = 0
		brightnessThread.join()
		clockThread.join()
		weatherThread.join()
		for n in range(0,30):
			strip.setPixelColor(n, off)
			strip.show()
			time.sleep(0.1)					

if __name__ == '__main__':
	running = 1
	strip.begin()
	startThreads()
