import math
import statistics

def calculateClassAndBCConstant(bvindex):
    spectralClass = None
    BCConstant = None
    if bvindex >= 1.45:
        if bvindex >= 1.63:
            BCConstant = -2.3
        else:
            BCConstant = -1.2
        spectralClass = 'M'
    elif bvindex >= 0.89:
        if bvindex >= 1.18:
            BCConstant = -0.6
        else:
            BCConstant = -0.2
        spectralClass = 'K'
    elif bvindex >= 0.58:
        if bvindex >= 0.7:
            BCConstant = -0.07
        else:
            BCConstant = -0.03
        spectralClass = 'G'
    elif bvindex >= 0.27:
        if bvindex >= 0.42:
            BCConstant = 0
        else:
            BCConstant = -0.06
        spectralClass = 'F'
    elif bvindex >= 0:
        if bvindex >= 0.13:
            BCConstant = -0.12
        else:
            BCConstant = -0.4
        spectralClass = 'A'
    elif bvindex >= -0.31:
        if bvindex >= -0.16:
            BCConstant = -1.5
        else:
            BCConstant = -2.8
        spectralClass = 'B'
    else:
        BCConstant = -4.0
        spectralClass = 'O'

    return [spectralClass, BCConstant]


def calculateAbsoluteMag(appMag, dist):
    return appMag - (5 * math.log(dist/10, 10))


def calculateBolometricMag(absMag, BCConstant):
    return absMag + BCConstant


def calculateLuminosity(bolMag):
    bolMagSun = 4.72
    POGSON_RATIO = -2.5
    lum = 10 ** ((bolMag - bolMagSun) / POGSON_RATIO)
    return lum


def calculateHRadii(lum): # in astronomical units
    try:
        innerR = math.sqrt((lum / 1.1))
        outerR = math.sqrt((lum / 0.53))
    except ValueError:
        innerR = 0
        outerR = 0


    return {'inner': innerR, 'outer': outerR}

def statisticalAnalysis(radii_data, e_radii_data):
    inner_arr = []
    e_inner_arr = []
    outer_arr = []
    e_outer_arr = []
    print(radii_data)
    for radii_dict in radii_data:
        inner_arr.append(radii_dict['inner'])
        outer_arr.append(radii_dict['outer'])

    for e_dict in e_radii_data:
        e_inner_arr.append(e_dict['e_inner'])
        e_outer_arr.append(e_dict['e_outer'])

    data = {}
    data['inner_mean'] = statistics.mean(inner_arr)
    data['inner_mean_uncertainty'] = statistics.mean(e_inner_arr)
    data['outer_mean'] = statistics.mean(outer_arr)
    data['outer_mean_uncertainty'] = statistics.mean(e_outer_arr)

    data['inner_median'] = statistics.median(inner_arr)
    data['inner_median_uncertainty'] = statistics.median(e_inner_arr)
    data['outer_median'] = statistics.median(outer_arr)
    data['outer_median_uncertainty'] = statistics.median(e_outer_arr)

    data['inner_pstdev'] = statistics.pstdev(inner_arr)
    data['outer_pstdev'] = statistics.pstdev(outer_arr)

    return data

