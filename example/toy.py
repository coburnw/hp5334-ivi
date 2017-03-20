import sys
import time

import ivi

#
# hit your instrument directly, bypassing IVI and the IVI driver
#
#import vxi11
#instr = vxi11.Instrument("192.168.2.9", "gpib0,3")
#instr.term_char = '\n'
#print instr.ask("ID")
#quit()

#
# use IVI and the 5334 driver to interact with a vxi-11 connected instrument.
#
instr = ivi.contrib.agilent5334B("TCPIP0::192.168.2.9::gpib0,3::INSTR")

#instr.help()

print instr.identity.instrument_manufacturer,
print instr.identity.instrument_model
print

instr.frequency.channel = 0

instr.channels[0].coupling = 'dc'
instr.channels[0].slope = 'positive'
instr.channels[0].impedance = 1e6

# set channel level to -50 for auto trigger levels, +50 for front panel trigger levels 
instr.channels[0].level = 50
instr.channels[0].attenuation = 1
instr.channels[0].filter_enabled = False

instr.channels[1].coupling = 'dc'
instr.channels[1].slope = 'positive'
instr.channels[1].impedance = 1e6
#instr.channels[1].filter_enabled = False

#instr.channels[2].coupling = 'ac'
#instr.channels[2].slope = 'positive'
#instr.channels[2].impedance = 50

print('Channel ' + instr.channels[0].name)
print(' ' + instr.channels[0].coupling)
print(' ' + instr.channels[0].slope)
print(' ' + `instr.channels[0].impedance`)

print('Channel ' + instr.channels[1].name)
print(' ' + instr.channels[1].coupling)
print(' ' + instr.channels[1].slope)
print(' ' + `instr.channels[1].impedance`)

print('Channel ' + instr.channels[2].name)
print(' ' + instr.channels[2].coupling)
print(' ' + instr.channels[2].slope)
print(' ' + `instr.channels[2].impedance`)
print

instr.measurement_function = 'frequency'
instr.frequency.aperture_time = 1

instr.frequency.channel = 0
print instr.measurement_function, instr.channels[instr.frequency.channel].name + ' = ',

try:
    print instr.measurement.read(1000)
    
except ivi.vxi11.vxi11.Vxi11Exception as e:
    print "Vxi11Exception: " + e.msg
    print instr.utility.error_query()
    instr.measurement.abort()

instr.frequency.channel = 1
print instr.measurement_function, instr.channels[instr.frequency.channel].name + ' = ',
try:
    print instr.measurement.read(1000)
    
except ivi.vxi11.vxi11.Vxi11Exception as e:
    print "Vxi11Exception: " + e.msg
    print instr.utility.error_query()
    instr.measurement.abort()

instr.frequency.channel = 2
print instr.measurement_function, instr.channels[instr.frequency.channel].name + ' = ',
try:
    print instr.measurement.read(1000)
    
except ivi.vxi11.vxi11.Vxi11Exception as e:
    print "Vxi11Exception: " + e.msg
    print instr.utility.error_query()
    instr.measurement.abort()

instr.measurement_function = 'period'
instr.period.aperture_time = 1
print instr.measurement_function, instr.channels[instr.period.channel].name + ' = ',

try:
    print instr.measurement.read(1000)
    
except ivi.vxi11.vxi11.Vxi11Exception as e:
    print "Vxi11Exception: " + e.msg
    print instr.utility.error_query()
    instr.measurement.abort()

# measures interval from a to b.  Will timeout if b channel is inactive
instr.measurement_function = 'time_interval'
instr.time_interval.resolution = 1e-9
print instr.measurement_function + ' = ',
try:
    print instr.measurement.read(1000)
    
except ivi.vxi11.vxi11.Vxi11Exception as e:
    print "Vxi11Exception: " + e.msg
    print instr.utility.error_query()
    instr.measurement.abort()

# measures interval from a to b with 100-gate average
instr.measurement_function = 'time_interval'
instr.time_interval.resolution = 1e-10
print instr.measurement_function + ' = ',
try:
    print instr.measurement.read(1000)
    
except ivi.vxi11.vxi11.Vxi11Exception as e:
    print "Vxi11Exception: " + e.msg
    print instr.utility.error_query()
    instr.measurement.abort()

instr.totalize_continuous.channel = 0
instr.totalize_continuous.start()
print 'continuous totalize ' , instr.channels[instr.totalize_continuous.channel].name + ' = ',
try:
    print instr.totalize_continuous.fetch_count()
    
except ivi.vxi11.vxi11.Vxi11Exception as e:
    print "Vxi11Exception: " + e.msg
    print instr.utility.error_query()
    instr.measurement.abort()

instr.totalize_continuous.stop()

