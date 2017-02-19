import time
from neopixel import *
import threading
import math
import RPi.GPIO as GPIO
import requests
import os
import spidev
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
APIKEY = "36dbaf4c441591ef"
CITY = "Wickliffe"
STATE = "OH"
INDICATOR = {'TOR': 'Color(255, 0, 0)', 'TOW': 'Color(255, 0, 0)', 'WRN': 'Color(255, 168, 0)', 'SEW': 'Color(255, 168, 0)', 'WIN': 'Color(77, 233, 255)', 'FLO': 'Color(5, 255, 0)', 'WAT': 'Color(5, 255, 0)', 'WND': 'Color(33, 255, 135)', 'HEA': 'Color(255, 81, 20)'} 
#conditions = {'Light Drizzle': 0, 'Drizzle': 0, 'Heavy Drizzle': 0, 'Light Rain': 0, 'Rain': 0, 'Heavy Rain': 0, 'Light Snow': 1, 'Snow': 1, 'Heavy Snow': 1, 'Light Snow Grains': 1, 'Snow Grains': 1, 'Heavy Snow Grains': 1, 'Light Ice Crystals': 1, 'Ice Crystals': 1, 'Heavy Ice Crystals': 1, 'Light Ice Pellets': 1, 'Ice Pellets': 1, 'Heavy Ice Pellets': 1, 'Light Hail': 0, 'Hail': 0, 'Heavy Hail': 0, 'Light Mist': 0, 'Mist': 0, 'Heavy Mist': 0, 'Light Fog Patches': 0, 'Fog Patches': 0, 'Heavy Fog Patches': 0, 'Light Smoke': 2, 'Smoke': 2, 'Heavy Smoke': 2, 'Light Volcanic Ash': 2, 'Volcanic Ash': 2, 'Heavy Volcanic Ash': 2, 'Light Widespread Dust': 2, 'Widespread Dust': 2, 'Heavy Widespread Dust': 2, 'Light Sand': 2, 'Sand': 2, 'Heavy Sand': 2, 'Light Haze': 0, 'Haze': 0, 'Heavy Haze': 0, 'Light Spray': 0, 'Spray': 0, 'Heavy Spray': 0, 'Light Dust Whirls': 2, 'Dust Whirls': 2, 'Heavy Dust Whirls': 2, 'Light Sandstorm': 2, 'Sandstorm': 2, 'Heavy Sandstorm': 2, 'Light Low Drifting Snow': 1, 'Low Drifting Snow': 1, 'Heavy Low Drifting Snow': 1, 'Light Low Drifting Widespread Dust': 2, 'Low Drifting Widespread Dust': 2, 'Heavy Low Drifting Widespread Dust': 2, 'Light Low Drifting Sand': 2, 'Low Drifting Sand': 2, 'Heavy Low Drifting Sand': 2, 'Light Blowing Snow': 1, 'Blowing Snow': 1, 'Heavy Blowing Snow': 1, 'Light Blowing Widespread Dust': 2, 'Blowing Widespread Dust': 2, 'Heavy Blowing Widespread Dust': 2, 'Light Blowing Sand': 2, 'Blowing Sand': 2, 'Heavy Blowing Sand': 2, 'Light Rain Mist': 0, 'Rain Mist': 0, 'Heavy Rain Mist': 0, 'Light Rain Showers': 0, 'Rain Showers': 0, 'Heavy Rain Showers': 0, 'Light Snow Showers': 1, 'Snow Showers': 1, 'Heavy Snow Showers': 1, 'Light Snow Blowing Snow Mist': 1, 'Snow Blowing Snow Mist': 1, 'Heavy Snow Blowing Snow Mist': 1, 'Light Ice Pellet Showers': 1, 'Ice Pellet Showers': 1, 'Heavy Ice Pellet Showers': 1, 'Light Hail Showers': 0, 'Hail Showers': 0, 'Heavy Hail Showers': 0, 'Light Small Hail Showers': 0, 'Small Hail Showers': 0, 'Heavy Small Hail Showers': 0, 'Light Thunderstorms': 0, 'Thunderstorms': 0, 'Heavy Thunderstorms': 0, 'Light Thunderstorms and Rain': 0, 'Thunderstorms and Rain': 0, 'Heavy Thunderstorms and Rain': 0, 'Light Thunderstorms and Snow': 1, 'Thunderstorms and Snow': 1, 'Heavy Thunderstorms and Snow': 1, 'Light Thunderstorms and Ice Pellets': 1, 'Thunderstorms and Ice Pellets': 1, 'Heavy Thunderstorms and Ice Pellets': 1, 'Light Thunderstorms with Hail': 0, 'Thunderstorms with Hail': 0, 'Heavy Thunderstorms with Hail': 0, 'Light Thunderstorms with Small Hail': 0, 'Thunderstorms with Small Hail': 0, 'Heavy Thunderstorms with Small Hail': 0, 'Light Freezing Drizzle': 1, 'Freezing Drizzle': 1, 'Heavy Freezing Drizzle': 1, 'Light Freezing Rain': 1, 'Freezing Rain': 1, 'Heavy Freezing Rain': 1, 'Light Freezing Fog': 1, 'Freezing Fog': 1, 'Heavy Freezing Fog': 1, 'Patches of Fog': 0, 'Shallow Fog': 0, 'Partial Fog': 0, 'Overcast': 0, 'Clear': 0, 'Partly Cloudy': 0, 'Mostly Cloudy': 0, 'Scattered Clouds': 0, 'Small Hail ': 0, 'Squalls': 0, 'Funnel Cloud': 2, 'Unknown Precipitation': 2, 'Unknown ': 2}
conditions = {'chanceflurries': 1, 'chancerain': 0, 'chancesleet': 1, 'chancesnow': 1, 'chancetstorms': 2, 'clear': 0, 'cloudy': 0, 'flurries': 1, 'fog': 0, 'hazy': 0, 'mostlycloudy': 0, 'mostlysunny': 0, 'partlycloudy': 0, 'partlysunny': 0, 'sleet': 1, 'rain': 0, 'snow': 1, 'sunny': 0, 'tstorms': 2, 'unknown': 2}
update_interval = 180 #In seconds

#GPIO
GPIO.setmode(GPIO.BCM)

#SPI
spi = spidev.SpiDev()
spi.open(0,0)
light_channel = 0
update_delay = 0.5

#LED strip configuration:
LED_COUNT = 30 #Number of LED Pixels.
LED_PIN = 18 #GPIO pin connected to the pixels (must support PWM!)
LED_FREQ_HZ = 800000 #LED signal frequency in hertz (usually 800khz)
LED_DMA = 5 #DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 90 #Set to 0 for darkest and 255 for brightest. 100 is the most my power supply will support.
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
#	strip.begin()
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
#			strip.begin()#Reinit strip, clear it?
			for n in range(0,26): #Clearing only the time portion of the strip
				strip.setPixelColor(n,off)
			strip.show()
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
#			print(hour, minute)  #Use this to show the actual time values that are being calculated by the above code. 
#			#Otherwise, if it's working fine, just use time.strftime to display a user-friendly time. 
			print time.strftime("%-I:%M %p, %A %B %d, %Y")
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
#			print('on')
			second = 'ON'
			strip.setPixelColor(strip.numPixels() - 1, defaultColor)
		elif second == 'ON':
			#Turn LED Off
#			print('off')
			second = 'OFF'
			strip.setPixelColor(strip.numPixels() - 1, Color(0, 0, 0))
		strip.show()
		if forceupdate == 1:
			forceupdate = 0
		time.sleep(1)

def brightnessUpdate():
	def ReadChannel(channel):
		adc = spi.xfer2([1,(8+channel)<<4,0])
		data = ((adc[1]&3) << 8) + adc[2]
		return data
	def ConvertedVolts(data,places):
		volts = (data * 3.3) / float(1023)
		volts = round(volts,places)
		return volts	
	def ReadLight():
		light_level = ReadChannel(light_channel)
		light_volts = ConvertedVolts
		#Print the results (debugging)
		#print "------------"
		#print("Light: {} ({}V)".format(light_level,light_volts
		#Return the result instead
		return light_level

	def averageBrightness():
		global running
		brightness = []
		while running == 1:
			for i in range(0,3):
				if running == 1:
					brightness.append(lightSens(lightSensPin))
					time.sleep(0.1)
			return float(sum(brightness)/len(brightness))
	#Variables for following equation
	a = 100.45162
#	a = 164.696634
	b = -0.004506
#	b = -0.004989
	global strip
	global forceupdate
	firstrun = 1
	ambientLight1 = ReadLight()
	while running == 1:
		ambientLight2 = ReadLight()
		if ambientLight1 != ambientLight2 or firstrun == 1:
			ambientLight1 = ambientLight2
			adjustedBrightness = math.ceil(a * math.pow(math.e,b*ambientLight2))
			if adjustedBrightness > 100:
				adjustedBrightness = 100
			strip.setBrightness(int(adjustedBrightness))
			strip.show()
#			print ('Brightness -', adjustedBrightness)
			if firstrun == 1:
				firstrun = 0
		else:
			pass
		time.sleep(1)

def weather(): #Run the entirity of this function once every 3 minutes, or 180 seconds. 
#	testalert = 'SVR' #If you want to test an alert type, uncomment tihs variable and the code below that refers to it. Take care to comment the code that it replaces, though. 
	def precip():
		input = str(r.json()['hourly_forecast'][0]['icon'])
		if input in conditions:
			precipType = conditions[input]
			if precipType == 0:
				precipColor = [0, 0, 255]
			if precipType == 1:
				precipColor = [245, 246, 255]
			if precipType == 2:
				precipColor = [255, 202, 32]
#			print precipColor #Debugging
		pop = float(r.json()['hourly_forecast'][0]['pop'])/100
		popIndic = "Color(" + str(int(precipColor[0] * pop)) + ", " + str(int(precipColor[1] * pop)) + ", " + str(int(precipColor[2] * pop)) + ")" 
#		print popIndic
		return popIndic
        def tempColor():
		try:
	                colorval = []
	                temp = int(r.json()['hourly_forecast'][0]['temp']['english'])
			print temp
	                def colorCalc(temp, focus):
        	                result = -abs((256/28)*temp - ((256/28) * focus)) + 256
                	        if result < 0: #So, if the result is subzero,
                        	        result = 0
	                        return result
        	        def blueCalc(temp):
                	        return colorCalc(temp, 30)
	                def greenCalc(temp):
        	                return colorCalc(temp, 60)
                	def redCalc(temp):
	                        return colorCalc(temp, 90)
        	        def whiteCalc(temp):
	        	        if temp <= 30:
        	        	        return colorCalc(temp, 0)
	                	elif temp >= 90:
        	                	return colorCalc(temp, 120)
				else:
					return 0
	                colorval.insert(0, redCalc(temp) + whiteCalc(temp))
        	        colorval.insert(1, greenCalc(temp) + whiteCalc(temp))
                	colorval.insert(2, blueCalc(temp) + whiteCalc(temp))
	                rgb = "Color(" + `colorval[0]` +", " +  `colorval[1]` + ", " + `colorval[2]` + ")"
#        	        print rgb
			return rgb
		except:
#			print ("There's been an error in the tempColor function.")
#			rgb = "Color(0, 0, 0)"
#			return rgb
			raise
	global strip
	global defaultColor
	time_marker = 0
	while running == 1:
		if time_marker + update_interval <= time.time():
			time_marker = time.time()
			try:
				r = requests.get('http://api.wunderground.com/api/' + str(APIKEY) + '/alerts/hourly/q/' + str(STATE) + '/' + str(CITY) + '.json?apiref=0bcd59e502b38b2e')
				# Parsing and displaying the probability of precip.
#				alertval = str(r.json()['alerts'][0]['type']) 
#      				pop = "Color(0, 0, " + str(int((float(str(r.json()['hourly_forecast'][0]['pop']))/100)*255)) + ")"
				popval = r.json()['hourly_forecast'][0]['pop']
				strip.setPixelColor(strip.numPixels() - 4, eval(tempColor()))
				strip.setPixelColor(strip.numPixels() - 3, eval(precip()))
				# Checking for weather alerts, comparing them against my dictionary of color values, and displaying them.
				strip.setPixelColor(strip.numPixels() - 2, eval(INDICATOR[str(r.json()['alerts'][0]['type'])]))
#				strip.setPixelColor(strip.numPixels() - 2, eval(INDICATOR[testalert]))
				alert = str(r.json()['alerts'][0]['type'])
				if alert == 'TOR' or alert == 'WRN' or alert == 'FLO': 
#				if str(testalert) == 'TOR' or str(testalert) == 'WRN' or str(testalert) == 'FLO': 
					defaultColor = eval(INDICATOR[str(r.json()['alerts'][0]['type'])]) 
#					print(INDICATOR[str(testalert)]) 
#					defaultColor = eval(INDICATOR[str(testalert)])
				else:
					defaultColor = Color(255, 147, 41)
			except IndexError:
				print('Currently, there are no severe weather alerts for your area, though there is a', eval(popval), '% chance of precip.')
#				print ", ".join('Currently, there are no severe weather alerts for your area, though there is a', eval(pop),'% chance of precip.')
				defaultColor = Color(255, 147, 41) #We know of this error and there are no weather alerts, so make sure the second indicator is its normal color
				strip.setPixelColor(strip.numPixels() - 2, Color(255,147,41))
				pass
			except requests.ConnectionError:
				print("There's an issue with the network.")
				defaultColor = Color(255, 0, 0) #Indicate an error
				pass
#			except requests.JSONDecodeError:
			except ValueError:
				print("There's an isse with the .json file we pulled down. Trying again in a few minutes.")
				defaultColor = Color(255, 0, 0)
				pass
#				raise #Something's up. Need to debug it. 12-8-16
			except KeyError:
				print("There's a weather situation, but it doesn't apply to this program.")
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
