import time
from neopixel import *
import threading

defaultColor = Color(255, 147, 41)
minuteColor = Color(255, 147, 41)
hourColor = Color(255, 147, 41)
red = Color(255, 0, 0)
green = Color(0, 255, 0)
blue = Color(0, 0, 255)
placeholder = blue
#LED strip configuration:
LED_COUNT = 30 #Number of LED Pixels.
LED_PIN = 18 #GPIO pin connected to the pixels (must support PWM!)
LED_FREQ_HZ = 800000 #LED signal frequency in hertz (usually 800khz)
LED_DMA = 5 #DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 2 #Set to 0 for darkest and 255 for brightest. 100 is the most my power supply will support.
LED_INVERT = False #True to invert the signal (when using NPN transistor level shift)

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)

forceupdate = 1

def timeCheck():
	currentTime = time.localtime()
	return currentTime

def updateClock():
	global running
	global forceupdate
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
		if convertedHour - hour == 1 or convertedHour - hour == -11 or forceupdate == 1: 
			hour = actualTime.tm_hour
			strip.begin()#Reinit strip, clear it?
			print('pre', hour)
			if hour == 0:
				hour = 12
			if hour >= 13:
				hour = hour - 12
			hour_str = str(hour)
			print('post', hour)
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
						strip.setPixelColor(int(hour_str[0]) + 1, Color(0, 0, 0))
						strip.setPixelColor(int(hour_str[0]) + 1 + x, hourColor)
					inuseHour = int(hour_str[0]) + 1 + int(hour_str[1])
			print(hour)
			#Here, add another pixil to the clock
		if actualTime.tm_min - minute == 1 or actualTime.tm_min - minute == -59 or forceupdate == 1:
			print('look here', convertedHour - hour)
			print('tm_hour', convertedHour)
			print('hour', hour)
			minute = actualTime.tm_min
			minute_str = str(minute)
			print(minute)
			print(inuseHour)
			#minute action here
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
		#Check hour, minute, second

def brightnessUpdate():
	#Poll for brightness once per second, and reconfigure 'strip.led_brightness' based on sensor readings. 
	#For now, though, just do nothing. 
	#Take a look at the built_in brightness ajusting function. Refer to pydoc neopixel for more information
	global strip
	global forceupdate
	while True:
		#Poll for brightness change, determine if brightness setting needs to be changed
		if LED_BRIGHTNESS != LED_BRIGHTNESS: #Then, enact the change
			strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)		
			forceupdate = 1
		time.sleep(1)

#def startThreads():
#	brightnessThread = threading.Thread(target=brightnessUpdate)
#	brightnessThread.start()
		
if __name__ == '__main__':
	running = 1
	strip.begin()
#	brightnessUpdate()
	updateClock()	
