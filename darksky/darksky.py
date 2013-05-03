#!/usr/bin/python

from __future__ import division
import json
import urllib
from os import environ
from sys import exit, argv
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Where to save the plot.
plotfile = environ['HOME'] + '/Pictures/ds-rain.png'

# The list of times on the x axis, 10 minutes apart.
checktime = datetime.now()
plotminutes = [10, 20, 30, 40, 50]
plotlabels = [ (checktime + timedelta(minutes=m)).strftime('%-I:%M')
                for m in plotminutes ]

# The probability and number of standard deviations
# associated with the upper and lower bounds.
nUpper = .6745      # 75th percentile
nLower = -.6745     # 25th percentile

# Get the latitude and longitude from the command line
# or use default values from downtown Naperville.
try:
  lat = argv[1]
  lon = argv[2]
except IndexError:
  lat = 34.019087
  lon = -118.497745
  # Naperville
  #lat = 41.772903
  #lon = -88.150392

# Get my API key and construct the URL
try:
  with open(environ['HOME'] + '/.darksky') as rcfile:
    for line in rcfile:
      k, v = line.split(':')
      if k.strip() == 'APIkey':
        APIkey = v.strip()
    dsURL = 'https://api.darkskyapp.com/v1/forecast/%s/%s,%s' % (APIkey, lat, lon)
except (IOError, NameError):
  print "Failed to get API key"
  exit()

# Get the data from Dark Sky.
try:
  jsonString = urllib.urlopen(dsURL).read()
  weather = json.loads(jsonString)
except (IOError, ValueError):
  print "Connection failure to %s" % dsURL
  exit()

# Pluck out the hourly rain forecast information.
startTime = weather['hourPrecipitation'][0]['time']
intensity = [ x['intensity'] for x in weather['hourPrecipitation'] ]
upper = [ min(x['intensity'] + x['error']/3*nUpper, 75) for x in weather['hourPrecipitation'] ]
lower = [ max(x['intensity'] + x['error']/3*nLower, 0) for x in weather['hourPrecipitation'] ]
time = [ (x['time'] - startTime)/60 for x in weather['hourPrecipitation'] ]

# Plot the intensity ranges.
plt.fill_between([0, 59], [15, 15], [0, 0], color='#ffffff', alpha=.01, linewidth=0)
plt.fill_between([0, 59], [30, 30], [15, 15], color='#ffffff', alpha=.02, linewidth=0)
plt.fill_between([0, 59], [45, 45], [30, 30], color='#ffffff', alpha=.04, linewidth=0)
plt.fill_between([0, 59], [75, 75], [45, 45], color='#ffffff', alpha=.08, linewidth=0)

# Plot the values.
plt.plot(time, intensity, color='#ffffff', linewidth=3)
plt.fill_between(time, upper, lower, color='#ffffff', alpha=.05, linewidth=0)
plt.box()
plt.axis([0, 59, 0, 65])
plt.xticks(plotminutes, plotlabels, color='#ffffff')
plt.yticks([])
plt.tick_params('y', length=0, color='#ffffff')
plt.tick_params('x', color='#ffffff')

plt.savefig(plotfile, dpi=50, transparent=True, bbox_inches='tight')

# Pluck and display current and approaching conditions
currentTemperature = weather['currentTemp']
currentCondition = weather['currentSummary']
hourCondition = weather['hourSummary']
dayCondition = weather['daySummary']

print "%s degrees" % currentTemperature
print "Now: %s" % currentCondition
print "Soon: %s" % hourCondition
print "Today: %s" % dayCondition
