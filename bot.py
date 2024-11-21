import discord
from botutils import Clock
from botutils import Event
from botutils import Date
from botutils import BotTimer

client = discord.Client()
events = []

class EventBot:
    client = None
    clock = Clock()
    generalId = None
    commandsId = None
    eventCommandsId = None
    messageChannel = None
    botToken = None
    lastTimeCheck = None
    daysEvents = []
    updated = False

    def __init__(self, client):
        self.client = client
        self.generalId = None
        self.commandsId = None
        self.eventCommandsId = None
        self.botToken = "put token here"
    
    """ Initializes the bot in the server """
    def run(self):
        self.client.run(self.botToken)
    #end of run
    
    """ Sends a message to a channel with the given channel ID """
    async def sendMessage(self, message, channelID):
        print(f"Sending: {message}")
        channel = self.client.get_channel(channelID)
        await channel.send(f"{message}")
    # end sendMessage

    """ prompts the user for a message and only takes messages from the user that wrote the command """
    async def prompt(self, prompt, message):
        author = message.author
        
        # checks to make sure the response is coming from the same user
        def check(m):
            return m.content and m.author == author
        
        await self.messageChannel.send(f"{prompt}")
        return await self.client.wait_for("message", check=check)
    # end prompt

    """ checks if an event is valid """
    def isValidEvent(self, event, arr):
        for i in arr:
            print(f"{i.getTitle()} = {event.content}")
            if(i.getTitle() == event.content):
                return True
            
        return False
    # end isValidEvent

    """ returns the index of an event in events based on the title of the event """
    def getEventIndex(self, event):
        for i in range(len(events)):
            if(events[i].getTitle() == event):
                return i
    # end getEventIndex

    """ lists an array of events in boys format """
    async def listArray(self, arr):
        count = 1
        for i in arr:
            maxUsers = None
            if (i.getUserLimit()) <= 0:
                maxUsers = "INF"
            else:
                maxUsers = i.getUserLimit();
            
            await self.sendMessage(f"{count}. {i.getTitle()}: {len(i.getJoinedUserList())}/{maxUsers} Joined Users", self.commandsId)
            count += 1;
        # end for
    # end listArray

    """ displays the events the user is admin of """
    async def displayAdminEvents(self, message):
        author = message.author
        await self.sendMessage("--- Events you are admin of ---", self.commandsId)
        authorAdminEvents = []

        for i in events:
            if(i.getAuthor() == author):
                authorAdminEvents.append(i)
        # end for

        await self.listArray(authorAdminEvents)
        return authorAdminEvents
    # end displayAdminEvents

    """ displays the events that the user is a part of """
    async def displayJoinedEvents(self, message):
        author = message.author
        joinedEvents = []

        for event in events:
            for user in event.getJoinedUserList():
                if user.name.split("#")[0] == author.name:
                    joinedEvents.append(event)
                    print(user.name.split("#")[0] + "==" + author.name + ": " + str(user.name.split("#")[0] == author.name))
            # end inner for
        # end for

        await self.listArray(joinedEvents)
    # end displayJoinedEvents

    """ list the joined users given input """
    async def listJoinedUsers(self, message):
        await self.listArray(events)
        eventToList = await self.prompt("Enter event to list", message)

        if self.isValidEvent(eventToList, events):
            await self.sendMessage(f"Users in {eventToList.content}", self.commandsId)
            userString = ""
            for user in events[self.getEventIndex(eventToList.content)].getJoinedUserList():
                userString += user.name + " | "
            # end for

            await self.sendMessage(f"{userString}", self.commandsId)
        else:
            await self.sendMessage("Bad event", self.commandsId)
    # end listJoinedUsers
            

    """ removes the first event with the events name from the array """
    async def remove(self, eventName):
        for event in events:
            if(event.getTitle() == eventName):
                events.remove(event)
                await self.sendMessage(f"Event \"{event.getTitle()}\" ended", self.commandsId)
                self.updated = False
                return None
        await self.sendMessage("Nothing removed", self.commandsId)
        # end for
    # end remove

    """ Bot Commands """
    async def createEvent(self, message):
        title = await self.prompt("Enter the event title", message)

        # checking to see if an event with that title already exists
        titleTaken = False
        for event in events:
            if title.content == event.getTitle() :
                titleTaken = True
                break
        
        if titleTaken:
            await self.sendMessage("The title you took is already in use", self.commandsId)
            return None

        # if the title isn't taken we can continue to create the event
        game = await self.prompt ("Enter the game's name", message)

        # getting the date and splitting it up into data that the object can read
        date = await self.prompt("Enter date in MM/DD/YYYY format", message)

        dateSplit = date.content.split("/")
        if len(dateSplit) == 3:
            date = Date(dateSplit[0], dateSplit[1], dateSplit[2])
        else:
            await self.sendMessage("Invalid date format", self.commandsId)
            return None

        if not(date.isValid()):
            await self.sendMessage("Invalid date (possibly already passed?)", self.commandsId)
            return None
        

        startTime = await self.prompt("Enter event's start time", message)
        userLimit = await self. prompt("Enter max users (0 = no limit)", message)

        event = Event(title.content, game.content, message.author, date, startTime.content, 1, int(userLimit.content))
        await self.sendMessage(event.toString(), self.commandsId)
        events.append(event)
        self.updated = False
    # end createEvent

    """ ends the event entered by the user """
    async def endEvent(self, message):
        authorAdminEvents = await self.displayAdminEvents(message)

        if len(authorAdminEvents) == 0 or authorAdminEvents == None:
            await self.sendMessage("You are not the admin of any events", self.commandsId)
            return None

        eventToEnd = await self.prompt("Enter the title of the event you want to end: ", message)

        if(self.isValidEvent(eventToEnd, authorAdminEvents)):
            await self.remove(eventToEnd.content)
        else:
            await self.sendMessage("Bad event", self.commandsId)
    # end endEvent

    """ prints out the detail about an event """
    async def seeEvents(self, message):
        await self.listArray(events)
        eventToView = await self.prompt("Enter event to view", message)

        if self.isValidEvent(eventToView, events):
            eventIndex = self.getEventIndex(eventToView.content)
            await self.sendMessage(events[eventIndex].toString(), self.commandsId)
        else:
            await self.sendMessage("Event is invalid", self.commandsId)

    
    """ List Admin Events """
    async def myAdminEvents(self, message):
        await self.displayAdminEvents(message)
    
    """ List all of the users events"""
    async def displayMyEvents(self, message):
        await self.displayJoinedEvents(message)

    """ changes variables of events """
    async def change(self, message, var):
        authorAdminEvents = await self.displayAdminEvents(message)
        
        if len(authorAdminEvents) == 0 or authorAdminEvents == None:
            await self.sendMessage("You're are not the admin of any events", self.commandsId)
            return None
        
        eventToEdit = await self.prompt("Enter the title of the event you want to edit: ", message)

        if self.isValidEvent(eventToEdit, authorAdminEvents):
            newValue = await self.prompt("Enter new value", message)
            oldEventIndex = self.getEventIndex(eventToEdit.content)
            getFunction = None
            setFunction = None

            if var == "game":
                getFunction = events[oldEventIndex].getGame
                setFunction = events[oldEventIndex].setGame
            elif var == "start_time":
                getFunction = events[oldEventIndex].getStartTime
                setFunction = events[oldEventIndex].setStartTime
            elif var == "user_limit":
                getFunction = events[oldEventIndex].getUserLimit
                setFunction = events[oldEventIndex].setUserLimit
            else:
                await self.sendMessage("Sorry, it looks like I've run into an unexpected error.")
                return None

            setFunction(newValue.content)
            await self.sendMessage(f"Value changed to {getFunction()}", self.commandsId)

        else:
            await self.sendMessage("Bad event", self.commandsId)
    # end change

    async def joinEvent(self, message):
        await self.listArray(events)
        eventToJoin = await self.prompt("Enter event you want to join", message)
        
        if self.isValidEvent(eventToJoin, events):
            event = events[self.getEventIndex(eventToJoin.content)]
            
            if event.getJoinedUsers() >= event.getUserLimit() and not(event.getUserLimit() == 0) :
                await self.sendMessage("Event full", self.commandsId)
            elif(message.author in event.getJoinedUserList()):
                await self.sendMessage("You are already a part of this event", self.commandsId)
            else:
                event.append(message.author)
                event.setJoinedUsers(event.getJoinedUsers() + 1)
                await self.sendMessage(f"User {message.author.name} joined {event.getTitle()}", self.commandsId)
        else:
            await self.sendMessage("Bad event", self.commandsId)
    # end joinEvent

    async def leaveEvent(self, message):
        await self.listArray(events)
        eventToLeave = await self.prompt("Enter event you want to leave", message)

        if self.isValidEvent(eventToLeave, events):
            event = events[self.getEventIndex(eventToLeave.content)]
            if message.author in event.getJoinedUserList():
               event.remove(message.author)
               await self.sendMessage("You were successfully removed!", self.commandsId)
            else:
                await self.sendMessage("You are not in this event", self.commandsId)
        else:
            await self.sendMessage("Bad event", self.commandsId)  
    # end leaveEvent            
    
    """ allows the admin to kick a user from an event """
    async def kick(self, message):
        adminEvents = await self.displayAdminEvents(message)
        eventToView = await self.prompt("Enter event ", message)

        if(self.isValidEvent(eventToView, adminEvents)):
            event = events[self.getEventIndex(eventToView.content)]

            userString = ""
            for user in events[self.getEventIndex(eventToView.content)].getJoinedUserList():
                userString += user.name + " | "
            # end for

            await self.sendMessage(f"{userString}", self.commandsId)

            toKick = await self.prompt("Who do you want to kick ", message)

            if(toKick.content in event.getJoinedUserNameList()):
                event.remove(event.getUserByName(toKick.content))
                await self.sendMessage("User kicked", self.commandsId)
            else:
                await self.sendMessage(f"\"{toKick.content}\" is not a user in this event", self.commandsId)
        else:
            await self.sendMessage("Bad Event", self.commandsId)
    
    async def tick(self):
        currentTime = Clock()
        print(f"Tick -> {currentTime.getHour()}:{currentTime.getMinute()}:{currentTime.getSecond()}")
        # updating events
        if not(self.updated):
            print("Updating todays list")
            for event in events:
                print("Event Name: " + event.getTitle())
                print(f"comparison {event.getDate().getFormattedDate()} == {currentTime.date()}")
                if event.getDate().getFormattedDate() == currentTime.date():
                    print("running")
                    self.daysEvents.append(event)
            self.updated = True
            print("set updated to true")
        
        # checking through the days events
        for event in self.daysEvents:
            if event.getStartTime() == str(currentTime.getHour()) + str(currentTime.getMinute()):
                await self.sendMessage(f"Event \"{event.getTitle()}\" is starting", self.commandsId)
                events.remove(event)
                self.daysEvents.remove(event)
        
        timer = BotTimer(1, self.tick)


bot = EventBot(client)
waitTime = 10 - (bot.clock.getSecond() % 10)
botTimer = BotTimer(waitTime, bot.tick)
    

@client.event
async def on_ready():
    print(f"Starting Discord Event Bot on {bot.clock.date()}")
    await bot.sendMessage("use !help for command list", bot.commandsId)
    
    # for some reason this one is assgined here, whenever we try to assign it in __init__ it returns None
    bot.messageChannel = bot.client.get_channel(bot.commandsId)
# end on_ready

@client.event
async def on_message(message):
    if message.content == "!createEvent":
        await bot.createEvent(message)
    elif message.content == "!endEvent":
        await bot.endEvent(message)
    elif message.content == "!deleteEvent":
        await bot.endEvent(message)
    elif message.content == "!joinEvent":
        await bot.joinEvent(message)
    elif message.content == "!leaveEvent":
        await bot.leaveEvent(message)
    elif message.content == "!kick":
        await bot.kick(message)
    elif message.content == "!displayAdminEvents":
        await bot.displayAdminEvents(message)
    elif message.content == "!displayMyEvents":
        await bot.displayMyEvents(message)
    elif message.content == "!listJoinedUsers":
        await bot.listJoinedUsers(message)
    elif message.content == "!seeEvents":
        await bot.seeEvents(message)
    elif message.content == "!changeGame":
        await bot.change(message, "game")
    elif message.content == "!changeStartTime":
        await bot.change(message, "start_time")
    elif message.content == "!changeUserLimit":
        await bot.change(message, "user_limit")
    
# end on_message

bot.run()
