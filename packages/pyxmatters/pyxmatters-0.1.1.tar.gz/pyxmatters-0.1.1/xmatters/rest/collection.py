# standard python modules
import logging
import threading
import math

# import all local modules from the rest package
from . import *

class xMattersCollectionThread(object):

    # constructor
    def __init__(self, request):
        self.log = logging.getLogger(__name__)
        self.request = request

    def createCollection(self, data, max_threads, function):
        bucketSize = int(math.ceil(float(len(data)) / float(max_threads)))
        threads = []
        for n in range(max_threads):
            slice = data[n * int(bucketSize): (n + 1) * int(bucketSize)]
            if len(slice) > 0:
                process = threading.Thread(target=function, args=(n, slice, ))
                process.start()
                threads.append(process)

        # Join all threads before proceeding
        for process in threads:
            process.join()

        return process

class xMattersCollection(xMattersCollectionThread):

    # constructor
    def __init__(self, *args, **kwargs):
        super(xMattersCollection, self).__init__(*args, **kwargs)
        self.succeed = []
        self.fail = []

    # def to Create Groups
    def createGroupsCollection(self, data, max_threads):
        del self.succeed[:]  # first clear the list from previous process
        del self.fail[:]

        process = self.createCollection(data, max_threads, self.createGroups)
        print('Returning List of Users Created: ' + str({'succeed': self.succeed, 'fail': self.fail}))
        return {'succeed': self.succeed, 'fail': self.fail}

    def createGroups(self, thread, data):
        xmGroup = xMattersGroup(self.request)
        for x in range(len(data)):
            self.log.debug('Thread number: ' + str(thread) + ' Creating Group: ' + data[x]['targetName'])
            response = xmGroup.createGroup(data[x])
            if (response):
                self.succeed.append(data[x]['targetName'])
            else:
                self.fail.append(data[x]['targetName'])

    # def to add Members
    def addMemberToShiftCollection(self, data, max_threads):
        del self.succeed[:]  # first clear the list from previous process
        del self.fail[:]

        process = self.createCollection(data, max_threads, self.addMembersToShift)
        print('Returning List: ' + str({'succeed': self.succeed, 'fail': self.fail}))
        return {'succeed': self.succeed, 'fail': self.fail}

    def addMembersToShift(self, thread, data):
        xmShift = xMattersShift(self.request)
        for x in range(len(data)):
            self.log.debug('Thread number: ' + str(thread) + ' Adding Member: ' + data[x]['member'] + ' to Shift: '+data[x]['shift']+' in Group: ' + data[x]['name'])
            response = xmShift.addMemberToShift(data[x]['name'], data[x]['shift'], data[x]['member'])
            if (response):
                self.succeed.append(data[x])
            else:
                self.fail.append(data[x])

    # def to Create Groups
    def removeGroupsCollection(self, data, max_threads):
        del self.succeed[:]  # first clear the list from previous process
        del self.fail[:]

        process = self.createCollection(data, max_threads, self.removeGroups)
        print('Returning List of Groups Removed: ' + str({'succeed': self.succeed, 'fail': self.fail}))
        return {'succeed': self.succeed, 'fail': self.fail}

    def removeGroups(self, thread, data):
        xmGroup = xMattersGroup(self.request)
        for x in range(len(data)):
            self.log.debug('Thread number: ' + str(thread) + ' Removing Group: ' + data[x]['targetName'])
            response = xmGroup.removeGroup(data[x]['targetName'])
            if (response):
                self.succeed.append(data[x]['targetName'])
            else:
                self.fail.append(data[x]['targetName'])
