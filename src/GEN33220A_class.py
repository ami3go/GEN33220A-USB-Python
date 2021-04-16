import sys
import pyvisa # PyVisa info @ http://PyVisa.readthedocs.io/en/stable/
import time

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
        self.app = self.rm.open_resource(SCOPE_VISA_ADDRESS)
        IDN = str(self.app.query("*IDN?"))
        print(f': Connected to: {IDN}')
        ## Set Global Timeout
        ## This can be used wherever, but local timeouts are used for Arming, Triggering, and Finishing the acquisition... Thus it mostly handles IO timeouts
        self.app.timeout = GLOBAL_TOUT

        ## Clear the instrument bus
        self.app.clear()
    def conf_puls(self):
        self.app.write("FUNCtion PULSe")

    def conf_square(self):
        self.app.write("FUNCtion SQUare")

    def conf_sinus(self):
        self.app.write("FUNCtion SINusoid")

    def conf_dc(self):
        self.app.write("FUNCtion DC")



    def set_freq(self, freq):
        if freq == "min":
            self.app.write("FREQuency MINimum")
        if freq == "max":
            self.app.write("FREQuency MAXimum")

    def set_voltage(self, voltage):
        voltage = range_check(voltage,-10,10,"Voltage")

        self.app.write(f"VOLTage {voltage}")

    def set_output_on(self):
        self.app.write(f"OUTPut ON")

    def set_output_off(self):
        self.app.write(f"OUTPut OFF")

    def cmd_write(self, txt_cmd):
        self.app.write(txt_cmd)

    def set_output_load(self, load_in_ohms, text_var=None):
        if load_in_ohms != 0:
            load_in_ohms = range_check(load_in_ohms,1, 10000, "Resistance")
            self.app.write(f"OUTPut:LOAD {load_in_ohms}")
            return True
        if text_var != None:
            if text_var == "inf":
                self.app.write(f"OUTPut:LOAD {INFinity}")
                return True
            if text_var == "min":
                self.app.write(f"OUTPut:LOAD {MINimum}")
                return True
            if text_var == "max":
                self.app.write(f"OUTPut:LOAD {MAXimum}")
                return True



    def cmd_query(self, txt_cmd):
        return_val = self.app.query(txt_cmd)
        return return_val
    def cmd_read(self):
        txt_cmd = "READ?"
        tmp = self.cmd_query(txt_cmd)
        return tmp
    def measure_voltage(self):
        return self.app.query("MEASure:VOLTage:DC? AUTO")


    def close(self):
        self.app.clear()
        self.app.close()