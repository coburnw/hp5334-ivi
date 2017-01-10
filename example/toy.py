import sys
import time

import ivi
#import vxi11

#instr = vxi11.Instrument("192.168.2.9", "gpib0,3")
instr = ivi.contrib.agilent5334A("TCPIP0::192.168.2.9::gpib0,3::INSTR")

instr.term_char = '\n'

#print instr.ask("FN1")
#instr.help()

#print instr.utility.error_query()
#print instr.utility.self_test()
#print instr.utility.reset()
#quit()

print instr.identity.instrument_manufacturer
print instr.identity.instrument_model

instr.channels[0].coupling = 'ac'
instr.channels[0].slope = 'positive'
instr.channels[0].impedance = 1e6
instr.channels[0].hysteresis = 1
instr.channels[0].filter_enabled = False

instr.channels[1].coupling = 'ac'
instr.channels[1].slope = 'positive'
instr.channels[1].impedance = 1e6

#instr.channels[2].coupling = 'ac'
#instr.channels[2].slope = 'positive'
#instr.channels[2].impedance = 50

print('Channel ' + instr.channels[0].name)
print(instr.channels[0].coupling)
print(instr.channels[0].slope)
print(instr.channels[0].impedance)

print('Channel ' + instr.channels[1].name)
print(instr.channels[1].coupling)
print(instr.channels[1].slope)
print(instr.channels[1].impedance)

print('Channel ' + instr.channels[2].name)
print(instr.channels[2].coupling)
print(instr.channels[2].slope)
print(instr.channels[2].impedance)

instr.frequency.channel = 0

instr.measurement_function = 'frequency'
print instr.measurement_function
try:
    print instr.measurement.read(1000)
    
except ivi.vxi11.vxi11.Vxi11Exception as e:
    print "got Vxi11Exception: " + e.msg
    print instr.utility.error_query()
    print instr.utility.reset()

instr.measurement_function = 'period'
print instr.measurement_function
try:
    print instr.measurement.read(1000)
    
except ivi.vxi11.vxi11.Vxi11Exception as e:
    print "got Vxi11Exception: " + e.msg
    print instr.utility.error_query()
    print instr.utility.reset()

# measures interval from a to b.  Will timeout if b channel is inactive
instr.measurement_function = 'time_interval'
print instr.measurement_function
try:
    print instr.measurement.read(1000)
    
except ivi.vxi11.vxi11.Vxi11Exception as e:
    print "got Vxi11Exception: " + e.msg
    print instr.utility.error_query()
    print instr.utility.reset()

instr.measurement_function = 'totalize_continuous'
print instr.measurement_function
try:
    print instr.measurement.read(1000)
    
except ivi.vxi11.vxi11.Vxi11Exception as e:
    print "got Vxi11Exception: " + e.msg
    print instr.utility.error_query()
    print instr.utility.reset()

