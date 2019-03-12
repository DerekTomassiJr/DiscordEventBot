"""
List of Commands for the Bot
!createEvent \/
!joinedUsers \/
!deleteEvent
!changeEventTime
!changeEventGame
!changeUserLimit
!events
!joinEvent \/
!leaveEvent
!kick
!end
"""
import discord
from Event import Event

client = discord.Client()
events = []

def isValidEvent(event):
    isValid = False
    for i in events:
        if (i.getTitle() == event):
            isValid = True
    return isValid
#end of isValidEvent()

def getEventIndex(event):
    for i in range(len(events)):
        if (events[i].getTitle() == event):
            return i
#end of getEventIndex()

@client.event
async def on_message(message):
    id = client.get_guild(554882293194555395)
    channels = ["commands"]

    if (str(message.channel) in channels):
        if (message.content == "!createEvent"):
            author = message.author
            await message.channel.send(f"""Enter the event title """)

            def check(m):
                return m.content and m.author == author

            title = await client.wait_for('message', check=check)

            await message.channel.send(f"""Enter the game name """)
            game = await client.wait_for('message', check=check)

            await message.channel.send(f"""Enter Event Start Time """)
            startTime = await client.wait_for('message', check=check)

            await message.channel.send(f"""Enter Max Amount of Users (0 = No Limit)""")
            userLimit = await client.wait_for('message', check=check)

            await message.channel.send(f"""@everyone""")
            await message.channel.send(f"""!!!New Event Created!!!""")
            await message.channel.send(f"""Event: {title.content}""")
            await message.channel.send(f"""Made By: {author}""")
            await message.channel.send(f"""Game: {game.content}""")
            await message.channel.send(f"""Starts At: {startTime.content}""")
            await message.channel.send(f"""User Limit: {userLimit.content}""")

            event = Event(title.content, game.content, author, startTime.content, 1, userLimit.content)
            events.append(event)
        #end of create event command code
        elif (message.content == "!joinEvent"):
            author = message.author
            await message.channel.send(f"""Enter the event you wish to join""")

            def check(m):
                return m.content and m.author == author

            eventToJoin = await client.wait_for('message', check=check)
            #checking if the user input is a valid event
            if (isValidEvent(eventToJoin.content) == True):
                event = events[getEventIndex(eventToJoin.content)]
                joinedUserList = event.getJoinedUserList()

                if (author in joinedUserList):
                    await message.channel.send(f"""You are already apart of this event""")
                elif (int(event.getUserLimit()) > int(event.getJoinedUsers())):
                    event.newUserJoined(author)
                    await message.channel.send(f"""{author} has joined {event.getTitle()}""")
                else:
                    await message.channel.send(f"""{event.getTitle()} is full""")
            else:
                await message.channel.send(f"""That is not a valid event""")
        #end of joinEvent command code
        elif (message.content == "!joinedUsers"):
            author = message.author
            await message.channel.send(f"""Enter event name to see joined users""")

            def check(m):
                return m.content and m.author == author

            eventToSearch = await client.wait_for('message', check=check)
            #checking if the event is a valid event
            if (isValidEvent(eventToSearch.content) == True):
                event = events[getEventIndex(eventToSearch.content)]
                joinedUserList = event.getJoinedUserList()

                await message.channel.send(f"""{event.getTitle()}""")
                count = 1
                for i in joinedUserList:
                    await message.channel.send(f"""{count}. {i}""")
                    count += 1
            else:
                await message.channel.send(f"""That is not a valid event""")
        #end of joinedUsers command code




client.run("NTU0ODY5MDU2MjI2ODUyODk4.D2i9aA.8Z0-bvrmOmsT8de3LKylkQcOOnY")