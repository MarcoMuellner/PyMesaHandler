import os
from MesaHandler.MesaFileHandler.MesaEnvironmentHandler import MesaEnvironmentHandler
import click

class ProjectOps:
    def __init__(self, projName=''):
        self.envObject = MesaEnvironmentHandler()
        if projName == '':
            self.projName = input("No project name supplied! Please provide a project name... \n")
        else:
            self.projName = projName
    
    def make(self):
        if not os.path.exists(self.projName):
            print("Project does not exists!! Create a project first.")
        else:
            os.system("cd %s; ./mk >/dev/null 2>&1" %self.projName)
    
    def run(self):
        if not os.path.exists(self.projName):
            print("Project does not exists!!")
        else:
            os.system("cd %s; ./rn" %self.projName)

    
    def create(self, overwrite=False, clean=False):
        if os.path.exists(self.projName):
            print("Mesa project "+self.projName+" already exists! \n")
            if overwrite == False:
                if click.confirm("Do you wish to overwrite?", default=False):
                    os.system("rm -rf %s" %self.projName)
                    self.workCreate()
                elif clean == False:
                    if click.confirm("Clean the existing work directory for re-use?", default=False):
                        self.workClean()
                elif clean == True:
                    self.workClean()
            else:
                self.workCreate() 
        else:
            self.workCreate()
    

    def workClean(self):
        os.system('''
                cd %s
                ./clean
                ''' %self.projName)

    def workCreate(self):
        os.system('''
                cp -R $MESA_DIR/star/work %s
                cd %s
                ''' %(self.projName, self.projName)
                )
    
    def projectName(self):
        return self.projName