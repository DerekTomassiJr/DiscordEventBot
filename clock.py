import time

'''
TODO
 - add date to events
 - find a way that you can have the clock do comparison every 10 minutes
 - midnight check
 - command parser
'''
class Clock:
	local_time = None
	month = None
	day = None
	year = None
	hour = None
	minute = None
	second = None
	
	def __init__(self):
		self.local_time = time.localtime(time.time())
		self.month = self.local_time.tm_mon
		self.day = self.local_time.tm_mday
		self.year = self.local_time.tm_year
		self.hour = self.local_time.tm_hour
		self.minute = self.local_time.tm_min
		self.second = self.local_time.tm_sec
	
	'''
	 reinitializes all variables to the current time
	'''
	def update(self):
		self.local_time = time.localtime(time.time())
		self.month = self.local_time.tm_mon
		self.day = self.local_time.tm_mday
		self.year = self.local_time.tm_year
		self.hour = self.local_time.tm_hour
		self.minute = self.local_time.tm_min
		self.second = self.local_time.tm_sec
	
	
	# following methods are for testing purposes
	'''
	 returns a string with the time in HH:MM:SS
	'''
	def clock(self):
		self.update()
		t = str(self.hour) + ":" + str(self.minute) + ":" + str(self.second)
		return t
	

	'''
	 returns a string with the date in MM/DD/YY
	'''
	def date(self):
		self.update()
		d = str(self.month) + "/" + str(self.day) + "/" + str(self.year)
		return d

	def wait(self, second):
		startSecond = self.getSecond()
		endSecond = startSecond + second
		currentSecond = self.getSecond()

		while not(currentSecond == endSecond):
			if currentSecond == self.getSecond():
				continue
			else:
				currentSecond = self.getSecond()
	# end of wait()

	# following methods will be used in the event part of the bot
	def is_time(self, t_time):
		self.update()
		return t_time == int((str(hour) + str(minute)))	
	
	def getHour(self):
		self.update()
		return self.hour
	
	def getMinute(self):
		self.update()
		return self.minute
	
	def getSecond(self):
		self.update()
		return self.second

