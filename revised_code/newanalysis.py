import pandas as pd
import math
import matplotlib.pyplot as plt
from matplotlib.pyplot import Figure, subplot
import numpy as np
import calculations

stellar_data = pd.read_csv('hip2.csv', header=None, usecols=[6, 19, 23])
parallaxes = list(stellar_data[6])
appMags = list(stellar_data[19])
bvindices = list(stellar_data[23])

filtered_data = []

count = 1
for i in range(len(stellar_data)):
    if parallaxes[i] > 0 and appMags[i]:
        distance = 1000 / parallaxes[i] # distance in parsecs
        star = {
            'distance': distance,
            'appMag': appMags[i],
            'bvindex': bvindices[i]
        }
        filtered_data.append(star)
        count += 1

for star in filtered_data:
    star['type'] = calculations.calculateClassAndBCConstant(star['bvindex'])[0]
    star['BCConstant'] = calculations.calculateClassAndBCConstant(star['bvindex'])[1]
    star['absMag'] = calculations.calculateAbsoluteMag(star['appMag'], star['distance'])
    star['BolMag'] = calculations.calculateBolometricMag(star['absMag'], star['BCConstant'])
    star['lum'] = calculations.calculateLuminosity(star['BolMag'])
    star['HRadii'] = calculations.calculateHRadii(star['lum'])

def calculate(type):
    radii_list = []
    for star in filtered_data:
        if star['type'] == type:
            radii_dict = {}
            radii_dict['inner'] = star['HRadii']['inner']
            radii_dict['outer'] = star['HRadii']['outer']
            radii_list.append(radii_dict)

    return radii_list


types = ['M', 'K', 'G', 'F', 'A', 'B', 'O']

with open('statData.txt', 'w') as f:
    for stellar_type in types:
        data = calculate(stellar_type)
        print("{}: {}".format(stellar_type, calculations.statisticalAnalysis(data)), file=f)



'''
# Plotting section below

fig = plt.figure(1)

mag = 3000
plt.axis([0, mag, 0, mag])

center = mag / 2

ax = fig.add_subplot(1, 1, 1)

for radius_dict in data:
    inner_radius = radius_dict['inner']
    outer_radius = radius_dict['outer']
    orbit_inner = plt.Circle((center, center), radius=inner_radius, color='red', fill=False)
    orbit_outer = plt.Circle((center, center), radius=outer_radius, color='blue', fill=False)
    ax.add_patch(orbit_inner)
    ax.add_patch(orbit_outer)

plt.show()
'''