from MesaHandler import MesaFileAccess

from collections import OrderedDict
from MesaHandler.support import *

class MesaAccess:
    def __init__(self):
        self.fullConfig = MesaFileAccess()

        self._fullDict = self.stripFullDict()

    def stripToDict(self,section):
        retDict = OrderedDict()
        for file,parameterDict in self.fullConfig.dataDict[section].items():
            for key,value in parameterDict.items():
                retDict[key] = value

        return retDict

    def stripFullDict(self):
        retDict = OrderedDict()

        for section in [sectionStarJob,sectionControl,sectionPgStar]:
            retDict.update(self.stripToDict(section))

        return retDict


    def __getitem__(self, item):
        return self._fullDict[item]

    def items(self):
        return self._fullDict.items()

    def __setitem__(self, key, value):
        self.fullConfig[key] = value
        self._fullDict = self.stripFullDict()