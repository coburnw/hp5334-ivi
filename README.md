## HP5334A/B Universal Counter driver for Python-IVI

A rough but functional driver for the HP5334B Universal Counter

### Requirements
  * developed using Python 2.7.9
  
### Dependencies
  * python-ivi https://github.com/python-ivi/python-ivi
  * python-vxi11 https://github.com/python-ivi/python-vxi11
  * untested with the other python-ivi gpib interface drivers
  
### Installation
  Three installation methods
  
#### I know what I'm doing
  * Copy the new driver files into the Python-IVI tree
  * Adjust `__init__.py` files accordingly
  * rebuild and reinstall python-ivi
  * make the digits roll
  
#### I like to know what I'm doing
  Inside the python-ivi source tree I made a contrib folder to store
  additional drivers. This was to minimize the amount of tromping around i would
  have to do in someone else's tree.  The `__init__.py` files need to be adjusted up
  the tree to account for the changes in structure including `config.py` at the root
  only once, while the `__init__.py` file in contrib needs to accurately reflect
  any changes to the contents of the contrib folder.

  An easier way to handle this might be to copy the new drivers directly into
  python-ivi/ivi/agilent folder and adjusting its `__init__.py` file accordingly.
  This might be a safer bet if you git pull python-ivi now and then.

  Regardless of the installation method chosen, the python-ivi package must
  be rebuilt and reinstalled each time a file inside its tree is modified.
  If you develop your application outside of the python-ivi tree, then a
  rebuild should hopefully be a rare occasion.

#### Just spell it out for me (in my case, and as best as i recall)
  * git clone https://github.com/coburnw/hp5334-ivi.git to a devel directory
    of your choice.  For me it was the parent folder containing the python-ivi clone.
  * if it doesnt already exist, mkdir python-ivi/ivi/contrib
  * cp hp5334-ivi.git/contrib/agilent*.py to python-ivi/ivi/contrib folder
  * edit `python-ivi/ivi/contrib/__init__.py` file to add each of the 5334 drivers 
  * edit `python-ivi/ivi/__init__.py` and add 'contrib' to IVI drivers section
  * edit `python-ivi/setup.py` and verify 'contrib' in IVI drivers section
  * `python setup.py install` to (re)build and (re)install python-ivi
  * explore the example folder in hp5334-ivi.git

### Notes
  * developed for an HP5334B and an E2050A
  * if any of the agilent5334 driver files are modified, python-ivi will
    need to be rebuilt and reinstalled
  * none of the memory, math, or voltmeter functionality has been implemented
  * frequency, time_interval, period, and ratio seems to work
  * with my setup, i had to define instr.term_char = '\n'.  I found,
    this caused a conversion error during pack_int() of the python-vxi11
    library.  If you have the same problem, notes on how i worked around it
    are [here] (https://github.com/python-ivi/python-vxi11/commit/3b9a0e9ea7788c24c61727854a0e997b46fbd3f9)

This has been a fun trip and I greatly appreciate the work the Python-IVI
developers have invested.  I look forward to fleshing this little cog out
further.
