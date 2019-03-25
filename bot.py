"""
List of Commands for the Bot
!createEvent \/
!joinedUsers \/
!deleteEvent
!changeEventTime
!changeEventGame
!changeUserLimit
!events \/
!joinEvent \/
!leaveEvent \/
!kick
!end
"""
import discord
from Event import Event

# global variables
client = discord.Client()
events = []

class EventBot:
	client = None

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
		self.commandsId = 554890894118223882
		self.eventCommandsId = 555094463907758090
		self.botToken = "NTU0ODY5MDU2MjI2ODUyODk4.D2i9aA.8Z0-bvrmOmsT8de3LKylkQcOOnY"
		return None
	#end of __init__

	# causes the bot to run on the server
	def run(self):
		self.client.run(self.botToken)
	# end of run


	""" Bot utilities """
	# function that has the bot do something so we can test to see if the bot picked up the command
	async def testMessage(self, message):
		await self.sendMessage(message, generalId)
	# end of testMessage

	async def sendMessage(self, message, channelID):
		print("Sending message: " + message)
		channel = self.client.get_channel(channelID)
		await channel.send(f"{message}")
	# end of sendMessage

	async def prompt(self, prompt, message):
		author = message.author

		def check(m):
			return m.content and m.author == author

		await self.messageChannel.send(f"{prompt}")
		return await self.client.wait_for("message", check=check)
	# end of prompt

	def isValidEvent(event):
		for i in events:
			print(i.getTitle(), "=", event)
			if (i.getTitle() == event):
				return True
		return False
	#end of isValidEvent()

	def getEventIndex(event):
		for i in range(len(events)):
			if (events[i].getTitle() == event):
				return i
	#end of getEventIndex()

	""" Bot commands """
	async def createEvent(self, message):
		title = await self.prompt("Enter the event title", message)
		game = await self.prompt("Enter the game name", message)
		startTime = await self.prompt("Enter event start time", message)
		userLimit = await self.prompt("Enter user max users (0 = no limit)", message)

		event = Event(title.content, game.content, message.author, startTime.content, 1, userLimit.content)
		await self.sendMessage(event.getNotificationString(), self.commandsId)
		events.append(event)
	# end of createEvent command

	async def joinEvent(self, message):
		await self.sendMessage("Read message", self.generalId)



bot = EventBot(client)

@client.event
async def on_ready():
	print("Welcome to the bot")

	# for some reason this on is assigned here whenever we try to assign in __init___ it returns None
	bot.messageChannel = bot.client.get_channel(bot.commandsId)

@client.event
async def on_message(message):
	if message.content == "!createEvent":
		await bot.createEvent(message)
	elif message.content == "!joinEvent":
		await bot.joinEvent(message)



bot.run()
