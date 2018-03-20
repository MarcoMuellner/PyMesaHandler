import os

from MesaHandler.support import *

class MesaEnvironmentHandler:
    def __init__(self):
        self.readMesaDir()

    def readMesaDir(self):
        self.mesaDir = os.environ[mesa_env]
        if not os.path.exists(self.mesaDir):
            raise EnvironmentError("MESA_DIR is not set in your enviroment. Be sure to set it properly!!")




x = MesaEnvironmentHandler()