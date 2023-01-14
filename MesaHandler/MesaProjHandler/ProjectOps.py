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
            if not click.confirm(f"Use the already existing '{self.projName}' project as it is?", default=False):
                raise ValueError("Aborting!!! No project specified.")
                os._exit()

        def cleanCheck():
            if clean == None:
                if click.confirm(f"Clean the existing '{self.projName}' project for re-use?", default=False):
                    self.clean()
                else:
                    useExisting()
            elif clean == True:
                self.clean()
            elif clean == False:
                print(f"Using the already existing '{self.projName}' project as it is.")
            else:
                raise ValueError("Invalid input for argument 'clean'")
        
        def writeover():
            os.chdir("..")
            os.system(f"rm -rf '{self.projName}'; cp -r $MESA_DIR/star/work .")
            os.rename("work", self.projName)
            os.chdir(self.projName)

        if self.found == True:
            if overwrite == True:
                writeover()
            elif overwrite == False:
                cleanCheck()
            elif overwrite == None:
                print(f"Mesa project named '{self.projName}' already exists!")
                if not click.confirm(f"Use the already existing '{self.projName}' project as it is?", default=False):
                    if click.confirm("Do you wish to overwrite?", default=False):
                        writeover()
                    else:
                        cleanCheck()
            else:
                raise ValueError("Invalid input for argument 'overwrite'")
        else:
            os.system(f"cp -r $MESA_DIR/star/work '{self.projName}'")
            os.chdir(self.projName)
        
    

    def clean(self):
        print("Cleaning...")
        try:
            if os.system("./clean") != 0:
                raise OSError(f"Either the project '{self.projName}' or the file '{self.projName}/clean' does not exists...could not clean!")
            else:
                print("Done cleaning.\n")
        except:
            raise Exception("Clean failed!")
            

    def make(self):
        print("Making...")
        try:
            if os.system("./mk >>/dev/null 2>&1") != 0:
                raise OSError(f"Either the project '{self.projName}' or the file '{self.projName}/mk' does not exists...could not make!")
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
                raise OSError(f"Either the project '{self.projName}' or the file '{self.projName}/rn' does not exists...could not run!")
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
                raise OSError(f"Either the project '{self.projName}' or the file '{self.projName}/re'  does not exists...could not restart!")
            else:
                print("Done with the run!\n")
        except OSError:
            raise Exception("Rerun failed!")
            
    
    def loadProjInlist(self, inlistPath):
        try:
            if os.system(f"cd ..; cp {inlistPath} {self.projName}/inlist_project") != 0:
                raise OSError(f"Either the project '{self.projName}' or the inlist {inlistPath} does not exists...could not load!" %(self.projName, inlistPath))
        except:
            raise Exception("Loading project inlist failed!" %inlistPath)
    
    def loadPGstarInlist(self, inlistPath):
        try:
            if os.system(f"cd ..; cp {inlistPath} {self.projName}/inlist_pgstar") != 0:
                raise OSError(f"Either the project '{self.projName}' or the inlist '{inlistPath}' does not exists...could not load!" %(self.projName, inlistPath))
        except:
            raise Exception("Loading pgstar inlist failed!" %inlistPath)
