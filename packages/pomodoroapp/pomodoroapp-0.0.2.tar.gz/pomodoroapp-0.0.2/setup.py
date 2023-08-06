try:
    from setuptools import setup
    from setuptools import find_packages
    
except ImportError:
    from distutils.core import setup
    
with open("README.md", "r") as fh:
    long_description = fh.read()
    
setup(
    name="pomodoroapp",
    version="0.0.2",
    author="Andrea Anaya",
    author_email="andrayantelo@gmail.com",
    description="Pomodoro GUI App",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/andrayantelo/pomodoroapp",
    packages=find_packages(),
    classifiers=[	
          "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
    ],
    python_requires='>=3.5',
)

