# PyMesaHandler ![Travis Status](https://travis-ci.org/muma7490/PyMesaHandler.svg?branch=master)
PyMesHandler allows for a native interaction of inlist
files via Python. This means, that the package will
automatically convert between the fortran like variables
within inlist and native python standard datatypes. For
example the variable
```fortran
read_extra_star_job_inlist1 = .true.
```
will be available through the package as
```python
mesaHandlerObject["read_extra_star_job_inlist1"] = True
```

The conversion happens in a black box using some regex
magic automatically. This means if you change a property
in the python object, it will automatically transfer to
the file.

Keep in mind this application is still a work in progress.
If you find any errors or have a feature request, don't
hesitate to open an issue on this github.

## Features
- **No more file hassle**. PyMesaHandler automatically
combines all files you use for your setup and will
update them accordingly
- **Python file types**. You can actually do some scripting
or calculation beforehand. The package will automatically
convert these properly to the right types for fortran.
- **Parameter creation and deletion**: The package allows you to create
and remove parameters from your inlist files, again using only python
datatypes. It will even check if the parameter is available through
the Mesa defaults and if the type of the data you want to assign is the
correct one.
- **Includes the full capabilities of MesaReader**: MesaReader is
included as a submodule of this code, and therefore provides it's full
capabilities. Further integration is also part of future development.
- **Creation of new projects and sharing of projects**: Now you only need to share your python
project. Anyone who has Python and Mesa installed, will than be able to
run your model using only python code. You can also run Mesa solely through the module.
## Getting started
PyMesaHandler is available through pip. To install simply
call
```
pip install PyMesaHandler
```
## Usage example
Simply write a python file anywhere and 
use it to create, modify, make and run a project in the current working 
directory. Lets say you want to create a new project and edit the initial mass of the model
you want to create, you can do all this with the following code
```python
from MesaHandler.MesaProjHandler import ProjectOps
from MesaHandler import MesaAccess


work = ProjectOps()        ## Use ProjectOps("your_project") for a custom project name  
work.create()              ## Use boolean arguments 'overwrite' and 'clean' to work on existing projects.
                           ## Interactive user prompts are shown if neither of these arguments are supplied.

work.loadProjInlist("relative/path/to/inlist_custom_project")
work.loadPGstarInlist("relative/path/to/inlist_custom_pgstar")

object = MesaAccess()
object["initial_mass"] = 5

work.make()
work.run()
work.rerun("x450")        ## Rerun from a photo
work.clean()              ## Clean the project
```
**Thats it**. You will now have a new project (MESA work directory) with the inlist file having the
changed mass as its parameter. You can use any parameter that is
available through your installed Mesa version.
Also refer examply.py for more information.

PyMesaHandler also includes MesaReader, whichs documentation can be
found [here](https://wmwolf.github.io/py_mesa_reader/).

## Credit

As it should be mentioned here, the code makes use of
[MesaReader](https://github.com/wmwolf/py_mesa_reader). Thanks to
the original author to make its use available to me.

## Future development
There are many features that are aimed to be added to this
module. The goal is to create a package, where you no
longer need to manually run Mesa, so that you can automate
your usage of Mesa. Features for the pipeline are:

- **Plotting capabilities**: You want to plot one
or multiple results from Mesa? That will be also possible
through this package.
- **Further Integration of MesaReader**: MesaReader has some cool
capabilities to get Mesa Reader into Python. Future development will
see further integration into the MesaAccess class, as this should
be the only point of entry to interact with Mesa.

And various other features that are not yet included.
