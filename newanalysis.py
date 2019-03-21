import pandas as pd
import math
import matplotlib.pyplot as plt
from matplotlib.pyplot import Figure, subplot
import numpy as np
import calculations
import uncertainties

stellar_data = pd.read_csv('hip2.csv', header=None, usecols=[6, 11, 19, 20, 23, 24])
parallaxes = list(stellar_data[6])
e_plxs = list(stellar_data[11])
appMags = list(stellar_data[19])
e_appMags = list(stellar_data[20])
bvindices = list(stellar_data[23])
e_bvindices = list(stellar_data[24])

filtered_data = []

count = 1
for i in range(len(stellar_data)):
    if parallaxes[i] > 0 and appMags[i]:
        star = {
            'parallax': parallaxes[i],
            'e_plx': e_plxs[i],
            'appMag': appMags[i],
            'e_appMag': e_appMags[i],
            'bvindex': bvindices[i],
            'e_bvindex': e_bvindices[i]
        }
        filtered_data.append(star)
        count += 1

for star in filtered_data:
    star['distance'] = 1000 / star['parallax']
    star['e_dist'] = uncertainties.e_dist(star['distance'], star['parallax'], star['e_plx'])
    star['type'] = calculations.calculateClassAndBCConstant(star['bvindex'])[0]
    star['BCConstant'] = calculations.calculateClassAndBCConstant(star['bvindex'])[1]
    star['absMag'] = calculations.calculateAbsoluteMag(star['appMag'], star['distance'])
    star['e_absMag'] = uncertainties.e_AbsMag(star['appMag'], star['e_appMag'], star['distance'], star['e_dist'])
    star['BolMag'] = calculations.calculateBolometricMag(star['absMag'], star['BCConstant'])
    star['e_BM'] = uncertainties.e_BM(star['e_absMag'])
    star['lum'] = calculations.calculateLuminosity(star['BolMag'])
    star['e_lum'] = uncertainties.e_L(star['lum'], star['e_BM'])
    star['HRadii'] = calculations.calculateHRadii(star['lum'])
    star['e_HRadii'] = {
        'e_inner': uncertainties.e_Inner(star['e_lum'], star['lum'], star['HRadii']['inner']),
        'e_outer': uncertainties.e_Outer(star['e_lum'], star['lum'], star['HRadii']['outer'])
    }



def calculate(type):
    radii_list = []
    e_radii_list = []
    for star in filtered_data:
        if star['type'] == type:
            radii_dict = {}
            e_radii_dict = {}

            radii_dict['inner'] = star['HRadii']['inner']
            e_radii_dict['e_inner'] = star['e_HRadii']['e_inner']
            radii_dict['outer'] = star['HRadii']['outer']
            e_radii_dict['e_outer'] = star['e_HRadii']['e_outer']

            radii_list.append(radii_dict)
            e_radii_list.append(e_radii_dict)

    return [radii_list, e_radii_list]


types = ['M', 'K', 'G', 'F', 'A', 'B', 'O']

with open('statData.txt', 'w') as f:
    for stellar_type in types:
        raw_data = calculate(stellar_type)
        data, e_data = raw_data[0], raw_data[1]
        print(stellar_type, len(data))
        print("{}: {}".format(stellar_type, calculations.statisticalAnalysis(data, e_data)), file=f)

for stellar_type in types:
    raw_data = calculate(stellar_type)
    data, e_data = raw_data[0], raw_data[1]
    print(stellar_type, len(data))

    option = 'line'

    if option == 'circle':
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

    elif option == 'line':
        x_arr = []
        y_arr = []

        for radius_dict in data:
            inner_radius = radius_dict['inner']
            x_arr.append(inner_radius)
            outer_radius = radius_dict['outer']
            y_arr.append(outer_radius)


        plt.scatter(x_arr, y_arr, s=0.1)
        plt.xlabel('Inner radius (in AU)')
        plt.ylabel('Outer radius (in AU)')


    plt.show()


