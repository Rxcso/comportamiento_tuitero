#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import codecs
import re
import datetime
import time
from itertools import groupby
import numpy as np
import matplotlib.pyplot as plt
import brewer2mpl

f = codecs.open(sys.argv[1].strip(), "r", "utf-8")
datos = f.readlines()
f.close()

timestamps = []
counting = []
x = []
for line in datos:
    line = line.strip()
    if re.search("^[0-9]{6,},", line):
        line = line.split(",")
        fecha = line[1]
        unix_time = time.mktime(datetime.datetime.strptime(fecha, "%Y-%m-%d %H:%M:%S +%f").timetuple())
        # correct for local time Lima -5 hours
        unix_time -= 60*60*5
        print unix_time
        fecha = fecha.split(" ")[0]
        my_time = datetime.datetime.strptime(fecha, "%Y-%m-%d")
        if my_time not in timestamps:
            timestamps.append(my_time)

        counting.append(fecha)
        if fecha not in x:
            x.append(fecha)
        
# de reversa
timestamp = timestamps[::-1]
y_axis = [len(list(group)) for key, group in groupby(counting)]

# queremos color
set2 = brewer2mpl.get_map('Set2', 'qualitative', 8).mpl_colors
color = set2[0]

fig, ax = plt.subplots(1)

plt.plot(timestamps, y_axis, color=color)
plt.xticks(rotation="45")
plt.ylabel(u"Número de tuits por día")
plt.title(u'Actividad tuitera de Martha Chavez: timeline')
plt.tight_layout()
plt.savefig("timeline" + sys.argv[1].strip() + ".png")
sys.exit()
