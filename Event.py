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

    """Getters for all variables"""
    def getTitle(self):
        return self.title
    #end of getTitle()

    def getGame(self):
        return self.game
    #end of getGame()

    def getAuthor(self):
        return self.author
    #end of getAuthor()

    def getStartTime(self):
        return self.startTime
    #end of getStartTime()

    def getJoinedUsers(self):
        return self.joinedUsers
    #end of getJoinedUsers()

    def getUserLimit(self):
        return self.userLimit
    #end of getUserLimit()

    def getJoinedUserList(self):
        return self.joinedUserList
    #end of getJoinedUserList()

    def newUserJoined(self, user):
        self.joinedUsers += 1
        self.joinedUserList.append(user)
    #end newUserJoined()
