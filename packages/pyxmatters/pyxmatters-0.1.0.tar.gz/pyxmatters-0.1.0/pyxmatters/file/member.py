import logging
import csv

class MemberFile(object):

    # constructor
    def __init__(self, file, encoding):
        self.log = logging.getLogger(__name__)
        self.file = file
        self.encoding = encoding

    def getGroupMembership(self, groups):

        members = []
        for group in groups:
            with open(self.file, encoding=self.encoding) as f:
                reader = csv.DictReader(f, delimiter=',')
                for row in reader:
                    if (row['name'] == group['name']):
                        members.append({'name': row['name'], 'shift': row['shift'], 'member': row['member']})
        return members
