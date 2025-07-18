import time

import src.GEN33220A_class as gen_class

#
# sweep parameters
#
start_freq_hz = 80
stop_freq_hz = 1000
step_freq_hz = 10
step_time_sec = 5
vout = 0.13
offset = 3

#
# generator config
#

gen = gen_class.GEN_33220A()
gen.conf_sinus()
gen.set_freq(start_freq_hz)
gen.set_voltage(vout)
gen.set_output_load(50)
gen.set_output_on()
gen.set_offset(3)


#
# sweep cycle
#


for freq in range(start_freq_hz, stop_freq_hz + step_freq_hz, step_freq_hz ):
    print(f"Set: {freq} Hz, amplitude: {vout} V")
    gen.set_freq(freq)
    time.sleep(step_time_sec)

gen.set_output_off()