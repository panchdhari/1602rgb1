#!/usr/bin/python


# Driver for HD44780 LCD display on the RPi
# Written by: Ron Ritchey
# Derived from Lardconcepts
# https://gist.github.com/lardconcepts/4947360
# Which was also drived from Adafruit
# http://forums.adafruit.com/viewtopic.php?f=8&t=29207&start=15#p163445
#
# Useful references
# General overview of HD44780 style displays
# https://en.wikipedia.org/wiki/Hitachi_HD44780_LCD_controller
#
# More detail on initialization and timing
# http://web.alfredstate.edu/weimandn/lcd/lcd_initialization/lcd_initialization_index.html
#

import time, math,logging
import fonts
import wiringpi

LCD_ADDRESS = (0x7c>>1)
RGB_ADDRESS = (0xc0>>1)
WHITE      =     0
RED        =     1
GREEN      =     2
BLUE       =     3
REG_RED    =     0x04
REG_GREEN  =     0x03
REG_BLUE   =     0x02
REG_MODE1  =     0x00
REG_MODE2  =     0x01
REG_OUTPUT =     0x08
LCD_CLEARDISPLAY = 0x01
LCD_RETURNHOME = 0x02
LCD_ENTRYMODESET = 0x04
LCD_DISPLAYCONTROL = 0x08
LCD_CURSORSHIFT = 0x10
LCD_FUNCTIONSET = 0x20
LCD_SETCGRAMADDR = 0x40
LCD_SETDDRAMADDR = 0x80
LCD_CLEARDISPLAY = 0x01
LCD_RETURNHOME = 0x02
LCD_ENTRYMODESET = 0x04
LCD_DISPLAYCONTROL = 0x08
LCD_CURSORSHIFT = 0x10
LCD_FUNCTIONSET = 0x20
LCD_SETCGRAMADDR = 0x40
LCD_SETDDRAMADDR = 0x80
LCD_ENTRYRIGHT = 0x00
LCD_ENTRYLEFT = 0x02
LCD_ENTRYSHIFTINCREMENT = 0x01
LCD_ENTRYSHIFTDECREMENT = 0x00
LCD_DISPLAYON = 0x04
LCD_DISPLAYOFF = 0x00
LCD_CURSORON = 0x02
LCD_CURSOROFF = 0x00
LCD_BLINKON = 0x01
LCD_BLINKOFF = 0x00
LCD_DISPLAYMOVE = 0x08
LCD_CURSORMOVE = 0x00
LCD_DISPLAYMOVE = 0x08
LCD_CURSORMOVE = 0x00
LCD_MOVERIGHT = 0x04
LCD_MOVELEFT = 0x00
LCD_8BITMODE = 0x10
LCD_4BITMODE = 0x00
LCD_2LINE = 0x08
LCD_1LINE = 0x00
LCD_5x10s = 0x04
LCD_5x8DOTS = 0x00
LCD_BACKLIGHT  = 0x08  # On
LCD_BACKLIGHT = 0x00  # Off
ENABLE = 0b00000100 # Enable bit

try:
	import smbus
except:
	logging.debug("smbus not installed")


class hd44780_i2c():


   def __init__(self, rows=16, cols=80, i2c_addr=0x27, i2c_bus=1, enable_duration=1):
     self._row = rows
     self._col = cols
     print("LCD _row=%d _col=%d"%(self._row,self._col))
     self.LCD = wiringpi.wiringPiI2CSetup(LCD_ADDRESS)
     self.RGB = wiringpi.wiringPiI2CSetup(RGB_ADDRESS)
     self._showfunction = LCD_4BITMODE | LCD_1LINE | LCD_5x8DOTS;
     self.begin(self._row,self._col)
    
    
   def delayMicroseconds(self, microseconds):
     seconds = microseconds / 1000000.0 
     time.sleep(seconds)

   def command(self,cmd):
	   b=bytearray(2)
	   b[0]=0x80
	   b[1]=cmd
	   wiringpi.wiringPiI2CWriteReg8(self.LCD,0x80,cmd)

   def write4bits(self, bits, mode=False):
     b=bytearray(2)
     b[0]=0x40
     b[1]=data
     wiringpi.wiringPiI2CWriteReg8(self.LCD,0x40,data)

   def write(self,data):
    b=bytearray(2)
    b[0]=0x40
    b[1]=data
    wiringpi.wiringPiI2CWriteReg8(self.LCD,0x40,data)
    
   def setReg(self,reg,data):
    b=bytearray(1)
    b[0]=data
    wiringpi.wiringPiI2CWriteReg8(self.RGB,reg,data)


   
   def lcd_toggle_enable(self, bits):
     self.delayMicroseconds(self.enable_duration)

   def createcustom(self, image):
     return self.currentcustom - 1

   def compare(self, image, position):
     return False

   def setRGB(self,r,g,b):
            self.setReg(REG_RED,r)
            self.setReg(REG_GREEN,g)
            self.setReg(REG_BLUE,b)


   def update(self, image):
        	a=1

   def clear(self):
       self.command(LCD_CLEARDISPLAY)
       time.sleep(0.002)

   def setCursor(self, col_char, row_char):
       if(row_char == 0):
           col_char|=0x80
       else:
           col_char|=0xc0;
       self.command(col_char)

   def loadcustomchars(self, char, fontdata):
       location &= 0x7  # we only have 8 locations 0-7
       self.command(LCD_SETCGRAMADDR | (location << 3))
       #data = bytearray(9);
       data = 0x40 
       for i in range(0,8):
           wiringpi.wiringPiI2CWriteReg8(self.LCD,0x40,charmap[i])

   def message(self, arg):
	   if(isinstance(arg,int)):
		   arg=str(arg)
	   for x in bytearray(arg,'utf-8'):
		   self.write(x)

   def msgtest(self, text, wait=1.5):
       self.clear()
       lcd.message(text)
       time.sleep(wait)
   
   def home(self):
       self.command(LCD_RETURNHOME)        # set cursor position to zero
       time.sleep(1)        # this command takes a long time!
    
   def noDisplay(self):
       self._showcontrol &= ~LCD_DISPLAYON 
       self.command(LCD_DISPLAYCONTROL | self._showcontrol)

   def display(self):
       self._showcontrol |= LCD_DISPLAYON 
       self.command(LCD_DISPLAYCONTROL | self._showcontrol)

   def stopBlink(self):
    		self._showcontrol &= ~LCD_BLINKON 
    		self.command(LCD_DISPLAYCONTROL | self._showcontrol)

   def blink(self):
    		self._showcontrol |= LCD_BLINKON 
    		self.command(LCD_DISPLAYCONTROL | self._showcontrol)

   def noCursor(self):
    		self._showcontrol &= ~LCD_CURSORON 
    		self.command(LCD_DISPLAYCONTROL | self._showcontrol)

   def cursor(self):
    		self._showcontrol |= LCD_CURSORON 
    		self.command(LCD_DISPLAYCONTROL | self._showcontrol)

   def leftToRight(self):
    		self._showmode |= LCD_ENTRYLEFT 
    		self.command(LCD_ENTRYMODESET | self._showmode)

   def rightToLeft(self):
    		self._showmode &= ~LCD_ENTRYLEFT 
    		self.command(LCD_ENTRYMODESET | self._showmode)

   def noAutoscroll(self):
    		self._showmode &= ~LCD_ENTRYSHIFTINCREMENT 
    		self.command(LCD_ENTRYMODESET | self._showmode)

   def autoscroll(self):
    		self._showmode |= LCD_ENTRYSHIFTINCREMENT 
    		self.command(LCD_ENTRYMODESET | self._showmode)

   def blinkLED(self):
    # blink period in seconds = (<reg 7> + 1) / 24
    # on/off ratio = <reg 6> / 256
    		self.setReg(0x07, 0x17)  # blink every second
    		self.setReg(0x06, 0x7f)  # half on, half off

   def noBlinkLED(self):
    		self.setReg(0x07, 0x00)
    		self.setReg(0x06, 0xff)
   def blink_on(self):
    		self.blink()

   def blink_off(self):
    		self.stopBlink()

   def cursor_on(self):
    		self.cursor()

   def cursor_off(self):
    		self.noCursor()

   def setBacklight(self,new_val):
       if(new_val):
           self.blinkLED()      # turn backlight on
       else:
           self.noBlinkLED()        # turn backlight off

   def load_custom_character(self,char_num,rows):
       self.customSymbol(char_num, rows)


   def begin(self,cols,lines,dotsize=LCD_5x8DOTS):
	   if (lines > 1):
		   self._showfunction |= LCD_2LINE 
	   self._numlines = lines
	   self._currline = 0 
	   if ((dotsize != 0) and (lines == 1)) :
		   self._showfunction |= LCD_5x10DOTS 
	   time.sleep(0.05)
	   self.command(LCD_FUNCTIONSET | self._showfunction);
	   time.sleep(0.005)
	   self.command(LCD_FUNCTIONSET | self._showfunction);
	   time.sleep(0.005)
	   self.command(LCD_FUNCTIONSET | self._showfunction)
	   self.command(LCD_FUNCTIONSET | self._showfunction)
	   self._showcontrol = LCD_DISPLAYON | LCD_CURSOROFF | LCD_BLINKOFF 
	   self.display()
	   self.clear()
	   self._showmode = LCD_ENTRYLEFT | LCD_ENTRYSHIFTDECREMENT 
	   self.command(LCD_ENTRYMODESET | self._showmode);
	   self.setReg(REG_MODE1, 0)
	   self.setReg(REG_OUTPUT, 0xFF)
	   self.setReg(REG_MODE2, 0x20)
	   self.setColorWhite()

   def setColorWhite(self):
	   self.setRGB(255, 255, 255)
   
   def setPWM(self,color,pwm):
	   self.setReg(color, pwm)
    
   def setColorAll(self):
    		self.setRGB(0, 0, 0)



if __name__ == '__main__':

	import getopt,sys, os
	#import graphics as g
	import fonts
	#import display
	#import moment

	def processevent(events, starttime, prepost, db, dbp):
		for evnt in events:
			t,var,val = evnt

			if time.time() - starttime >= t:
				if prepost in ['pre']:
					db[var] = val
				elif prepost in ['post']:
					dbp[var] = val

	db = {
			'actPlayer':'mpd',
			'playlist_position':1,
			'playlist_length':5,
	 		'title':"Nicotine & Gravy",
			'artist':"Beck",
			'album':'Midnight Vultures',
			'elapsed':0,
			'length':400,
			'volume':50,
			'stream':'Not webradio',
			'utc': 	0,
			'outside_temp_formatted':u'46\xb0F',
			'outside_temp_max':72,
			'outside_temp_min':48,
			'outside_conditions':'Windy',
			'system_temp_formatted':u'98\xb0C',
			'state':'stop',
			'system_tempc':81.0
		}

	dbp = {
			'actPlayer':'mpd',
			'playlist_position':1,
			'playlist_length':5,
	 		'title':"Nicotine & Gravy",
			'artist':"Beck",
			'album':'Midnight Vultures',
			'elapsed':0,
			'length':400,
			'volume':50,
			'stream':'Not webradio',
			'utc': 	0,
			'outside_temp_formatted':u'46\xb0F',
			'outside_temp_max':72,
			'outside_temp_min':48,
			'outside_conditions':'Windy',
			'system_temp_formatted':u'98\xb0C',
			'state':'stop',
			'system_tempc':81.0
		}

	events = [
		(15, 'state', 'play'),
		(20, 'title', 'Mixed Bizness'),
		(30, 'volume', 80),
		(40, 'title', 'I Never Loved a Man (The Way I Love You)'),
		(40, 'artist', 'Aretha Franklin'),
		(40, 'album', 'The Queen Of Soul'),
		(40, 'playlist_position', 2),
		(70, 'state', 'stop'),
		(90, 'state', 'play'),
		(100, 'title', 'Do Right Woman, Do Right Man'),
		(100, 'playlist_position', 3),
		(120, 'volume', 100),
		(140, 'state', 'play' )
	]




	try:
		opts, args = getopt.getopt(sys.argv[1:],"hr:c:",["row=","col=","addr=","bus="])
	except getopt.GetoptError:
		print ('hd44780_i2c.py -r <rows> -c <cols> --addr <i2c addr> --bus <i2c bus> --enable <duration in microseconds>')
		sys.exit(2)

	# Set defaults
	# These are for the wiring used by a Raspdac V3
	rows = 80
	cols = 16
	i2c_addr = 0x3E
	i2c_bus = 1
	enable = 1

	for opt, arg in opts:
		if opt == '-h':
			print ('hd44780.py -r <rows> -c <cols> --addr <i2c addr> --bus <i2c bus> --enable <duration in microseconds>')
			sys.exit()
		elif opt in ("-r", "--rows"):
			rows = int(arg)
		elif opt in ("-c", "--cols"):
			cols = int(arg)
		elif opt in ("--addr"):
			i2c_addr  = int(arg)
		elif opt in ("--bus"):
			i2c_bus  = int(arg)
		elif opt in ("--enable"):
			enable = int(arg)

	try:

		print ("HD44780 I2C LCD Display Test")
		print ("ROWS={0}, COLS={1}, I2C Addr={2}, I2C Bus={3} enable duraction={4}".format(rows,cols,i2c_addr,i2c_bus,enable))

		lcd = hd44780_i2c(rows,cols,i2c_addr, i2c_bus, enable)
		lcd.clear()
		lcd.setRGB(192,168,200)
		lcd.autoscroll()
		lcd.message("HD44780 LCD  Pi Powered :-)")
		time.sleep(4)

		starttime = time.time()
		elapsed = int(time.time()-starttime)
		timepos = time.strftime(u"%-M:%S", time.gmtime(int(elapsed))) + "/" + time.strftime(u"%-M:%S", time.gmtime(int(254)))

		

		starttime=time.time()
		counter=1
		while True:
			lcd.setCursor(0,1)
			lcd.message(counter)
			counter=counter+1
			time.sleep(1)

		lcd.clear()

		time.sleep(2)


	except KeyboardInterrupt:
		pass

	finally:
		try:
			lcd.clear()
			lcd.message("Goodbye!")
			time.sleep(2)
			lcd.clear()
		except:
			pass
		time.sleep(.5)
		print ("LCD Display Test Complete")
