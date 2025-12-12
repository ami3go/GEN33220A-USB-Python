import visa

class Agilent33220A:
    def __init__(self, resource):
        self.rm = visa.ResourceManager()
        self.inst = self.rm.open_resource(resource)
        self.inst.timeout = 5000

    def idn(self):
        return self.inst.query("*IDN?")

    def beep(self):
        return self.inst.write("beep")

    def reset(self):
        return self.inst.write("*RST")

    def clear(self):
        return self.inst.write("*CLS")

    # Output configuration
    def set_waveform(self, shape):
        assert shape.upper() in ["SIN", "SQU", "RAMP", "PULS", "NOISE", "DC", "USER"]
        self.inst.write(f"FUNCtion {shape.upper()}")

    def set_frequency(self, freq_hz):
        self.inst.write(f"FREQuency {freq_hz}")

    def set_amplitude(self, volts_pp):
        self.inst.write(f"VOLTage {volts_pp}")

    def set_offset(self, volts):
        self.inst.write(f"OFFSet {volts}")

    def output(self, state: bool):
        self.inst.write(f"OUTPut {'ON' if state else 'OFF'}")

    # Pulse
    def set_pulse_duty_cycle(self, percent):
        self.inst.write(f"FUNCtion:PULSe:DCYCle {percent}")

    def set_pulse_transition(self, seconds):
        self.inst.write(f"FUNCtion:PULSe:TRANsition {seconds}")

    def set_pulse_period(self, seconds):
        self.inst.write(f"PULSe:PERiod {seconds}")

    def set_pulse_width(self, seconds):
        self.inst.write(f"PULSe:WIDTh {seconds}")

    # Modulation: AM, FM, PM, FSK, PWM
    def mod_state(self, mode: str, on: bool):
        assert mode.upper() in ["AM", "FM", "PM", "FSK"]
        self.inst.write(f"{mode.upper()}:STATe {'ON' if on else 'OFF'}")

    def mod_source(self, mode: str, source: str):
        assert source.upper() in ["INTERNAL", "EXTERNAL"]
        self.inst.write(f"{mode.upper()}:SOURce {source.upper()}")

    def mod_internal_function(self, mode: str, func: str):
        funcs = ["SINusoid","SQUare","RAMP","NRAMp","TRIangle","NOISe","USER"]
        assert func in funcs
        self.inst.write(f"{mode.upper()}:INTernal:FUNCtion {func.upper()}")

    def mod_internal_frequency(self, mode: str, freq_hz):
        self.inst.write(f"{mode.upper()}:INTernal:FREQuency {freq_hz}")

    def set_mod_depth(self, depth_pct):
        self.inst.write(f"AM:DEPTh {depth_pct}")

    def set_fm_deviation(self, dev_hz):
        self.inst.write(f"FM:DEViation {dev_hz}")

    # FSK hop rate, carrier/hop frequency
    def set_fsk_hop_frequency(self, freq_hz):
        self.inst.write(f"FSKey:HOP:FREQuency {freq_hz}")

    def set_fsk_rate(self, rate_hz):
        self.inst.write(f"FSKey:RATE {rate_hz}")

    # PWM
    def pwm_source(self, source: str):
        assert source.upper() in ["INTERNAL","EXTERNAL"]
        self.inst.write(f"PWM:SOURce {source.upper()}")

    def pwm_internal_function(self, func: str):
        funcs = ["SINusoid","SQUare","RAMP","NRAMp","TRIangle","NOISe","USER"]
        assert func in funcs
        self.inst.write(f"PWM:INTernal:FUNCtion {func.upper()}")

    def pwm_internal_frequency(self, freq_hz):
        self.inst.write(f"PWM:INTernal:FREQuency {freq_hz}")

    # Sweep
    def sweep_enable(self, enable: bool):
        self.inst.write(f"SWEep:STATe {'ON' if enable else 'OFF'}")

    def sweep_center(self, freq_hz):
        self.inst.write(f"FREQuency:CENTer {freq_hz}")

    def sweep_span(self, span_hz):
        self.inst.write(f"FREQuency:SPAN {span_hz}")

    def sweep_marker(self, freq_hz=None, on=True):
        if freq_hz is None:
            self.inst.write(f"MARKer {'ON' if on else 'OFF'}")
        else:
            self.inst.write(f"MARKer:FREQuency {freq_hz}")

    def sweep_trigger_source(self, source: str):
        assert source.upper() in ["IMMEDIATE","EXTERNAL","BUS"]
        self.inst.write(f"TRIGger:SOURce {source.upper()}")

    def sweep_trigger_slope(self, slope: str):
        assert slope.upper() in ["POSitive","NEGative".upper()]
        self.inst.write(f"TRIGger:SLOPe {slope.upper()}")

    def trigger_output(self, enable: bool, slope="POSitive"):
        self.inst.write(f"OUTPut:TRIGger {'ON' if enable else 'OFF'}")
        self.inst.write(f"OUTPut:TRIGger:SLOPe {slope.upper()}")

    # Burst
    def burst_enable(self, enable: bool):
        self.inst.write(f"BURSt:STATe {'ON' if enable else 'OFF'}")

    def burst_mode(self, mode: str):
        assert mode.upper() in ["TRIGGERED","GATED"]
        self.inst.write(f"BURSt:MODE {mode.upper()}")

    def burst_gate_polarity(self, polarity: str):
        assert polarity.upper() in ["NORMAL","INVERTED"]
        self.inst.write(f"BURSt:GATE:POLarity {polarity.upper()}")

    def burst_cycles(self, n):
        self.inst.write(f"BURSt:NCYCles {n}")

    def burst_period(self, seconds):
        self.inst.write(f"BURSt:INTernal:PERiod {seconds}")

    def burst_phase(self, angle_deg):
        self.inst.write(f"BURSt:PHASe {angle_deg}")

    # Trigger (bus trigger)
    def bus_trigger(self):
        self.inst.write("TRIG")

    # Memory
    def memory_recall(self, slot: int):
        self.inst.write(f"MEMory:STATe:RECall {slot}")

    def memory_name(self, slot: int, name: str):
        self.inst.write(f"MEM:STATE:NAME {slot},{name}")

    def memory_auto_recall(self, enable: bool):
        self.inst.write(f"MEMory:STATe:RECall:AUTO {'ON' if enable else 'OFF'}")

    # System
    def system_version(self):
        return self.inst.query("SYSTem:VERSion?")

    # Error queue
    def get_error(self):
        return self.inst.query("SYST:ERR?")

    # Calibration
    def cal_secure(self, on: bool, code="AT33220A"):
        self.inst.write(f"CAL:SECURE:STATE {'ON' if on else 'OFF'},{code}")

    def cal_count(self):
        return self.inst.query("CAL:COUNt?")

    def cal_message(self, msg=None):
        if msg is None:
            return self.inst.query("CAL:MESSage?")
        else:
            self.inst.write(f"CAL:MESSage {msg}")

    def close(self):
        self.inst.close()
        self.rm.close()