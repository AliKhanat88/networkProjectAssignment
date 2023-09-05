from abc import ABC, abstractmethod
from collections import defaultdict

class NetworkObject(ABC):
    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def size(self):
        pass

class Member(NetworkObject):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.friendList = []

    def getFriends(self):
        return self.friendList
    
    def addFriend(self, friend):
        self.friendList.append(friend)

    def __str__(self):
        r = f"{self.name} is friends with "
        if self.size() == 0:
            return r + "no one"
        for friend in self.friendList:
            r += f"{friend}, "
        return r[:-2]
    
    def deleteFriend(self, friend):
        self.friendList.remove(friend)

    def size(self):
        return len(self.friendList)

class Network(NetworkObject):
    def __init__(self):
        super().__init__()
        self.network = {}

    def addMember(self, member):
        self.network[member] = Member(member)

    def addFriend(self, member, friend):
        self.network[member].addFriend(friend) 

    def size(self):
        return len(self.network)
    
    def deleteMember(self, member):
        for friend in self.network[member].getFriends():
            self.network[friend].deleteFriend(member)
        del(self.network[member])

    def getGroups(self):
        groups_sizes = [0]*5
        visited = defaultdict(lambda: False)
        polygons = 0
        for member in self.network:
            if visited[member] == False:
                queue = [member]
                gz = 0
                is_polygon = True
                while len(queue) != 0:
                    cur = queue.pop(0)
                    if visited[cur] == True:
                        continue
                    visited[cur] = True
                    neighbors = self.network[cur].getFriends()
                    if self.network[cur].size() != 3:
                        is_polygon = False
                    for neighbor in neighbors:
                        queue.append(neighbor)
                    gz += 1
                # print(gz)
                if gz >= 5:
                    groups_sizes[4] += 1
                else:
                    groups_sizes[gz-1] += 1

                if is_polygon and gz == 4:
                    polygons += 1
        return groups_sizes, polygons
    

    def printGroupSize(self):
        groups_sizes, _ = self.getGroups() 
        print("The size of  friend groups:")
        for i, size in enumerate(groups_sizes):
            print(f"Number of  groups with {i+1} members: {size}")

    def printShape(self):
        groups_sizes, polygons = self.getGroups()
        stars = self.getStars()
        print("Friend group network shapes:")
        print(f"{groups_sizes[0]} singleton")
        print(f"{groups_sizes[1]} pair")
        print(f"{groups_sizes[2]} triangle")
        print(f"{polygons} polygon")
        print(f"{stars} star") 
    

    def getStars(self):
        stars = 0
        for member in self.network:
            if self.network[member].size() == 4:
                is_star = True
                for friend in self.network[member].getFriends():
                    if self.network[friend].size() != 1:
                        is_star = False
                        break
                if is_star == True:
                    stars += 1

        return stars

    def __str__(self):
        r = ""
        if self.size() == 0:
            return ""
        for member in self.network:
            r += self.network[member].__str__() + "\n"
        return r[:-1]
    
    def averageFriends(self):
        sumi = 0
        for member in self.network:
            sumi += self.network[member].size()

        return sumi / self.size()
    
    def maxFriends(self):
        maxi = 0
        name = "No One"
        for member in self.network:
            if self.network[member].size() >= maxi:
                maxi = self.network[member].size()
                name = member

        return name


class MakeNetwork:
    def __init__(self, filename):
        self.filename = filename
        
    def make(self):
        file = open(self.filename, "r")
        n = int(file.readline())
        line = file.readline()
        nw = Network()
        while line != "":
            line = line.rstrip().split()
            if len(line) == 1:
                nw.addMember(line[0])
            else:
                f1, f2 = line
                try:
                    nw.addFriend(f1, f2)
                except:
                    nw.addMember(f1)
                    nw.addFriend(f1, f2)

                try:
                    nw.addFriend(f2, f1)
                except:
                    nw.addMember(f2)
                    nw.addFriend(f2, f1)
            line = file.readline()

        if nw.size() != n:
            raise Exception("Member defined in the file are not equal to the actual members")
        
        return nw
 


        


def main():
    while True:
        fileName = input("Input valid file name or type 'done': ")
        if fileName == "done":
            exit()
        else:
            try:
                file = open(fileName, "r")
                file.close()
            except:
                continue
            break

    makeNet = MakeNetwork(fileName)
    network = makeNet.make()
    print("Printing network: ")
    print(network)
    network.deleteMember("Bob")
    print("Printing network after deleting Bob: ")
    print(network)
    print("Printing size of the groups")
    network.printGroupSize()
    print("Printing Network shapes")
    network.printShape()
    print(f"Average number of friends : {network.averageFriends()}")
    print(f"Member with highest friends: {network.maxFriends()}")


main()
    





