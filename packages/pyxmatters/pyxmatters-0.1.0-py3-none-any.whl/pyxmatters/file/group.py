import logging
import csv

class GroupFile(object):

    # constructor
    def __init__(self, file, encoding):
        self.log = logging.getLogger(__name__)
        self.file = file
        self.encoding = encoding

    def getGroups(self):

        groups = []
        with open(self.file, encoding=self.encoding) as f:
            reader = csv.DictReader(f, delimiter=',')
            for row in reader:
                if (row['name'] not in groups):
                    groups.append(row['name'])

        return groups
