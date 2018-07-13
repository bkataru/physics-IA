import pandas as pd
import math
import matplotlib.pyplot as plt
from matplotlib.pyplot import Figure, subplot
import numpy as np

data = pd.read_csv('hygdata_v3.csv')

def calculateHRadii(lum):
    try:
        innerR = math.sqrt(lum / 1.1)
        outerR = math.sqrt(lum / 0.53)
    except ValueError:
        innerR = 0
        outerR = 0


    return {'inner': innerR, 'outer': outerR}

spectral = data['spect']
appMags = data['mag']
lums = data['lum']
distances = data['dist']

radii = {}

def filterData(spectral, appMags, distances, starType):
    filteredData = []
    for ind in range(len(spectral)):
        if type(spectral[ind]) != str or not spectral[ind]:
            continue
        if distances[ind] >= 10000000 or distances[ind] <= 0:
            print('Distance value missing or invalid (mostly in Hipparcos)')
            continue
        try:
            spectral[ind].index(starType)
        except ValueError:
            continue
        filteredData.append({'simp_spectral_type': starType, 'spectral_type': spectral[ind], 'appMag': appMags[ind], 'distance': distances[ind], 'luminosity': lums[ind]})

    return filteredData

# O type is missing

def calculate(type):
    data = filterData(spectral, appMags, distances, type)
    radii = []
    for elem in data:
        luminosity = elem['luminosity']
        radii_dict = calculateHRadii(luminosity)
        if radii_dict['inner'] == 0 or radii_dict['outer'] == 0:
            continue
        radii.append(radii_dict)
    return radii

data = calculate('M')
print(len(data))
print(data)
# Plotting section below

fig = plt.figure(1)

mag = 20
plt.axis([0, mag, 0, mag])

center = mag / 2

ax = fig.add_subplot(1, 1, 1)

for radius_dict in data:
    inner_radius = radius_dict['inner']
    outer_radius = radius_dict['outer']
    if inner_radius > 5 or outer_radius > 5:
        print(inner_radius, outer_radius)
    orbit_inner = plt.Circle((center, center), radius=inner_radius, color='red', fill=False)
    orbit_outer = plt.Circle((center, center), radius=outer_radius, color='blue', fill=False)
    ax.add_patch(orbit_inner)
    ax.add_patch(orbit_outer)

plt.show()


