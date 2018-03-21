import pytest
from typing import Tuple,List

from MesaHandler import MesaFileAccess
from MesaHandler.support import *

import shutil


testWritePath = "tests/playground/"
inlistpgstarParameters = [
    "HR_win_flag",
    "HR_logT_min",
    "HR_logT_max",
    "HR_logL_min",
    "HR_logL_max",
    "HR_win_width",
    "HR_win_aspect_ratio",
    "TRho_Profile_win_flag",
    "show_TRho_Profile_legend",
    "show_TRho_Profile_text_info",
    "TRho_Profile_win_width",
    "TRho_Profile_win_aspect_ratio",
]

inlistProjectParametersStarJob =[
"create_pre_main_sequence_model",
"save_model_when_terminate", 
"save_model_filename",
"pgstar_flag", 
"change_Y", 
"new_Y", 
]

inlistProjectParametersControl = [
    "initial_mass",
    "Lnuc_div_L_zams_limit",
    "stop_near_zams",
    "max_age",
    "max_years_for_timestep",
    "mixing_length_alpha",
    "xa_central_lower_limit_species(1)",
    "xa_central_lower_limit(1)",
]

@pytest.fixture(scope="function")
def defaultSetup(request):
    with cd("tests"):
        if "playground" not in os.listdir("."):
            os.makedirs("playground/")


    def cleanup():
        print("Performing cleanup")
        with cd(testWritePath):
            for i in os.listdir("."):
                os.remove(i)
        with cd("tests"):
            if "playground" in os.listdir("."):
                os.rmdir("playground")

        os.remove("inlist")
        os.remove("inlist_pgstar")
        os.remove("inlist_project")

    shutil.copy2("tests/inlist","inlist")
    shutil.copy2("tests/inlist_pgstar", "inlist_pgstar")
    shutil.copy2("tests/inlist_project", "inlist_project")

    request.addfinalizer(cleanup)
    return MesaFileAccess()

def testObject(defaultSetup: MesaFileAccess):
    object = defaultSetup
    assert set(sections).issubset(object.dataDict.keys())
    assert set(inlistpgstarParameters).issubset(object.dataDict["pgstar"]["inlist_pgstar"].keys())
    assert set(inlistProjectParametersStarJob).issubset(object.dataDict["star_job"]["inlist_project"].keys())
    assert set(inlistProjectParametersControl).issubset(object.dataDict["controls"]["inlist_project"].keys())

    object["initial_mass"] = 5
    assert object["controls"]["inlist_project"]["initial_mass"] == 5
    object["initial_mass"] = 10
    assert object["controls"]["inlist_project"]["initial_mass"] == 10
    object.addValue("saved_model_for_merger_1","text")
    assert object["star_job"]["inlist_project"]["saved_model_for_merger_1"] == "text"
    object.removeValue("saved_model_for_merger_1")
    with pytest.raises(KeyError):
        object.addValue("dummy","dummy")



@pytest.mark.parametrize("value",[("firstFile","abcd"),("secondFile.txt","efgh"),("firstFile","jklmn")])
def testWriteFile(defaultSetup: MesaFileAccess,value:Tuple[str,str]):
    defaultSetup.writeFile(testWritePath+value[0],value[1])
    assert os.path.exists(testWritePath+value[0])
    with open(testWritePath+value[0]) as f:
        assert value[1] == f.read()



