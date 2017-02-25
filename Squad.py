import math
import random

class Squad:

    squadLst = []
    INDICATOR_RADIUS = 1
    JOIN_DISTANCE = 100
    MAX_SIZE = 5

    def __init__(self):
        self.members = []
        self.location = [0, 0]
        self.target = [0, 0]
        self.size = 5
        self.color = Squad.gen_hex_colour_code()
        self.heading = 0

    @staticmethod
    def gen_hex_colour_code():
        return "#" + ''.join([random.choice('0123456789ABCDEF') for x in range(6)])

    def distance(self, other):
        distSquared = (other.location[0] - self.location[0]) ** 2 + (other.location[1] - self.location[1]) ** 2
        dist = math.sqrt(distSquared)
        return dist

    @staticmethod
    def distanceWithCoord(x1, y1, x2, y2):
        distSquared = (x1 - x2) ** 2 + (y1 - y2) ** 2
        dist = math.sqrt(distSquared)
        return dist

    @staticmethod
    def join(individual):
        '''
        Add member to members only if not exist in any squad
        :param individual: target
        :return:
        '''
        joined = False
        joinedSquad = None
        # Check if individual joined any squad
        for squad in Squad.squadLst:
            if(Squad.checkMemberInSquad(squad, individual)):
                joined = True
                joinedSquad = squad

        # Find and join squad if possible
        for squad in Squad.squadLst:
            center = squad.center()
            #print(individual.name)
            #print(center, " ", individual.typeName, " ", squad.members[0].typeName)
            dist = Squad.distanceWithCoord(center[0], center[1],
                                           individual.location[0], individual.location[1])
            if(dist <= Squad.JOIN_DISTANCE and
               individual.typeName == squad.members[0].typeName):
                if(not joined):
                    squad.addMember(individual)
                    joined = True
                    joinedSquad = squad
                elif(len(squad.members) < Squad.MAX_SIZE):
                    Squad.leave(joinedSquad, individual)
                    squad.addMember(individual)


        if(not joined):
            # Create new squad
            newSquad = Squad()
            newSquad.addMember(individual)
            Squad.squadLst.append(newSquad)

    @staticmethod
    def leave(squad, individual):
        '''
        Remove member from members if target exist in current squad
        :param individual: target
        :return:
        '''
        if(Squad.checkMemberInSquad(squad, individual)):
            squad.removeMember(individual)
            # Delete empty squad
            if(len(squad.members) == 0):
                Squad.squadLst.remove(squad)
        else:
            # TODO: debug this error
            print("leaving squad error")
            print(squad.members)
            print(individual)
            print("\n")

    @staticmethod
    def checkMemberInSquad(squad, individual):
        '''
        Check whether member is in squad
        :param individual: target
        :return: bool
        '''

        for member in squad.members:
            if (individual.name == member.name and
                        individual.typeName == member.typeName):
                return True
        return False

    def addMember(self, individual):
        '''
        Add member to members
        :param individual: target
        :return:
        '''
        if(self in Squad.squadLst):
            Squad.squadLst.remove(self)
        # add and update squadLst
        if(not(individual in self.members)):
            self.members.append(individual)
        self.update()
        Squad.squadLst.append(self)

    def removeMember(self, individual):
        '''
        Remove member from members
        :param individual: target
        :return:
        '''
        if(self in Squad.squadLst):
            Squad.squadLst.remove(self)
        if(individual in self.members):
            # remove and update squadLst
            self.members.remove(individual)
        self.update()
        Squad.squadLst.append(self)

    def update(self):
        '''
        Update squad if target died
        :param individual:
        :return:
        '''
        for individual in self.members:
            if(not individual.alive):
                self.removeMember(individual)
        if(len(self.members) == 0 and self in Squad.squadLst):
            Squad.squadLst.remove(self)
            return
        if(len(self.members) == 0):
            return
        self.location = self.center()
        self.target = self.center()

    def center(self):
        x = 0
        y = 0
        for member in self.members:
            x += member.location[0]
            y += member.location[1]
        x /= len(self.members)
        y /= len(self.members)
        return [x, y]
