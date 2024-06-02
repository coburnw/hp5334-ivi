"""

Python Interchangeable Virtual Instrument Driver


Copyright (c) 2017 Coburn Wightman

derived from agilent436a.py driver by:
Copyright (c) 2012-2014 Alex Forencich

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

import ivi
from ivi import counter
from ivi import vxi11

#import time

# Parameter Values

ChanNameMap = {0 : 'A', 1 : 'B', 2 : 'C'}

Units = set(['Sec', 'Hz', 'Volts'])

Operator = set(['none', 'difference', 'sum', 'quotient'])

RangeType = set(['in_range', 'under_range', 'over_range'])

OperationState = set(['complete', 'in_progress', 'unknown'])

MeasurementFunction = set(['frequency',
                           'period',
                           'pulse_width',
                           'duty_cycle',
                           'edge_time',
                           'frequency_ratio',
                           'time_interval',
                           'totalize_continuous',
                           'totalize_gated',
                           'totalize_timed',
                           'invalid'])

MeasurementFunctionMap = {'frequency' : 'FN',   # fn1, fn2, fn3 is a, b, and c channel
                          'period': 'FN4',
                          'time_interval' : 'FN5',
                          'time_interval_delay' : 'FN6',
                          'frequency_ratio' : 'FN7',
                          'total_stop' : 'FN8',  # non standard
                          'total_start' : 'FN9', # non standard
                          'pulse_width' : 'FN10',
                          'edge_time' : 'FN11',
                          #'dc_voltage' : 'FN12',
                          #'trigger_voltage' : 'FN13',
                          #'peak_to_peak_voltage' : 'FN14',
                          #'totalize_timed' : 'x',
                          #'totalize_gated' : 'xx',
                          'invalid' : 'inv'}

ErrorMessages = { 0 : 'No error',    # to accurately reflect error codes of device, divide by 10
                  10 : 'Parameter disallowed in present mode',
                  11 : 'Attenuators controlled by AUTO TRIG',
                  12 : '50-ohm B, AC B settings preset by COM A',
                  13 : 'Slope B set by Slope A in Rise/Fall mode',
                  14 : 'Parameter disallowed in High Speed mode',
                  15 : 'Calibration data unaccessible in present mode',
                  20 : 'Invalid key entry',
                  21 : 'Data outside valid range',
                  22 : 'Data exceeds maximum resolution',
                  23 : 'Mantissa digit buffer full',
                  24 : 'Decimal point previously entered',
                  30 : 'Multiple key closures',
                  40 : 'Mnemonic not recognizable',
                  41 : 'Numeric syntax error',
                  42 : 'Alpha character expected',
                  43 : 'Data exceeds valid range',
                  44 : 'Attention (ATN) asserted in Talk-Only mode',
                  50 : 'Store instrument setup operation failed',        #50.X where x is the register number: 0-9
                  51 : 'Recall instrument setup operation failed',       #51.X
                  52 : 'HP-IB address cannot be recalled at power up; address default to 03'}


class agilentBase5334(ivi.Driver, counter.Base):
    "Agilent HP5334 Series IVI Universal Counter driver"
    
    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', '')
        
        super(agilentBase5334, self).__init__(*args, **kwargs)
        
        self._identity_description = "Agilent HP5334 Universal Counter driver"
        self._identity_identifier = ""
        self._identity_revision = ""
        self._identity_vendor = ""
        self._identity_instrument_manufacturer = "Agilent Technologies"
        self._identity_instrument_model = ""
        self._identity_instrument_firmware_revision = ""
        self._identity_specification_major_version = 1
        self._identity_specification_minor_version = 0
        self._identity_supported_instrument_models = ['HP5334A','HP5334B']
        
        self._init_defaults()
        self._init_channels()

    def _initialize(self, resource = None, id_query = False, reset = False, **keywargs):
        "Opens an I/O session to the instrument."
        
        super(agilentBase5334, self)._initialize(resource, id_query, reset, **keywargs)

        # configure interface
        if self._interface is not None:
            self._interface.term_char = '\n'
        
        # interface clear
        if not self._driver_operation_simulate:
            self._clear()

        # verify instrument model matches
        if id_query and not self._driver_operation_simulate:
            id = self.identity.instrument_model
            id_check = self._instrument_id
            id_short = id[:len(id_check)]
            if id_short != id_check:
                raise Exception("Instrument ID mismatch, expecting %s, got %s", id_check, id_short)

        # reset
        if reset:
            self.utility_reset()

    def _load_id_string(self):
        self._set_cache_valid(False, 'identity_instrument_manufacturer')
        self._set_cache_valid(False, 'identity_instrument_model')
        self._set_cache_valid(False, 'identity_instrument_firmware_revision')

        idstr = "HP5334S"
        if not self._driver_operation_simulate:
            idstr = self._ask("ID")

        if idstr.find('HP') == 0:
            self._identity_instrument_manufacturer = 'Agilent'
            self._set_cache_valid(True, 'identity_instrument_manufacturer')

            self._identity_instrument_model = idstr
            self._identity_instrument_firmware_revision = 'Cannot query from instrument'
            self._set_cache_valid(True, 'identity_instrument_model')
            self._set_cache_valid(True, 'identity_instrument_firmware_revision')
    
    def _get_identity_instrument_manufacturer(self):
        if self._get_cache_valid('identity_instrument_manufacturer'):
            return self._identity_instrument_manufacturer

        self._load_id_string()
        return self._identity_instrument_manufacturer
    
    def _get_identity_instrument_model(self):
        if self._get_cache_valid('identity_instrument_model'):
            return self._identity_instrument_model

        self._load_id_string()
        return self._identity_instrument_model
    
    def _get_identity_instrument_firmware_revision(self):
        if self._get_cache_valid():
            return self._identity_instrument_firmware_revision

        self._load_id_string()
        return self._identity_instrument_firmware_revision
    
    def _utility_disable(self):
        pass
    
    def _utility_error_query(self):
        error_code = 0
        error_message = "No error"
        try:
            error_code = self._ask("TE")
            error_code = float(error_code) * 10
            if error_code < 50 or error_code > 52:
                error_message = ErrorMessages[error_code]
            elif error_code < 51:
                regnum = int((error_code % 50) * 10.01)
                error_code = int(error_code)
                error_message = ErrorMessages[error_code]
            elif error_code < 52:
                regnum = int((error_code % 51) * 10.01)
                error_code = int(error_code)
                error_message = "Register " + str(regnum) + ' ' + ErrorMessages[error_code]
            
        except vxi11.vxi11.Vxi11Exception as err:
            error_message = err.msg
            error_code = -1
            
        except ValueError:
            error_message = "bad error code: " + str(error_code)
            error_code = -1
            
        except KeyError:
            error_message = "undefined error code: " + str(error_code)
            error_code = -1
            
        return (int(error_code), error_message)
    
    def _utility_lock_object(self):
        pass
    
    def _utility_unlock_object(self):
        pass
    
    def _utility_reset(self):
        #if not self._driver_operation_simulate:
        self._write("IN")
        self._clear()

        self.driver_operation.invalidate_all_attributes()
        self._init_defaults()

    def _utility_reset_with_defaults(self):
        self._utility_reset()
    
    def _utility_self_test(self):
        raise ivi.OperationNotSupportedException()
    
    def _init_defaults(self):
        self._measurement_function = 'frequency'
        self.driver_operation.invalidate_all_attributes()

        self._frequency_aperture = 0.3
        self._period_aperture = 0.3
        self._time_interval_resolution == 1e-9

    def _init_channels(self):
        try:
            super(agilentBase5334, self)._init_channels()
        except AttributeError:
            pass

        self._channel_name = list()
        self._channel_impedance = list()
        self._channel_coupling = list()
        self._channel_attenuation = list()
        self._channel_level = list()
        self._channel_hysteresis = list()
        self._channel_slope = list()
        self._channel_filter_enabled = list()
        self._channel_count = 3
        
        for i in range(self._channel_count):
            self._channel_name.append(ChanNameMap[i])
            self._channel_impedance.append(1e6)
            self._channel_coupling.append('dc')
            self._channel_attenuation.append(1)
            self._channel_level.append(-50)
            self._channel_hysteresis.append(0)
            self._channel_slope.append('positive')
            self._channel_filter_enabled.append(False)

        self.channels._set_list(self._channel_name)
        
        # Chan C not settable, override defaults
        self._channel_impedance[2] = 50
        self._channel_coupling[2] = 'ac'
    
    def _get_channel_impedance(self, index):
        index = ivi.get_index(self._channel_name, index)
        
        return self._channel_impedance[index]
    
    def _set_channel_impedance(self, index, value):
        if index > 1:
            raise ivi.SelectorNameException()
        index = ivi.get_index(self._channel_name, index)
        
        value = float(value)
        #if not self._driver_operation_simulate:
        if value > 99:
            self._write(ChanNameMap[index] + "Z0") # set to 1meg
            self._channel_impedance[index] = 1e6
        else: 
            self._write(ChanNameMap[index] + "Z1") # set to 50ohm
            self._channel_impedance[index] = 50
    
    def _get_channel_coupling(self, index):
        index = ivi.get_index(self._channel_name, index)
        
        return self._channel_coupling[index]
    
    def _set_channel_coupling(self, index, value):
        if index > 1:
            raise ivi.SelectorNameException()
        index = ivi.get_index(self._channel_name, index)
        
        if value not in counter.Coupling:
            raise ivi.ValueNotSupportedException()
        if value == "ac":
            self._write(ChanNameMap[index] + "A1") # ac
        else: 
            self._write(ChanNameMap[index] + "A0") # dc

        self._channel_coupling[index] = value
    
    def _get_channel_attenuation(self, index):
        index = ivi.get_index(self._channel_name, index)
        
        return self._channel_attenuation[index]
    
    def _set_channel_attenuation(self, index, value):
        if index > 1:
            raise ivi.SelectorNameException()
        index = ivi.get_index(self._channel_name, index)
        
        value = float(value)
        
        if value == 1:
            self._write(ChanNameMap[index] + "X0") # x1
        elif value == 10: 
            self._write(ChanNameMap[index] + "X1") # x10
        else:
            raise ivi.ValueNotSupportedException("attenuation must be '1' or '10'")

        self._channel_attenuation[index] = value
    
    def _get_channel_level(self, index):
        index = ivi.get_index(self._channel_name, index)
        
        return self._channel_level[index]
    
    def _set_channel_level(self, index, value):
        if index > 1:
            raise ivi.SelectorNameException()
        index = ivi.get_index(self._channel_name, index)

        value = float(value)
        max_atten = 10
        
        if value > 4.999 * max_atten:
            # set instrument to manual trigger (front panel knobs)
            self._write('AU0')
        elif value < -4.999 * max_atten:
            # set instrument to automatic trigger
            self._write('AU1')
        elif self._get_identity_instrument_model() == 'HP5334A':
            # set A instrument trigger dac values 
            self._write(ChanNameMap[index] + "T" + value)
        else:
            # B instrument has no dac. ignore for now.
            pass

        self._channel_level[index] = value
    
    def _get_channel_hysteresis(self, index):
        index = ivi.get_index(self._channel_name, index)

        return self._channel_level[index]
    
    def _set_channel_hysteresis(self, index, value):
        index = ivi.get_index(self._channel_name, index)
        
        value = float(value)
        self._channel_hysteresis[index] = value
    
    def _get_channel_slope(self, index):
        index = ivi.get_index(self._channel_name, index)
        
        return self._channel_slope[index]
    
    def _set_channel_slope(self, index, value):
        if index > 1:
            raise ivi.SelectorNameException()
        index = ivi.get_index(self._channel_name, index)
        
        if value not in counter.Slope:
            raise ivi.ValueNotSupportedException()
        if value == "positive":
            self._write(ChanNameMap[index] + "S0") # positive
        else: 
            self._write(ChanNameMap[index] + "S1") # negative

        self._channel_slope[index] = value
    
    def _get_channel_filter_enabled(self, index):
        index = ivi.get_index(self._channel_name, index)
        
        if index != 0:
            raise ivi.ValueNotSupportedException()

        return self._channel_filter_enabled[index]
    
    def _set_channel_filter_enabled(self, index, value):
        if index != 0:
            raise ivi.SelectorNameException()
        index = ivi.get_index(self._channel_name, index)
        
        if value == True:
            self._write("FI1") # 100khz filter on (a channel only)
        else: 
            self._write("FI0") # filter off.

        self._channel_filter_enabled[index] = value

    # totalize 
    def _totalize_continuous_configure(self, channel):
        if channel != 0:
            raise ivi.SelectorNameException()
        else:
            self._totalize_continuous.channel = channel

    def _totalize_continuous_fetch_count(self):
        return self._measurement_fetch()

    def _totalize_continuous_start(self):
        cmd = 'RE FN9'
        self._write(cmd)

    def _totalize_continuous_stop(self):
        cmd = 'FN8'
        self._write(cmd)

    # measurement
    def _set_measurement_function(self, value):     # override to limit functionality
        if value not in MeasurementFunction:
            raise ivi.ValueNotSupportedException()
        self._measurement_function = value
    
    def _measurement_is_measurement_complete(self): # counter.py version of get_state?
        return True
    
    def _measurement_abort(self):
        self._write("RE")
        #self._clear()
    
    def _measurement_fetch(self):
        val = self._read()
            
        if val[0] == 'O':
            return float("inf")

        f = float(val[1:19])
        return f

    def _measurement_initiate(self):
        if self._measurement_function == 'frequency' :
            func  = MeasurementFunctionMap[self._measurement_function] + repr(self._frequency_channel + 1)
            gate = 'GA' + str(self._frequency_aperture_time)
            cmd = func + gate
        elif self._measurement_function == 'period' :
            func = MeasurementFunctionMap[self._measurement_function]
            gate = 'GA' + str(self._period_aperture_time)
            cmd = func + gate
        elif self._measurement_function == 'time_interval' :
            func = MeasurementFunctionMap[self._measurement_function]
            if self._time_interval_resolution == 1e-10:
                gate = 'GV1'
            else:
                gate = 'GV0'
            cmd = func + gate
        elif self._measurement_function == 'frequency_ratio' :
            cmd = MeasurementFunctionMap[self._measurement_function]
        elif self._measurement_function == 'invalid' :
            cmd = MeasurementFunctionMap['invalid']

        self._write(cmd)

    def _measurement_read(self, maximum_time):
        self._measurement_initiate()
        return self._measurement_fetch()

