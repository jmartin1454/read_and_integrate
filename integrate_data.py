#!/usr/bin/python3

import matplotlib.pyplot as plt

with open('write_agilent.out','r') as f:
    data=[[float(num) for num in line.split()] for line in f]
print(data)
t,data1,data2,data3,data4=zip(*data)
print(t)

dt=t[1]-t[0]

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
