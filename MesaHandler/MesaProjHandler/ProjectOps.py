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
                raise ValueError("Aborting!!! No project specified.")
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
                raise ValueError("Invalid input for argument 'clean'")
        
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
                raise ValueError("Invalid input for argument 'overwrite'")
        else:
            os.system("cp -r $MESA_DIR/star/work %s" %self.projName)
            os.chdir(self.projName)
        
    

    def clean(self):
        print("Cleaning...")
        try:
            if os.system("./clean") != 0:
                raise OSError("Either the project '%s' or the file '%s/clean' does not exists...could not clean!" %(self.projName, self.projName))
            else:
                print("Done cleaning.\n")
        except:
            raise Exception("Clean failed!")
            

    def make(self):
        print("Making...")
        try:
            if os.system("./mk >>/dev/null 2>&1") != 0:
                raise OSError("Either the project '%s' or the file '%s/mk' does not exists...could not make!" %(self.projName, self.projName))
            print("Done making.\n")
        except:
            raise Exception("Make failed!")
        
    
    def run(self, silent=False):
        print('Running...')
        try:
            if silent == False:
                exitcode = os.system("./rn")
            elif silent == True:
                exitcode = os.system("./rn >>runlog 2>&1")
            else:
                raise ValueError("Invalid input for argument 'silent'")
            if exitcode != 0:
                raise OSError("Either the project '%s' or the file '%s/rn' does not exists...could not run!" %(self.projName, self.projName))
            else:
                print("Done with the run!\n")
        except:
            raise Exception("Run failed!")
            
    
    def rerun(self, photo, silent=False):
        try:
            print("Running from photo...")
            if silent == False:
                exitcode = os.system("./re %s" %photo)
            elif silent == True:
                exitcode = os.system("./re %s >>runlog 2>&1" %photo)
            else:
                raise ValueError("Invalid input for argument 'silent'")
            if exitcode != 0:
                raise OSError("Either the project '%s' or the file '%s/re'  does not exists...could not restart!" %(self.projName, self.projName))
            else:
                print("Done with the run!\n")
        except OSError:
            raise Exception("Rerun failed!")
            
    
    def loadProjInlist(self, inlistPath):
        try:
            if os.system("cd ..; cp %s %s/inlist_project" %(inlistPath, self.projName)) != 0:
                raise OSError("Either the project '%s' or the inlist '%s' does not exists...could not load!" %(self.projName, inlistPath))
        except:
            raise Exception("Loading project inlist failed!" %inlistPath)
    
    def loadPGstarInlist(self, inlistPath):
        try:
            if os.system("cd ..; cp %s %s/inlist_pgstar" %(inlistPath, self.projName)) != 0:
                raise OSError("Either the project '%s' or the inlist '%s' does not exists...could not load!" %(self.projName, inlistPath))
        except:
            raise Exception("Loading pgstar inlist failed!" %inlistPath)
