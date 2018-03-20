import re
from collections import OrderedDict

from MesaHandler.support import *


class MesaFileAccess:

    def __init__(self):
        self.setupDict()

    def setupDict(self):
        self.dataDict = OrderedDict()

        for section in [sectionStarJob,sectionControl,sectionPgStar]:
            self.dataDict[section]  = OrderedDict()
            self.readSections("inlist",section)

    def readFile(self,fileName):
        with open(fileName) as f:
            return f.read()

    def writeFile(self,fileName,content):
        with open(fileName,'w') as f:
            f.write(content)

    def readSections(self,filename,section=None):
        content = self.readFile(filename)

        p = re.compile(regex_sections)

        for matches in p.findall(content):
            if section is not None and section != matches[0]:
                continue

            self.dataDict[section][filename] =self.getParameters(matches[0],matches[1])



    def getParameters(self,section,text):
        parameters = OrderedDict()
        p = re.compile(regex_read_parameter)

        for matches in p.findall(text):
            if len(matches) != 2:
                raise AttributeError("Regex needs to match 2 items here! Found "+str(len(matches)))

            if matches[0] in external_file_parameters:
                self.readSections(self.convertToPythonTypes(matches[1]),section)
            else:
                parameters[matches[0]] = self.convertToPythonTypes(matches[1])

        return parameters


    def convertToPythonTypes(self,data):
        if data[0] == "." and data[-1] == ".": # return boolean
            return True if data[1:-1] == "true" else False
        elif data[0] == "'" and data[-1] == "'": # return string
            return data[1:-1]
        elif re.compile(regex_floatingValue).match(data) is not None:
            matches = re.compile(regex_floatingValue).findall(data)
            return float(matches[0][0])*pow(10,float(matches[0][1]))
        elif "." in data:
            return float(data)
        else:
            try:
                return int(data)
            except:
                raise AttributeError("Cannot convert "+data+" to known type!")

    def convertToInlistValue(self,data):
        if isinstance(data,bool):
            return "."+("true"if data else "false") + "."
        elif isinstance(data,str):
            return "'"+data+"'"
        elif isinstance(data,float) or isinstance(data,int):
            return str(data)
        else:
            raise AttributeError("Cannot convert type "+str(type(data))+"to known type")

    def items(self):
        return self.dataDict.items()

    def __getitem__(self, item):
        return self.dataDict[item]

    def __setitem__(self, key, value):
        for section in [sectionStarJob, sectionControl, sectionPgStar]:
            for file,parameteDict in self.dataDict[section].items():
                if key in parameteDict.keys():
                    self.rewriteFile(file,key,value)
                    return

    def rewriteFile(self,file,key,value):
        content = self.readFile(file)

        regex = r"("+key+r".+=)\s* ([\.\w_\d']+)"
        p = re.compile(regex)
        content = p.sub(r"\1 "+self.convertToInlistValue(value),content)

        self.writeFile(file,content)
        self.setupDict()

