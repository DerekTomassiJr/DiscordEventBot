class Event:
    def __init__(self, title, game, author, startTime, joinedUsers, userLimit):
        self.title = title
        self.game = game
        self.author = author
        self.startTime = startTime
        self.joinedUsers = joinedUsers
        self.userLimit = userLimit
        self.joinedUserList = [self.author]
    #end of constructor

    """Getters and setters for all variables"""
    def getTitle(self):
        return self.title
    #end of getTitle()

    def setTitle(self, newTitle):
        self.title = newTitle
    #end of setTitle

    def getGame(self):
        return self.game
    #end of getGame()

    def setGame(self, newGame):
        self.game = newGame;
    #end of setGame()

    def getAuthor(self):
        return self.author
    #end of getAuthor()

    def setAuthor(self, newAuthor):
        self.author = newAuthor

    def getStartTime(self):
        return self.startTime
    #end of getStartTime()

    def setStartTime(self, newTime):
        self.startTime = newTime
    #end of setStartTime

    def getJoinedUsers(self):
        return self.joinedUsers
    #end of getJoinedUsers()

    def setJoinedUsers(self, newJoinedUsers):
        self.joinedUsers = newJoinedUsers
    #end of setJoinedUsers

    def getUserLimit(self):
        return self.userLimit
    #end of getUserLimit()

    def setUserLimit(self, newUserLimit):
        self.userLimit = newUserLimit
    #end of setUserLimit()

    def getJoinedUserList(self):
        return self.joinedUserList
    #end of getJoinedUserList()

    def setJoinedUserList(self, newJoinedUsers):
        self.joinedUserList = newJoinedUsers
    #end of setJoinedUserList()

    def newUserJoined(self, user):
        self.joinedUsers += 1
        self.joinedUserList.append(user)
    #end newUserJoined()

    def getNotificationString(self):
    	return f"""
    	-----------------------------
    	!!!New event created!!!
    	Event: {self.title}
    	Made by: {self.author}
    	Game: {self.game}
    	Starts at: {self.startTime}
    	User limit: {self.userLimit}
    	------------------------------"""
