import time

import pyvisa # PyVisa info @ http://PyVisa.readthedocs.io/en/stable/

# https://www.keysight.com/upload/cmc_upload/All/34410A_Quick_Reference.pdf

## Number of Points to request
USER_REQUESTED_POINTS = 1000
    ## None of these scopes offer more than 8,000,000 points
    ## Setting this to 8000000 or more will ensure that the maximum number of available points is retrieved, though often less will come back.
    ## Average and High Resolution acquisition types have shallow memory depth, and thus acquiring waveforms in Normal acq. type and post processing for High Res. or repeated acqs. for Average is suggested if more points are desired.
    ## Asking for zero (0) points, a negative number of points, fewer than 100 points, or a non-integer number of points (100.1 -> error, but 100. or 100.0 is ok) will result in an error, specifically -222,"Data out of range"

## Initialization constants
SCOPE_VISA_ADDRESS = 'USB0::0x0957::0x0407::MY44048527::0::INSTR' # Get this from Keysight IO Libraries Connection Expert
    ## Note: sockets are not supported in this revision of the script (though it is possible), and PyVisa 1.8 does not support HiSlip, nor do these scopes.
    ## Note: USB transfers are generally fastest.
    ## Video: Connecting to Instruments Over LAN, USB, and GPIB in Keysight Connection Expert: https://youtu.be/sZz8bNHX5u4

GLOBAL_TOUT =  10 # IO time out in milliseconds

def range_check(val, min, max, val_name):
    if val > max:
        print(f"Wrong {val_name}: {val}. Max output should be less then {max} V")
        val = max
    if val < min:
        print(f"Wrong {val_name}: {val}. Should be >= {min}")
        val = min
    return val



class GEN_33220A:
    def __init__(self):
        self.rm = pyvisa.ResourceManager()
        self.inst = self.rm.open_resource(SCOPE_VISA_ADDRESS)
        IDN = str(self.inst.query("*IDN?"))
        print(f'*** Connected to: {IDN}')
        ## Set Global Timeout
        ## This can be used wherever, but local timeouts are used for Arming, Triggering, and Finishing the acquisition... Thus it mostly handles IO timeouts
        self.inst.timeout = GLOBAL_TOUT

        ## Clear the instrument bus
        self.inst.clear()

    def __cmd_write(self, txt_cmd):
        self.inst.write(txt_cmd)

    def __cmd_query(self, txt_cmd):
        return_val = self.inst.query(txt_cmd)
        return return_val

    def cmd_read(self):
        txt_cmd = "READ?"
        tmp = self.__cmd_query(txt_cmd)
        return tmp

    def conf_puls(self):
        self.inst.write("FUNCtion PULSe")

    def conf_square(self):
        self.inst.write("FUNCtion SQUare")

    def conf_sinus(self):
        self.inst.write("FUNCtion SINusoid")

    def conf_dc(self):
        self.inst.write("FUNCtion DC")


    def set_freq(self, freq_hz):
        if freq_hz == "min":
            self.inst.write("FREQuency MINimum")
        if freq_hz == "max":
            self.inst.write("FREQuency MAXimum")
        else:
            self.inst.write(f'FREQ {freq_hz}')
    def set_voltage(self, voltage):
        voltage = range_check(voltage,-10,10,"Voltage")

        self.inst.write(f"VOLTage {voltage}")

    def set_output_on(self):
        self.inst.write(f"OUTPut ON")

    def set_output_off(self):
        self.inst.write(f"OUTPut OFF")

    def set_offset(self, offset_volt):
        offset_volt = range_check(offset_volt,-5,5, "set offset")
        self.inst.write(f"VOLTage:OFFSet {offset_volt}")

    def set_output_load(self, load_in_ohms, text_var=None):
        if load_in_ohms != 0:
            load_in_ohms = range_check(load_in_ohms,1, 10000, "Resistance")
            self.inst.write(f"OUTPut:LOAD {load_in_ohms}")
            return True
        if text_var != None:
            if text_var == "inf":
                self.inst.write(f"OUTPut:LOAD {INFinity}")
                return True
            if text_var == "min":
                self.inst.write(f"OUTPut:LOAD {MINimum}")
                return True
            if text_var == "max":
                self.inst.write(f"OUTPut:LOAD {MAXimum}")
                return True


    def set_trigger_immediate(self):
        self.inst.write(f"TRIGger:SOURce IMMediate")

    def trigger(self):
        self.inst.write(f"*TRG")

    def measure_voltage(self):
        return self.inst.query("MEASure:VOLTage:DC? AUTO")

    def sweep(self, start_freq, stop_freq, duration):
        self.inst.write('SWE:STAT OFF')  # Turn off sweep mode
        self.inst.write(f'SWE:STAR {start_freq}')
        self.inst.write(f'SWE:STOP {stop_freq}')
        self.inst.write(f'SWE:TIME {duration}')
        self.inst.write('SWE:STAT ON')  # Turn on sweep mode

    def stop_sweep(self):
        self.inst.write('SWE:STAT OFF')  # Turn off sweep mode

    def reset(self):
        self.inst.write('*RST')  # Turn off sweep mode

    def beep(self, delay_sec=1,  n_times = 1):
         delay_sec = range_check(delay_sec, 0,5, "beep:delay_sec" )

         for i in range(int(n_times)):
            self.__cmd_write(f'SYST:BEEP')  # Turn off sweep mode
            time.sleep(delay_sec)

    def close(self):
        self.inst.clear()
        self.inst.close()