import GEN33220A_class
import time


gen = GEN33220A_class.GEN_33220A()

#gen.conf_puls()
time.sleep(2)
gen.conf_square()
gen.set_freq("min")
vout = 2.000
gen.set_voltage(vout)
gen.set_output_load(100)
gen.set_output_on()
time.sleep(2)

for i in range(0,100):
    vout = round((vout + 0.1),3)
    print(f"Vout: {vout}")
    gen.set_voltage(vout)
    time.sleep(1)




time.sleep(3)
gen.set_output_off()

gen.close()