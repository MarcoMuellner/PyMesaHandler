import pip
from setuptools import setup,find_packages

reqs = ["numpy==1.14.2"]


#this is a bit of a hack, due to the inability to build numpy properly in a reasonable amount of time
for req in reqs:
    pip.main(["install", req])

setup(
    name='PyMesaHandler',
    version='0.2.1',
    packages=find_packages(exclude=["*test", "dist", "build", "venv","*egg-info*"]),
    url='https://github.com/muma7490/PyMesaHandler',
    license='MIT',
    author='Marco Müllner',
    author_email='muellnermarco@gmail.com',
    description='An easy way to handle Mesa using Python',
)
