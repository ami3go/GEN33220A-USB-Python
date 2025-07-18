import time
import datetime
import csv
import src.GEN33220A_class as gen_class

#
# sweep parameters
#

# Array definition for test
# [start_freq_hz, stop_freq_hz, step_freq_hz, step_time_sec, amplitude_V]
t_step = 5
amp_coefficient  = 2.8
test_parameters = [
    [80,     1000,   10,  t_step, 0.131*amp_coefficient],
    [1000,   5000,   100, t_step, 0.262*amp_coefficient],
    [5000,   9900,   100, t_step, 0.262*amp_coefficient],
    [10000, 40000,  1000, t_step, 0.262*amp_coefficient],
    [40000, 50000,  1000, t_step, 0.262*amp_coefficient],
    [50 ,  150000,  1000, t_step, 0.0857*amp_coefficient],

]

#
# generator config
#

gen = gen_class.GEN_33220A()
gen.reset()
time.sleep(3)
gen.conf_sinus()
gen.set_freq(1)
gen.set_voltage(0)
gen.set_output_load(50)
gen.set_offset(4)
gen.set_trigger_immediate()
gen.trigger()
gen.set_output_on()
time.sleep(1)


#
# sweep cycle
#
for item in test_parameters:
    print(item)


for item in test_parameters:
    start_freq_hz = item[0]
    stop_freq_hz = item[1]
    step_freq_hz = item[2]
    step_time_sec = item[3]
    vout = item[4]
    # gen.set_offset(round((vout*0.8),3)) # calculate offset if amp can't work with negative values
    gen.set_voltage(vout)
    for freq in range(start_freq_hz, stop_freq_hz + step_freq_hz, step_freq_hz ):
        print(f"{datetime.datetime.now()} Set: {freq} Hz, Amp: {vout} V, time: {step_time_sec} sec, {item}")
        gen.set_freq(freq)
        time.sleep(0.1)
        time.sleep(step_time_sec)

gen.set_output_off()