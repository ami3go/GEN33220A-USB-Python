import time

import src.GEN33220A_class as gen_class

gen = gen_class.GEN_33220A()

gen.conf_sinus()
gen.set_freq(80)
vout = 2.000
gen.set_voltage(vout)
gen.set_output_load(50)
gen.set_output_on()
gen.sweep(80,1000,20)