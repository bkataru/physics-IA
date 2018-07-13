import pandas as pd
import math
import matplotlib.pyplot as plt
from matplotlib.pyplot import Figure, subplot
import numpy as np

data = pd.read_csv('hygdata_v3.csv')

BC_correction = {'M': -2.0, 'K': -0.8, 'G': -0.4, 'F': -0.15,
                 'A': -0.3, 'B': -2.0, } # NOTE: CORRECTION CONSTANT FOR O-TYPE STARS MISSING


def calculateAbsoluteMag(appMag, dist):
    return appMag - (5 * math.log(dist/10, 10))


def calculateBolometricMag(absMag, starType):
    return absMag + BC_correction[starType]


def calculateLuminosity(bolMag):
    bolMagSun = 4.72
    POGSON_RATIO = -2.5
    lum = 10 ** ((bolMag - bolMagSun) / POGSON_RATIO)
    return lum


def calculateHRadii(lum):
    try:
        innerR = math.sqrt((lum / 1.1))
        outerR = math.sqrt((lum / 0.53))
    except ValueError:
        innerR = 0
        outerR = 0


    return {'inner': innerR, 'outer': outerR}

spectral = data['spect']
appMags = data['mag']
distances = data['dist']

radii = {}

def filterData(spectral, appMags, distances, starType):
    filteredData = []
    for ind in range(len(spectral)):
        if type(spectral[ind]) != str or not spectral[ind]:
            continue
        if distances[ind] == 10000000 or distances[ind] <= 0:
            print('Distance value missing or invalid (mostly in Hipparcos)')
            continue
        try:
            spectral[ind].index(starType)
        except ValueError:
            continue
        filteredData.append({'simp_spectral_type': starType, 'spectral_type': spectral[ind], 'appMag': appMags[ind], 'distance': distances[ind]})

    return filteredData

# O type is missing

def calculate(type):
    data = filterData(spectral, appMags, distances, type)
    radii = []
    for elem in data:
        starType = elem['simp_spectral_type']
        absMag = calculateAbsoluteMag(elem['appMag'], elem['distance'])
        bolMag = calculateBolometricMag(absMag, starType)
        luminosity = calculateLuminosity(bolMag)
        radii_dict = calculateHRadii(luminosity)
        if radii_dict['inner'] == 0 or radii_dict['outer'] == 0:
            continue
        radii.append(radii_dict)
    return radii

data = calculate('M')

# Plotting section below

fig = plt.figure(1)

mag = (1.5 * 10**11) * 5
plt.axis([0, mag, 0, mag])

center = mag / 2

ax = fig.add_subplot(1, 1, 1)

for radius_dict in data:
    inner_radius_in_m = radius_dict['inner'] * (1.5 * 10**11)
    outer_radius_in_m = radius_dict['outer'] * (1.5 * 10 ** 11)
    orbit_inner = plt.Circle((center, center), radius=inner_radius_in_m , color='red', fill=False)
    orbit_outer = plt.Circle((center, center), radius=outer_radius_in_m, color='blue', fill=False)
    ax.add_patch(orbit_inner)
    ax.add_patch(orbit_outer)


#fig.subplots_adjust(left=0.125, right = 0.9, bottom = 0.1, top = 0.9)

plt.show()


