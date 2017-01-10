"""

Python Interchangeable Virtual Instrument Driver

Copyright (c) 2013-2014 Alex Forencich

Modified by Coburn Wightman 2017

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

"""

from .agilentBase5334 import *

class agilent5334B(agilentBase5334):
    "HP / Agilent 5334B universal counter driver"

    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', 'HP5334B')

        super(agilent5334B, self).__init__(*args, **kwargs)

        #self._input_impedance = 50
        #self._frequency_low = 10e3
        #self._frequency_high = 1.5e9



