#!/usr/bin/python3

# writes data from agilent scope to disk
# Mon 11 Mar 2024 10:13:34 AM CDT
# Jeff modifying to write data from Tek scope to disk

import visa
import numpy as np
from struct import unpack

def get_data(chan):
    #####################################
    # old agilent code
    #print(scope.query(':WAV:FORM?'))
    #scope.write(':WAV:FORM ASCII')
    #print(scope.query(':WAV:FORM?'))
    #scope.write(':WAV:SOUR CHAN'+chan)
    #print(scope.query(':WAV:SOUR?'))
    #data=scope.query(':WAVeform:DATA?')
    #data=data[10:] # trim bytes from start of waveform data
    #data_float=[float(x) for x in data.split(',')]
    #return data_float
    #####################################
    scope.write("DATA:SOURCE "+chan)
    scope.write('DATA:WIDTH 1')
    scope.write('DATA:ENC RPB')
    ymult = float(scope.ask('WFMPRE:YMULT?'))
    yzero = float(scope.ask('WFMPRE:YZERO?'))
    yoff = float(scope.ask('WFMPRE:YOFF?'))
    xincr = float(scope.ask('WFMPRE:XINCR?'))
    xdelay = float(scope.query('HORizontal:POSition?'))
    scope.write('CURVE?')
    data = scope.read_raw()
    headerlen = 2 + int(data[1])
    header = data[:headerlen]
    ADC_wave = data[headerlen:-1]
    ADC_wave = np.array(unpack('%sB' % len(ADC_wave),ADC_wave))
    Volts = (ADC_wave - yoff) * ymult  + yzero
    Time = np.arange(0, (xincr * len(Volts)), xincr)-((xincr * len(Volts))/2-xdelay)
    return Time,Volts


# connect to the oscilloscope

rm=visa.ResourceManager('@py')
print(rm.list_resources())
# line below is for agilent
# scope=rm.open_resource('USB0::2391::6040::MY51350400::0::INSTR')
# line below is for Tek
scope=rm.open_resource('USB0::1689::1025::C011321::0::INSTR')
print(scope.query('*IDN?'))

# get the data from each channel

t1,data1=get_data('1')
print(t1,data1)
t2,data2=get_data('2')
t3,data3=get_data('3')
t4,data4=get_data('4')

npoints=len(data1)
dt=xinc=float(scope.query('WAV:XINC?'))
import numpy as np
t=[]
for i in range(npoints):
    t.append(dt*i)

import matplotlib.pyplot as plt
plt.plot(t,data1)
plt.plot(t,data2)  # chan2 is current
plt.plot(t,data3)
plt.plot(t,data4) # chan4 is db/dt
plt.show()

with open('write_agilent.out','w') as f:
    for x in zip(t,data1,data2,data3,data4):
        f.write('{} {} {} {} {}\n'.format(*x))

