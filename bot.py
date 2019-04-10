"""
List of Commands for the Bot
!createEvent ~
!joinedUsers ~
!deleteEvent ~
!changeEventTime ~
!changeEventGame ~
!changeUserLimit ~
!events ~
!joinEvent ~
!leaveEvent
!kick ~
!end
"""
import discord
from Event import Event
from clock import Clock

# global variables
client = discord.Client()
events = []

class EventBot:
	client = None
	clock = Clock()

	# channels
	generalId = None
	commandsId = None
	eventCommandsId = None
	messageChannel = None

	botToken = None

	""" Bot initialization """
	def __init__(self, client):
		self.client = client
		self.generalId = 554882293194555397
		self.commandsId = 557855504416636931
		self.eventCommandsId = 555094463907758090
		self.botToken = "NTU3ODQ3MjcwODM4NzYzNTIx.XKIMSA.Bs2UXTlPTd756a7qHrbm29A0J6o"
		return None
	#end of __init__

	'''
	Initializes the bot in the server
	'''
	def run(self):
		self.client.run(self.botToken)
	# end of run


	""" Bot utilities """
	'''
	sends a test message in the general channel
	'''
	async def testMessage(self, message):
		await self.sendMessage(message, self.generalId)
	# end of testMessage

	'''
	sends a message given a channel ID
	'''
	async def sendMessage(self, message, channelID):
		print("Sending message: " + message)
		channel = self.client.get_channel(channelID)
		await channel.send(f"{message}")
	# end of sendMessage

	'''
	prompt a user for a message and only takes messages from the user that wrote the command
	'''
	async def prompt(self, prompt, message):
		author = message.author

		def check(m):
			return m.content and m.author == author

		await self.messageChannel.send(f"{prompt}")
		return await self.client.wait_for("message", check=check)
	# end of prompt

	'''
	checks if an event is valid
	'''
	def isValidEvent(self, event):
		for i in events:
			print(i.getTitle(), "=", event)
			if (i.getTitle() == event):
				return True
		return False
	#end of isValidEvent()

	'''
	returns the index of an event in events based on the title of the event
	'''
	def getEventIndex(self, event):
		for i in range(len(events)):
			if (events[i].getTitle() == event):
				return i
	#end of getEventIndex()

	'''
	lists an array of events in bots format
	'''
	async def listArray(self, arr):
		count = 1

		for i in arr:
			if int(i.getUserLimit()) == 0:
				await self.sendMessage(f"{count}. {i.getTitle()}: {i.getJoinedUsers()}/INF Joined Users", self.commandsId)
			else:
				await self.sendMessage(f"{count}. {i.getTitle()}: {i.getJoinedUsers()}/{i.getUserLimit()} Joined Users", self.commandsId)

			count += 1
		#end for loop
	#end listArray

	'''
	displays the events the user is an admin of
	'''
	async def displayAdminEvents(self, message, channelId):
		author = message.author
		await self.sendMessage("--- Events you are admin of ---", self.commandsId)
		authorAdminEvents = []

		for i in events:
			if(i.getAuthor() == author):
				authorAdminEvents.append(i)
		# end for loop

		await self.listArray(authorAdminEvents)

		return authorAdminEvents

	'''
	displays events that the user has joined
	'''
	async def displayJoinedEvents(self, message):
		author = message.author
		joinedEvents = []

		for event in events:
			for user in event.getJoinedUserList():
				print("User is a " + str(type(user)))
				if user.name.split("#")[0] == author.name:
					joinedEvents.append(event)
					print(user.name.split("#")[0] + "==" + author.name + ": " + str(user.name.split("#")[0] == author.name))
			# end of innner for loop
		#end of outer for loop

		await self.listArray(joinedEvents)
		
		return joinedEvents 


	""" Bot commands """

	'''
	prompts the user to create a new event
	'''
	async def createEvent(self, message):
		title = await self.prompt("Enter the event title", message)
		game = await self.prompt("Enter the game name", message)
		startTime = await self.prompt("Enter event start time", message)
		userLimit = await self.prompt("Enter user max users (0 = no limit)", message)

		event = Event(title.content, game.content, message.author, startTime.content, 1, userLimit.content)
		await self.sendMessage(event.getNotificationString(), self.commandsId)
		events.append(event)
	# end of createEvent command

	'''
	has the user enter what event they want to join
	will reject the request if the event is full
	'''
	async def joinEvent(self, message):
		await self.sendMessage("!!!Current Active Events!!!", self.commandsId)

		await self.listArray(events)

		author = message.author

		eventToJoin = await self.prompt(f"Enter the event you wish to join", message)

		if self.isValidEvent(eventToJoin.content) == True:
			event = events[self.getEventIndex(eventToJoin.content)]
			joinedUserList = event.getJoinedUserList()

			if author in joinedUserList:
				await self.sendMessage(f"You are already apart of this event", self.commandsId)
			elif int(event.getUserLimit()) > int(event.getJoinedUsers()) or (int(event.getUserLimit()) == 0):
				event.newUserJoined(author)
				await self.sendMessage(f"{author} has joined: {event.getTitle()}", self.commandsId)
			else:
				await self.sendMessage(f"{event.getTitle()} is full", self.commandsId)
		else:
			await self.sendMessage(f"{eventToJoin} is not a valid event", self.commandsId)
	# end of joinEvent

	'''
	deletes an event from the event list
	NOTE: you MUST be an admin to delete an event
	'''
	async def deleteEvent(self, message):
		author = message.content

		authorAdminEvents = await self.displayAdminEvents(message, self.commandsId)
		eventToDelete = await self.prompt(f"Which event would you like to delete?", message)

		if self.isValidEvent(eventToDelete.content) == True:
			event = events[self.getEventIndex(eventToDelete.content)]
			if event in authorAdminEvents:
				events.remove(event)
				await self.sendMessage(f"{event.getTitle()} has been deleted", self.commandsId)
				del event
			else:
				await self.sendMessage(f"You are not admin of {eventToDelete.content}", self.commandsId)
	#end of deleteEvent

	'''
	prompts the user to change the event time
	NOTE: you MUST be an admin to change the event's time
	'''
	async def changeEventTime(self, message):
		adminEvents = await self.displayAdminEvents(message, self.commandsId)

		eventToChangeTime = await self.prompt("Which event would like to change the time for", message)
		if self.isValidEvent(eventToChangeTime.content) == True:
			event = events[self.getEventIndex(eventToChangeTime.content)]
			if event in adminEvents:
				newTime = await self.prompt("What would you like to change the time to", message)
				event.setStartTime(newTime)
			else:
				await self.sendMessage(f"You are not an admin of {eventToChangeTime.content}", self.commandsId)
	# end of changeEventTime code

	'''
	displays all active events in the instance
	'''
	async def events(self, message):
		await self.sendMessage(f"!!!Current Active Events!!!", self.commandsId)
		await self.listArray(events)
	# end of events code

	async def joinedUsers(self, message):
		author = message.author
		await self.events(message)

		eventToSearch = await self.prompt("Event event name to see joined users", message)

		if self.isValidEvent(eventToSearch.content) == True:
			event = events[self.getEventIndex(eventToSearch.content)]
			joinedUserList = event.getJoinedUserList()

			await self.sendMessage(f"{event.getTitle()}", self.commandsId)

			count = 1
			for i in joinedUserList:
				await self.sendMessage(f"{count}. {i}", self.commandsId)
				count += 1
		else:
			await self.sendMessage(f"{event.getTitle()} is invalid event", self.commandsId)
	# end of joinedUsers command codes

	'''
	prompts the user to change the game title of the event
	'''
	async def changeGameTitle(self, message):
		author = message.author
		authorAdminEvents = await self.displayAdminEvents(message, self.commandsId)
		eventGameToChange = await self.prompt("Which event's game title do you wish to change?", message)

		if self.isValidEvent(eventGameToChange.content) == True:
			event = events[self.getEventIndex(eventGameToChange.content)]
			if event in authorAdminEvents:
				newGame = await self.prompt("What do you want to change the game's title to?", message)
				event.setGame(newGame)
				await self.sendMessage(f"Event game set to {event.getGame()}", self.commandsId)
			else:
				await self.sendMessage(f"You are not an admin of {eventGameToChange.content}", self.commandsId)
	# end of changeEventTime

	'''
	prompts the user to change the user limit of the event
	'''
	async def changeUserLimit(self, message):
		author = message.author
		authorAdminEvents = await self.displayAdminEvents(message, self.commandsId)
		eventUserLimitToChange = await self.prompt("Which event's user limit do you wish to chnage?", message)

		if self.isValidEvent(eventUserLimitToChange.content) == True:
			event = events[self.getEventIndex(eventUserLimitToChange.content)]
			if event in authorAdminEvents:
				newUserLimit = await self.prompt("What do you want to change the user limit to?", message)
				event.setUserLimit(newUserLimit.content)
				await self.sendMessage(f"Event user limit set to {event.getUserLimit}", self.commandsId)
			else:
				await self.sendMessage(f"You are not an admin of {eventUserLimitToChange.content}", self.commandsId)
		else:
			await self.sendMessage("Event invalid", self.commandsId)
	# end of changeUserLimit

	'''
	prompts the user for who they want to kick from their event
	NOTE: you MUST be an admin to kick someone
	'''
	async def kick(self, message):
		author = message.author
		authorAdminEvents = await self.displayAdminEvents(message, self.commandsId)
		eventToListUsers = await self.prompt("What event do you want to kick someone from?", message)

		event = None
		if self.isValidEvent(eventToListUsers.content):
			event = events[self.getEventIndex(eventToListUsers.content)]
			if event in authorAdminEvents:
				# listing users
				await self.sendMessage("Users in event", self.commandsId)
				userList = ""
				for usr in event.getJoinedUserList():
					userList += usr.name + "\n"
				# end of for loop

				await self.sendMessage(f"{userList}", self.commandsId)
				userToKick = await self.prompt("What user do you want to kick?", message)

				for usr in event.getJoinedUserList():
					if usr.name == userToKick.content:
						print("kicking " + usr.name + " from " + event.getTitle())
						event.getJoinedUserList().remove(usr)
						event.setJoinedUsers(event.getJoinedUsers() - 1)
						events[self.getEventIndex(eventToListUsers.content)] = event # updating new event infomation
						break
				# end of for loop

				await self.sendMessage("User kicked", self.commandsId)
			else:
				await self.sendMessage("You are not an admin of this event", self.commandsId)
		else:
			await self.sendMessage("Event doesn't exist", self.commandsId)
	#end of kick()	

	'''
	prompts the user to enter the event they want to leave
	'''
	async def leaveEvent(self, message):
		author = message.author
		listOfAuthorEvents = self.displayJoinedEvents(message)
		eventToLeave = self.prompt("Which event do you want to leave", message)

	#end of leaveEvent()

	'''
	displays a help message listing commands
	'''
	async def help(self, message):
		helpMessage = "list of commands\n!createEvent\n!joinedUsers\n!deleteEvent\n!changeEventTime!changeEventGame\n!changeUserLimit\n!events\n!joinEvent\n!leaveEvent\n!kick\n!end\nNote: So commands aren't implemented, if that's the case the bot will throw unreconized command message"
		await self.sendMessage(helpMessage, self.commandsId)
	#end if


bot = EventBot(client)

@client.event
async def on_ready():
	print("Welcome to the bot")
	await bot.sendMessage("use !help for command list", bot.commandsId)
	# for some reason this on is assigned here whenever we try to assign in __init___ it returns None
	bot.messageChannel = bot.client.get_channel(bot.commandsId)

@client.event
async def on_message(message):
	print("USERNAME: " + message.author.name)
	if message.content == "!createEvent":
		await bot.createEvent(message)
	elif message.content == "!joinEvent":
		await bot.joinEvent(message)
	elif message.content == "!deleteEvent":
		await bot.deleteEvent(message)
	elif message.content == "!changeEventTime":
		await bot.changeEventTime(message)
	elif message.content == "!events":
		await bot.events(message)
	elif message.content == "!joinedUsers":
		await bot.joinedUsers(message)
	elif message.content == "!changeGameTitle":
		await bot.changeGameTitle(message)
	elif message.content == "!changeUserLimit":
		await bot.changeUserLimit(message)
	elif message.content == "!kick":
		await bot.kick(message)
	elif message.content == "!myEvents":
		await bot.displayJoinedEvents(message)
	elif message.content == "!leaveEvent":
		await bot.leaveEvent(message)
	elif message.content == "!help":
		await bot.help(message)
	elif message.content.startswith("!"):
		await bot.sendMessage("Unknown command", bot.commandsId)


bot.run()