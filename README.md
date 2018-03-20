# PyMesaHandler
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

## Getting started
PyMesaHandler is available through pip. To install simply
call
```
pip install PyMesaHandler
```
## Usage example
Lets say you want to edit the initial mass of the model
you want to create. Simply create a python file
in the same directory as the inlist files with the
following code
```python
from MesaHandler import MesaAccess

object = MesaAccess()

object["initial_mass"] = 5
```
and run it. **Thats it**. The file will now have the
changed mass as its parameter.

## Future development
There are many features that are aimed to be added to this
module. The goal is to create a package, where you no
longer need to manually run Mesa, so that you can automate
your usage of Mesa. Features for the pipeline are:

- **Parameter creation**: Currently the module only allows
for access of already existing parameters. This will
include checks if the parameter actually exists within Mesa.
- **Automated Build & run for Mesa**: The moduel will run
Mesa if you want to run it through the module
- **Plotting capabilities**: You want to plot one
or multiple results from Mesa? That will be also possible
through this package.

And various other features that are not yet included.
