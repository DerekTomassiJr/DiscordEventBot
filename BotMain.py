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

client = discord.Client()
events = []

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
            await message.channel.send(f"""!!!Current Active Events!!!""")

            count = 1
            for i in events:
                if (int(i.getUserLimit()) == 0):
                    await message.channel.send(f"""{count}. {i.getTitle()}: {i.getJoinedUsers()}/INF Joined Users""")
                else:
                    await message.channel.send(
                        f"""{count}. {i.getTitle()}: {i.getJoinedUsers()}/{i.getUserLimit()} Joined Users""")
                count += 1
            #end for loop
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
                elif (int(event.getUserLimit()) > int(event.getJoinedUsers()) or (int(event.getUserLimit()) == 0)):
                    event.newUserJoined(author)
                    await message.channel.send(f"""{author} has joined: {event.getTitle()}""")
                else:
                    await message.channel.send(f"""{event.getTitle()} is full""")
            else:
                await message.channel.send(f"""{eventToJoin} is not a valid event""")
        #end of joinEvent command code
        elif (message.content == "!joinedUsers"):
            author = message.author
            await message.channel.send(f"""Enter event name to see joined users""")
            await message.channel.send(f"""!!!Current Active Events!!!""")

            count = 1
            for i in events:
                if (int(i.getUserLimit()) == 0):
                    await message.channel.send(f"""{count}. {i.getTitle()}: {i.getJoinedUsers()}/INF Joined Users""")
                else:
                    await message.channel.send(f"""{count}. {i.getTitle()}: {i.getJoinedUsers()}/{i.getUserLimit()} Joined Users""")
                count += 1

            # end for loop

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
                await message.channel.send(f"""{event.getTitle()} is not a valid event""")
        #end of joinedUsers command code
        elif (message.content == "!events"):
            await message.channel.send(f"""!!!Current Active Events!!!""")

            count = 1
            for i in events:
                if (int(i.getUserLimit()) == 0):
                    await message.channel.send(f"""{count}. {i.getTitle()}: {i.getJoinedUsers()}/INF Joined Users""")
                else:
                    await message.channel.send(f"""{count}. {i.getTitle()}: {i.getJoinedUsers()}/{i.getUserLimit()} Joined Users""")
                count += 1
        #end of events command code
        elif (message.content == "!leaveEvent"):
            author = message.author

            #determining which events the author is apart of
            authorEvents = []
            for i in events:
                joinedUserList = i.getJoinedUserList()
                if (author in joinedUserList):
                    authorEvents.append(i)
            #end for loop

            await message.channel.send(f"""Which event would you like to leave""")
            await message.channel.send(f"""---Your Current Active Joined Events---""")

            count = 1
            for i in authorEvents:
                if (int(i.getUserLimit()) == 0):
                    await message.channel.send(f"""{count}. {i.getTitle()}: {i.getJoinedUsers()}/INF Joined Users""")
                else:
                    await message.channel.send(f"""{count}. {i.getTitle()}: {i.getJoinedUsers()}/{i.getUserLimit()} Joined Users""")
                count += 1
            #end for loop

            def check(m):
                return m.content and m.author == author

            eventToLeave = await client.wait_for('message', check=check)
            if (isValidEvent(eventToLeave.content) == True):
                event = events[getEventIndex(eventToLeave.content)]
                if (event.getJoinedUsers() > 1):
                    event.deleteUser(author)

                    joinedUserList = event.getJoinedUserList()
                    event.setAuthor(joinedUserList[0])
                else:
                    events.remove(event)
                    del event

                await message.channel.send(f"""You have been successfully removed from: {event.getTitle()}""")
            else:
                await message.channel.send(f"""{eventToLeave} is not a valid event you are apart of""")
        #end of deleteEvent command code
        elif (message.content == "!deleteEvent"):
            author = message.author

            authorAdminEvents = []
            for i in events:
                if (i.getAuthor() == author):
                    authorAdminEvents.append(i)
            #end for loop

            await message.channel.send(f"""Which event would you like to delete""")
            await message.channel.send(f"""---Events you are admin of---""")

            count = 1
            for i in authorAdminEvents:
                if (int(i.getUserLimit()) == 0):
                    await message.channel.send(f"""{count}. {i.getTitle()}: {i.getJoinedUsers()}/INF Joined Users""")
                else:
                    await message.channel.send(f"""{count}. {i.getTitle()}: {i.getJoinedUsers()}/{i.getUserLimit()} Joined Users""")
                count + 1
            #end for loop

            def check(m):
                return m.content and m.author == author

            eventToDelete = await client.wait_for('message', check=check)
            if (isValidEvent(eventToDelete.content) == True):
                event = events[getEventIndex(eventToDelete.content)]
                if (event in authorAdminEvents):
                    events.remove(event)
                    await message.channel.send(f"""{event.getTitle()} has been deleted""")

                    del event
                else:
                    await message.channel.send(f"""You are not admin of {eventToDelete.content}""")
        #end of deleteEvent command code
        elif (message.content == "!changeEventTime"):
            author = message.author

            await message.channel.send(f"""Which event would you like to change the time for""")
            await message.channel.send(f"""---Events you are admin of---""")

            authorAdminEvents = []
            for i in events:
                if (i.getAuthor() == author):
                    authorAdminEvents.append(i)
            #end for loop

            count = 1
            for i in authorAdminEvents:
                if (int(i.getUserLimit()) == 0):
                    await message.channel.send(f"""{count}. {i.getTitle()}: {i.getJoinedUsers()}/INF Joined Users""")
                else:
                    await message.channel.send(f"""{count}. {i.getTitle()}: {i.getJoinedUsers()}/{i.getUserLimit()} Joined Users""")
                count + 1
            #end for loop

            def check(m):
                return m.content and m.author == author

            eventToChangeTime = await client.wait_for('message', check=check)
            if (isValidEvent(eventToChangeTime.content) == True):
                event = events[getEventIndex(eventToChangeTime.content)]
                if (event in authorAdminEvents):
                    await message.channel.send(f"""What would you like to change the time to""")

                    newTime = client.wait_for('message', check=check)
                    event.setStartTime(newTime)
                else:
                    await message.channel.send(f"""You are not an admin of {eventToChangeTime.content}""")
        #end of changeEventTime command code



client.run("NTU0ODY5MDU2MjI2ODUyODk4.D2i9aA.8Z0-bvrmOmsT8de3LKylkQcOOnY")
