import os
from MesaHandler.MesaFileHandler.MesaEnvironmentHandler import MesaEnvironmentHandler
import click

class ProjectOps:
    def __init__(self, name=''):
        self.envObject = MesaEnvironmentHandler()
        if name == '':
            self.projName = "work"
            ### If user input is preferred over a default value, uncomment the line below
            # self.projName = input("No project name supplied! Please provide a project name... \n")
        else:
            self.projName = name

    
    def create(self, overwrite=None, clean=None):       ### overwrite and clean are boolean arguments that are intentionally kept empty
        def useExisting():
            if click.confirm("Use the already existing '%s' project as it is?" %self.projName, default=False):
                os.chdir(self.projName)
            else:
                raise Exception("Aborting!!! No project specified.")
                os._exit()

        def cleanCheck():
            if clean == None:
                if click.confirm("Clean the existing '%s' project for re-use?" %self.projName, default=False):
                    self.workClean()
                else:
                    useExisting()
            elif clean == True:
                self.workClean()
            elif clean == False:
                useExisting()

        if os.path.exists(self.projName):
            print("Mesa project named '"+self.projName+"' already exists! \n")
            if overwrite == True:
                self.workCreate()
            elif overwrite == False:
                cleanCheck()
            elif overwrite == None:
                if click.confirm("Use the already existing '%s' project as it is?" %self.projName, default=False):
                    os.chdir(self.projName)
                elif click.confirm("Do you wish to overwrite?", default=False):
                    os.system("rm -rf %s" %self.projName)
                    self.workCreate()
                else:
                    cleanCheck()
        else:
            self.workCreate()


    def workClean(self):
        os.system('''
                cd %s
                ./clean
                ''' %self.projName)
        os.chdir(self.projName)

    def workCreate(self):
        os.system('''
                cp -R $MESA_DIR/star/work %s
                cd %s
                ''' %(self.projName, self.projName)
                )
        os.chdir(self.projName)

    def make(self):
        try:
            os.system("./mk >/dev/null 2>&1")
        except:
            raise Exception("Project '%s' does not exists...could not make!" %self.projName)
        
    
    def run(self):
        try:
            os.system("./rn")
        except:
            raise Exception("Project '%s' does not exists...could not run!" %self.projName)
    
    def rerun(self, photo):
        try:
            os.system("./re %s" %photo)
        except:
            raise Exception("Photo '%s' does not exists...could not restart!" %photo)