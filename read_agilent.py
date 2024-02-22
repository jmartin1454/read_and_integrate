#!/usr/bin/python3

import visa


def get_data(chan):
    print(scope.query(':WAV:FORM?'))
    scope.write(':WAV:FORM ASCII')
    print(scope.query(':WAV:FORM?'))
    scope.write(':WAV:SOUR CHAN'+chan)
    print(scope.query(':WAV:SOUR?'))
    data=scope.query(':WAVeform:DATA?')
    data=data[10:] # trim bytes from start of waveform data
    data_float=[float(x) for x in data.split(',')]
    return data_float

# connect to the oscilloscope

rm=visa.ResourceManager('@py')
print(rm.list_resources())
scope=rm.open_resource('USB0::2391::6040::MY51350400::0::INSTR')
print(scope.query('*IDN?'))

# get the data from each channel

data1=get_data('1')
data2=get_data('2')
data3=get_data('3')
data4=get_data('4')

npoints=len(data1)
dt=xinc=float(scope.query('WAV:XINC?'))
import numpy as np
t=[]
for i in range(npoints):
    t.append(dt*i)

import matplotlib.pyplot as plt
#plt.plot(t,data1)
#plt.plot(t,data2)  # chan2 is current
#plt.plot(t,data3)
#plt.plot(t,data4) # chan4 is db/dt
plt.show()

integral=[]
current_integral=0
integral.append(current_integral)
h=[]
h.append(0)
d4offset=data4[-1]
d2offset=data2[-1]
for i,thist in enumerate(t):
    if (thist>12.5):
        print(i,thist,data4[i])
        current_integral+=(data4[i]-d4offset-0.000018)*dt
        integral.append(current_integral)
        h.append(data2[i]-d2offset)
plt.plot(h,integral)
plt.show()
