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
        if os.path.exists(self.projName):
            os.chdir(self.projName)
            self.found = True               ## Proj already present flag
        else:
            self.found = False

    

    def create(self, overwrite=None, clean=None):       ### overwrite and clean are boolean arguments that are intentionally kept empty
        def useExisting():
            if not click.confirm("Use the already existing '%s' project as it is?" %self.projName, default=False):
                raise Exception("Aborting!!! No project specified.")
                os._exit()

        def cleanCheck():
            if clean == None:
                if click.confirm("Clean the existing '%s' project for re-use?" %self.projName, default=False):
                    self.clean()
                else:
                    useExisting()
            elif clean == True:
                self.clean()
            elif clean == False:
                print("Using the already existing '%s' project as it is." %self.projName)
            else:
                raise Exception("Invalid input for argument 'clean'")
        
        def writeover():
            os.chdir("..")
            os.system("rm -rf %s; cp -r $MESA_DIR/star/work ." %self.projName)
            os.rename("work", self.projName)
            os.chdir(self.projName)

        if self.found == True:
            if overwrite == True:
                writeover()
            elif overwrite == False:
                cleanCheck()
            elif overwrite == None:
                print("Mesa project named '"+self.projName+"' already exists!")
                if not click.confirm("Use the already existing '%s' project as it is?" %self.projName, default=False):
                    if click.confirm("Do you wish to overwrite?", default=False):
                        writeover()
                    else:
                        cleanCheck()
            else:
                raise Exception("Invalid input for argument 'overwrite'")
        else:
            os.system("cp -r $MESA_DIR/star/work %s" %self.projName)
            os.chdir(self.projName)
        
    

    def clean(self):
        try:
            print("Cleaning...")
            os.system("./clean")
            print("Done cleaning.\n")
        except:
            raise Exception("Project '%s' does not exists...could not clean!" %self.projName)

    def make(self):
        try:
            print("Making...")
            os.system("./mk &>/dev/null")
            print("Done making.\n")
        except:
            raise Exception("Project '%s' does not exists...could not make!" %self.projName)
    
    def run(self, silent=False):
        try:
            print('Running...')
            if silent == False:
                os.system("./rn")
            elif silent == True:
                os.system("./rn &>>runlog")
            else:
                raise Exception("Invalid input for argument 'silent'")
            print("Done with the run!\n")
        except:
            raise Exception("Project '%s' does not exists...could not run!" %self.projName)
    
    def rerun(self, photo, silent=False):
        try:
            print("Running from photo...")
            if silent == False:
                os.system("./re %s" %photo)
            elif silent == True:
                os.system("./re %s &>>runlog" %photo)
            else:
                raise Exception("Invalid input for argument 'silent'")
            print("Done with the run!\n")
        except:
            raise Exception("Photo '%s' does not exists...could not restart!" %photo)
    
    def loadProjInlist(self, inlistPath):
        try:
            os.system("cd ..; cp %s %s/inlist_project" %(inlistPath, self.projName))
        except:
            raise Exception("Inlist '%s' does not exists...could not restart!" %inlistPath)
    
    def loadPGstarInlist(self, inlistPath):
        try:
            os.system("cd ..; cp %s %s/inlist_pgstar" %(inlistPath, self.projName))
        except:
            raise Exception("Inlist '%s' does not exists...could not restart!" %inlistPath)
