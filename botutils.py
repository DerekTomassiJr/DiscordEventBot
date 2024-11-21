import time
import asyncio
from threading import Timer

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
		return f"{self.month}/{self.day}/{self.year}"

	def wait(self, second):
		startSecond = self.getSecond()
		endSecond = startSecond + second
		currentSecond = self.getSecond()

		while not(currentSecond >= endSecond):
			if currentSecond == self.getSecond():
				continue
			else:
				currentSecond = self.getSecond()
	# end of wait()

	# following methods will be used in the event part of the bot    
	def getMonth(self):
		self.update()
		return self.month
	
	def getDay(self):
		self.update()
		return self.day

	def getYear(self):
		self.update()
		return self.year

	def getHour(self):
		self.update()
		return self.hour
	
	def getMinute(self):
		self.update()
		return self.minute
	
	def getSecond(self):
		self.update()
		return self.second

class BotTimer:
    def __init__(self, timeout, callback):
        self.timeout = timeout
        self.callback = callback
        self.task = asyncio.ensure_future(self.job())
    
    async def job(self):
        await asyncio.sleep(self.timeout)
        await self.callback()

    def cancel(self):
         self.task.cancel()

class Date:
    month = None
    day = None
    year = None

    def __init__(self, month, day, year):
        self.month = int(month)
        self.day = int(day)
        self.year = int(year)
    
    def getFormattedDate(self):
        return f"{self.month}/{self.day}/{self.year}"

    def isValid(self):
        clock = Clock()
        
        if self.year > clock.getYear():
            return True
        elif self.year == clock.getYear():
            if self.month >= clock.getMonth() and self.month <= 12 and self.month >= 1:
                if self.day <= 31 and self.month >= 1:
                    return True
        else:
            return False 

class Event:
    title = None
    game = None
    author = None
    date = None
    startTime = None
    joinedUsers = None
    userLimit = None
    joinedUserList = None;
    

    def __init__(self, title, game, author, date, startTime, joinedUsers, userLimit):
        self.title = title
        self.game = game
        self.author = author
        self.date = date
        self.startTime = startTime
        self.joinedUsers = joinedUsers
        self.userLimit = userLimit
        self.joinedUserList = [self.author]

    # Getters and Setters

    def getTitle(self):
        return self.title

    def setTitle(self, newTitle):
        self.title = newTitle

    def getGame(self):
        return self.game
        
    def setGame(self, newGame):
        self.game = newGame
        
    def getAuthor(self):
        return self.author
        
    def setAuthor(self, newAuthor):
        self.author = newAuthor
        
    def getStartTime(self):
        return self.startTime
        
    def setStartTime(self, newStartTime):
        self.startTime = newStartTime

    def getDate(self):
        return self.date

    def setDate(self, newDate):
        self.date = newDate

    def getJoinedUsers(self):
        return self.joinedUsers
        
    def setJoinedUsers(self, newJoinedUsers):
        self.joinedUsers = newJoinedUsers
        
    def getUserLimit(self):
        return int(self.userLimit)
        
    def setUserLimit(self, newUserLimit):
        self.userLimit = newUserLimit

    def getJoinedUserList(self):
        return self.joinedUserList

    def getJoinedUserNameList(self):
        userNameList = []
        for user in self.joinedUserList:
            userNameList.append(user.name)
        return userNameList
    
    def getUserByName(self, userName):
        for user in self.joinedUserList:
            if user.name == userName:
                return user
        return None
     
    def append(self, newUser):
        self.joinedUserList.append(newUser)
        
    def remove(self, user):
        self.joinedUserList.remove(user)

    def toString(self):
        maxUsers = self.userLimit
        print(str(maxUsers))
        if int(self.userLimit) == 0:
            maxUsers = "INF"
        
        return f"Event Bot : {self.title}\nBy: {self.author}\nGame: {self.game}\nDate: {self.date.getFormattedDate()}\nStarting: {self.startTime}\nUsers: {len(self.joinedUserList)} / {maxUsers}"