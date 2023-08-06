import krangpower as kp
from numpy import round
from numpy.random import random
import csv

import tools._smart_components

kp.set_log_level(30)

um = kp.UM
src = kp.Vsource(basekv=10.0 * um.kV)
twc = kp.Krang('twc', src)
twc['sourcebus', 'a'] << kp.Line(units='m', length=20.0 * um.m).aka('l1')

# -------------------------------------------------------
# 3-winding transformer
trf = kp.Transformer(windings=3,
                     conns=['delta', 'wye', 'wye'],
                     kvs=[10.0, 2.0, 3.0] * um.kV,
                     kvas=[100.0, 20.0, 85.0] * um.kW,
                     taps=[1.0, 1.0, 1.0],
                     pctrs=[1.0, 1.0, 1.0])
twc['a', 'b', 'c'] << trf.aka('trf')  # the first winding is considered primary
twc['b', 'bb'] << kp.Line(units='m', length=10.0 * um.m).aka('lbb')
twc['c', 'cc'] << kp.Line(units='m', length=15.0 * um.m).aka('lcc')

# -------------------------------------------------------
# live csv loadshape creation
with open('ls.csv', 'w') as csvfile:
    lshwriter = csv.writer(csvfile, delimiter=',')
    lshwriter.writerow(['1.0'])
    lshwriter.writerow(['1.1'])
    lshwriter.writerow(['1.2'])
    lshwriter.writerow(['0.9'])
    lshwriter.writerow(['0.2'])
    lshwriter.writerow(['1.8'])

ls = kp.CsvLoadshape('simple_lsh', 'ls.csv', interval=2 * um.min)
twc << ls
twc['cc', ] << kp.Load(kv=3.0 * um.kV, kw=35.0 * um.kW).aka('loadhi') * ls


# -------------------------------------------------------
# a simple fourq
class MyDM(tools._smart_components.DecisionModel):
    def decide_pq(self, oek, mynode):
        return round(5.0 * random(), decimals=3) * um.kW,\
               round(1.0 * random(), decimals=3) * um.kW


fq = tools._smart_components.FourQ(kv=2.0 * um.kV)
twc['bb', ] << fq.aka('myfq') * MyDM()


twc.set(number=6, stepsize=2 * um.min)
twc.drag_solve()


# -------------------------------------------------------
# GraphView demonstration
bvo = kp.gv.VoltageView(twc)
print(round(bvo['bb'], 2))
print(round(bvo['b', 'bb'], 2))

twc.pack_ckt(r'twc.zip')
two = kp._open_ckt(r'twc.zip')  # verifies that the hash-checking works
